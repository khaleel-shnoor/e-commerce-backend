"""Reusable SMTP email service for auth, orders, and notifications."""

from __future__ import annotations

import asyncio
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import TYPE_CHECKING

from app.services.email import templates

if TYPE_CHECKING:
    from app.core.config import Settings

logger = logging.getLogger(__name__)


class EmailService:
    """
    Application-wide email sender.

    Configure via SMTP_* env vars. All high-level methods delegate to send_email().
    """

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    @property
    def is_configured(self) -> bool:
        return self.settings.smtp_ready

    async def send_email(
        self,
        to: str,
        subject: str,
        html_body: str,
        text_body: str | None = None,
        *,
        reply_to: str | None = None,
    ) -> bool:
        """
        Send an email. Returns True if sent (or logged in dev fallback), False on failure.

        Runs blocking SMTP in a thread pool to keep the API async.
        """
        if not self.is_configured:
            logger.warning(
                "SMTP not configured — email not sent (to=%s, subject=%s). "
                "Set SMTP_HOST, SMTP_USER, SMTP_PASS, SMTP_FROM and SMTP_ENABLED=true.",
                to,
                subject,
            )
            if self.settings.is_development and text_body:
                logger.info("Dev email preview to=%s\n%s", to, text_body)
            return False

        try:
            await asyncio.to_thread(
                self._send_smtp_sync,
                to,
                subject,
                html_body,
                text_body,
                reply_to,
            )
            logger.info("Email sent to %s — %s", to, subject)
            return True
        except Exception:
            logger.exception("Failed to send email to %s — %s", to, subject)
            return False

    def _send_smtp_sync(
        self,
        to: str,
        subject: str,
        html_body: str,
        text_body: str | None,
        reply_to: str | None,
    ) -> None:
        from_addr = self.settings.smtp_from or self.settings.smtp_user
        assert from_addr is not None

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = from_addr
        msg["To"] = to
        if reply_to:
            msg["Reply-To"] = reply_to

        plain = text_body or _html_to_plain(html_body)
        msg.attach(MIMEText(plain, "plain", "utf-8"))
        msg.attach(MIMEText(html_body, "html", "utf-8"))

        host = self.settings.smtp_host
        port = self.settings.smtp_port
        user = self.settings.smtp_user
        password = self.settings.smtp_password
        assert host and user and password

        if self.settings.smtp_secure:
            with smtplib.SMTP_SSL(host, port, timeout=30) as server:
                server.login(user, password)
                server.sendmail(from_addr, [to], msg.as_string())
        else:
            with smtplib.SMTP(host, port, timeout=30) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(user, password)
                server.sendmail(from_addr, [to], msg.as_string())

    # --- Domain-specific helpers (reuse across the app) ---

    async def send_password_reset(self, email: str, reset_token: str) -> bool:
        reset_url = f"{self.settings.frontend_url}/reset-password?token={reset_token}"
        subject, text, html = templates.password_reset(
            reset_url=reset_url,
            expire_minutes=self.settings.password_reset_expire_minutes,
        )
        return await self.send_email(email, subject, html, text)

    async def send_verification(self, email: str, verify_token: str) -> bool:
        verify_url = f"{self.settings.frontend_url}/verify-email?token={verify_token}"
        subject, text, html = templates.email_verification(
            verify_url=verify_url,
            expire_hours=self.settings.email_verification_expire_hours,
        )
        return await self.send_email(email, subject, html, text)

    async def send_order_placed(
        self,
        email: str,
        *,
        customer_name: str,
        order_number: str,
        total: str,
        order_id: str,
    ) -> bool:
        """Send order confirmation — call from OrderService when checkout is implemented."""
        order_url = f"{self.settings.frontend_url}/account/orders/{order_id}"
        subject, text, html = templates.order_placed(
            customer_name=customer_name,
            order_number=order_number,
            total=total,
            order_url=order_url,
        )
        return await self.send_email(email, subject, html, text)


def _html_to_plain(html: str) -> str:
    """Minimal HTML strip for plain-text fallback."""
    import re

    text = re.sub(r"<br\s*/?>", "\n", html, flags=re.I)
    text = re.sub(r"<[^>]+>", "", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip()
