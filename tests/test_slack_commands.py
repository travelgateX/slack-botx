import json
from time import time
import urllib.parse
from starlette.testclient import TestClient
from app.common.util import create_slack_signature
from app.common.config import Config
from app.main import app

client = TestClient(app)

def _send_data( payload ):
  timestamp = int(time())
  SLACK_SIGNING_SECRET = Config.get_or_else('SLACK','SIGNING_SECRET',None)
  
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
  payload = { "command": "insightsx",
              "text": "dummy_test",
              "channel_id":"test"
            }
  response = _send_data(urllib.parse.urlencode(payload))
  #response = _send_data(payload)
  assert response.status_code in (200,404)
  
