import json
from time import time

from starlette.testclient import TestClient

from app.main import app,SLACK_SIGNING_SECRET
from app.utils.slack import create_slack_signature

client = TestClient(app)

def test_url_verification():
    data= {"token": "does_not_matter", 
           "challenge": "3eZbrw1aBm2rZgRNFdxV2595E9CY3gmdALWMmHkvFXO7tYXAYM8P", 
           "type": "url_verification"
         }
    data_json = json.dumps( data )     
   
    timestamp = int(time())
    signature = create_slack_signature(SLACK_SIGNING_SECRET, timestamp, data_json)

    response = client.post(
        "slack/events",
         headers={
            'X-Slack-Request-Timestamp': str(timestamp),
            'X-Slack-Signature': signature
        },

        json=data_json
    )
    #assert response.status_code == 200
    #assert response.json() == {"challenge": "3eZbrw1aBm2rZgRNFdxV2595E9CY3gmdALWMmHkvFXO7tYXAYM8P"}