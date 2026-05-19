"""HTML/text email templates — add new renderers here for order, promo, etc."""

from html import escape


def _layout(title: str, body_html: str, footer: str = "SHNOOR E-Commerce") -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><title>{escape(title)}</title></head>
<body style="font-family:system-ui,sans-serif;line-height:1.6;color:#111;max-width:560px;margin:0 auto;padding:24px;">
  <p style="font-size:20px;font-weight:600;letter-spacing:0.08em;">SHNOOR</p>
  {body_html}
  <hr style="border:none;border-top:1px solid #e5e5e5;margin:32px 0 16px;">
  <p style="font-size:12px;color:#666;">{escape(footer)}</p>
</body>
</html>"""


def password_reset(*, reset_url: str, expire_minutes: int) -> tuple[str, str, str]:
    """Return (subject, plain_text, html)."""
    subject = "Reset your SHNOOR password"
    text = (
        f"Reset your password using this link (expires in {expire_minutes} minutes):\n\n"
        f"{reset_url}\n\n"
        "If you did not request this, you can ignore this email."
    )
    html = _layout(
        subject,
        f"""
  <h1 style="font-size:22px;font-weight:600;">Reset your password</h1>
  <p>We received a request to reset your password. Click the button below — the link expires in
     <strong>{expire_minutes} minutes</strong>.</p>
  <p style="margin:28px 0;">
    <a href="{escape(reset_url)}"
       style="display:inline-block;background:#000;color:#fff;text-decoration:none;
              padding:12px 24px;border-radius:6px;font-weight:500;">
      Reset password
    </a>
  </p>
  <p style="font-size:14px;color:#444;">Or copy this link into your browser:<br>
     <a href="{escape(reset_url)}">{escape(reset_url)}</a></p>
  <p style="font-size:14px;color:#666;">If you did not request a reset, ignore this email.</p>
""",
    )
    return subject, text, html


def email_verification(*, verify_url: str, expire_hours: int) -> tuple[str, str, str]:
    subject = "Verify your SHNOOR email"
    text = (
        f"Verify your email (expires in {expire_hours} hours):\n\n{verify_url}\n\n"
        "If you did not create an account, ignore this email."
    )
    html = _layout(
        subject,
        f"""
  <h1 style="font-size:22px;font-weight:600;">Verify your email</h1>
  <p>Thanks for joining SHNOOR. Confirm your email to activate your account
     (link expires in <strong>{expire_hours} hours</strong>).</p>
  <p style="margin:28px 0;">
    <a href="{escape(verify_url)}"
       style="display:inline-block;background:#000;color:#fff;text-decoration:none;
              padding:12px 24px;border-radius:6px;font-weight:500;">
      Verify email
    </a>
  </p>
  <p style="font-size:14px;color:#444;">Or copy this link:<br>
     <a href="{escape(verify_url)}">{escape(verify_url)}</a></p>
""",
    )
    return subject, text, html


def order_placed(
    *,
    customer_name: str,
    order_number: str,
    total: str,
    order_url: str,
) -> tuple[str, str, str]:
    """Template for future order confirmation emails."""
    subject = f"Order confirmed — {order_number}"
    text = (
        f"Hi {customer_name},\n\n"
        f"Your order {order_number} was placed successfully.\n"
        f"Total: {total}\n\nView order: {order_url}\n"
    )
    html = _layout(
        subject,
        f"""
  <h1 style="font-size:22px;font-weight:600;">Order confirmed</h1>
  <p>Hi {escape(customer_name)},</p>
  <p>Thank you for your order <strong>{escape(order_number)}</strong>.</p>
  <p>Total: <strong>{escape(total)}</strong></p>
  <p style="margin:28px 0;">
    <a href="{escape(order_url)}"
       style="display:inline-block;background:#000;color:#fff;text-decoration:none;
              padding:12px 24px;border-radius:6px;font-weight:500;">
      View order
    </a>
  </p>
""",
    )
    return subject, text, html
