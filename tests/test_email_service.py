"""Email service unit tests (SMTP mocked)."""

from unittest.mock import MagicMock, patch

import pytest

from app.core.config import Settings
from app.services.email import EmailService


@pytest.fixture
def smtp_settings() -> Settings:
    return Settings(
        _env_file=None,
        SMTP_ENABLED=True,
        SMTP_HOST="smtp.gmail.com",
        SMTP_PORT=587,
        SMTP_SECURE=False,
        SMTP_USER="test@shnoor.com",
        SMTP_FROM="test@shnoor.com",
        SMTP_PASS="secret",
        FRONTEND_URL="http://localhost:5173",
    )


@pytest.mark.asyncio
async def test_send_password_reset_calls_smtp(smtp_settings: Settings) -> None:
    service = EmailService(smtp_settings)
    with patch.object(service, "_send_smtp_sync") as mock_send:
        result = await service.send_password_reset("user@example.com", "token-abc")
    assert result is True
    mock_send.assert_called_once()
    args = mock_send.call_args[0]
    assert args[0] == "user@example.com"
    assert "Reset your SHNOOR password" in args[1]
    assert "token-abc" in args[3] or "token-abc" in args[2]


@pytest.mark.asyncio
async def test_send_email_skipped_when_not_configured() -> None:
    service = EmailService(Settings(_env_file=None, SMTP_ENABLED=False))
    result = await service.send_email("a@b.com", "Hi", "<p>Hi</p>", "Hi")
    assert result is False
