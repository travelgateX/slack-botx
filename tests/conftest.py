import json
import hashlib
import hmac
import pytest

@pytest.fixture
def mock_env_slack(monkeypatch):
    monkeypatch.setenv("SLACK_CHANNEL_TGX_ANNOUNCEMENTS", "test")
    monkeypatch.setenv("SLACK_CHANNEL_ALL_ANNOUNCEMENTS", "test")
    monkeypatch.setenv("SLACK_SIGNING_SECRET", "dummy-signing-secret")
    
