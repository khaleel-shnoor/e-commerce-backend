"""Email delivery — SMTP-backed, reusable across auth, orders, and notifications."""

from app.services.email.service import EmailService

__all__ = ["EmailService"]
