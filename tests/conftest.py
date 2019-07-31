import json
import hashlib
import hmac
import pytest
import app.common.util
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

@pytest.fixture
def mock_env_slack(monkeypatch):
    monkeypatch.setenv("SLACK_CHANNEL_TGX_ANNOUNCEMENTS", "test")
    monkeypatch.setenv("SLACK_CHANNEL_ALL_ANNOUNCEMENTS", "test")
    monkeypatch.setenv("SLACK_SIGNING_SECRET", "dummy-signing-secret")

def send_slack_post_json_fake(url:str, data_json:json):
    return data_json

def send_slack_post_model_fake(url:str, data_model:BaseModel):
    return send_slack_post_json_fake(url=url, data_json=jsonable_encoder(data_model))


@pytest.fixture(autouse=True)
def mock_slack_post_response(monkeypatch):
    monkeypatch.setattr(app.common.util, 'send_slack_post_json', send_slack_post_json_fake)
    monkeypatch.setattr(app.common.util, 'send_slack_post_model', send_slack_post_model_fake)