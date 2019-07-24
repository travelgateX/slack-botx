import json
import hashlib
import hmac
import pytest
import app.common.util

@pytest.fixture
def mock_env_slack(monkeypatch):
    monkeypatch.setenv("SLACK_CHANNEL_TGX_ANNOUNCEMENTS", "test")
    monkeypatch.setenv("SLACK_CHANNEL_ALL_ANNOUNCEMENTS", "test")
    monkeypatch.setenv("SLACK_SIGNING_SECRET", "dummy-signing-secret")

def slack_post_ok(url:str, data:json):
    return data

@pytest.fixture(autouse=True)
def mock_slack_post_response(monkeypatch):
    import app.common.util
    monkeypatch.setattr(app.common.util, 'send_slack_post', slack_post_ok)