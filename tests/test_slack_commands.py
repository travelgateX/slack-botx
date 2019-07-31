import json
from time import time
import pytest
import urllib.parse
from starlette.testclient import TestClient
from app.common.config import Config
from app.main import app
from app.common.util import (create_slack_signature)
from app.common.slack_models import CommandModelIn, CommandModelOut
from app.tasks.factory import Macro,command_factory
from app.tasks.base_tasks import Command


client = TestClient(app)

def _send_data( payload ):
  SLACK_SIGNING_SECRET = Config.get_or_else('SLACK','SIGNING_SECRET',None)
  timestamp = int(time())
  signature = create_slack_signature(SLACK_SIGNING_SECRET, timestamp, payload)

  response = client.post(
        url="slack/commands",
        headers={
                 'X-Slack-Request-Timestamp': str(timestamp),
                 'X-Slack-Signature': signature,
                 'content-type':'application/x-www-form-urlencoded'
                },
        data=payload
    )
  print(f"response:[{response}], content:[{response.content}]")
  return response

def test_insightsx(mock_env_slack):
  payload = { "team_id":"T0001",
              "team_domain":"example",
              "enterprise_id":"E0001",
              "enterprise_name": "name enterprise",
              "channel_id": "test",
              "channel_name": "test_channel",
              "user_id": "U2147483697",
              "user_name": "Steve",
              "response_url":"https://slack.faketest.com",
              "trigger_id":"13345224609.738474920.8088930838d88f008e0",
              "command": "/insightsx",
              "text": "dummy_test"
            }
  response = _send_data(urllib.parse.urlencode(payload))
  assert response.status_code == 404
  

def test_alertsx(mock_env_slack):
  payload = { "team_id":"T0001",
              "team_domain":"example",
              "enterprise_id":"E0001",
              "enterprise_name": "name enterprise",
              "channel_id": "test",
              "channel_name": "test_channel",
              "user_id": "U2147483697",
              "user_name": "Steve",
              "response_url":"https://slack.faketest.com",
              "trigger_id":"13345224609.738474920.8088930838d88f008e0",
              "command": "/alertsx",
              "text": "status",
              "text_test": "dummy_test"
            }
  response = _send_data(urllib.parse.urlencode(payload))
  assert response.status_code == 200
  assert response.json()['text_test'] == "dummy_test"

@pytest.mark.asyncio
async def test_alertsx_needs_help(mock_env_slack):
    command = { "team_id":"T0001",
                "team_domain":"example",
                "enterprise_id":"E0001",
                "enterprise_name": "name enterprise",
                "channel_id": "test",
                "channel_name": "test_channel",
                "user_id": "U2147483697",
                "user_name": "Steve",
                "response_url":"https://slack.faketest.com",
                "trigger_id":"13345224609.738474920.8088930838d88f008e0",
                "command": "/alertsx",
                "text": "help"
              }

    command_model = CommandModelIn( **command) 
    command_name = command_model.command[1:]
    command:Command = command_factory(command_name, command_model)
    
    #Check if commands need help and response immediately
    ret:CommandModelOut = await command.help_payload()
    assert ret is not None

@pytest.mark.asyncio
async def test_alertsx_not_needs_help(mock_env_slack):
    command = { "team_id":"T0001",
                "team_domain":"example",
                "enterprise_id":"E0001",
                "enterprise_name": "name enterprise",
                "channel_id": "test",
                "channel_name": "test_channel",
                "user_id": "U2147483697",
                "user_name": "Steve",
                "response_url":"https://slack.faketest.com",
                "trigger_id":"13345224609.738474920.8088930838d88f008e0",
                "command": "/alertsx",
                "text": "status"
              }

    command_model = CommandModelIn( **command) 
    command_name = command_model.command[1:]
    command:Command = command_factory(command_name, command_model)
    
    #Check if commands need help and response immediately
    ret:CommandModelOut = await command.help_payload()
    assert ret is None