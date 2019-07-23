import json
from time import time
import urllib.parse
from starlette.testclient import TestClient
from app.common.util import create_slack_signature
from app.common.config import Config
from app.main import app

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
              "response_url":"https://hooks.slack.com/commands/1234/5678",
              "trigger_id":"13345224609.738474920.8088930838d88f008e0",
              "command": "insightsx",
              "text": "dummy_test"
            }
  response = _send_data(urllib.parse.urlencode(payload))
  assert response.status_code in (200,422)