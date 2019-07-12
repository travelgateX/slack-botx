import json
from time import time

from starlette.testclient import TestClient

from app.main import app,SLACK_SIGNING_SECRET
from app.common.slack_util import create_signature

client = TestClient(app)

def _send_data( data ):
    data_json = json.dumps(data)     
    timestamp = int(time())
    signature = create_signature(SLACK_SIGNING_SECRET, timestamp, data_json)
    response = client.post(
        "slack/events",
         headers={
            'X-Slack-Request-Timestamp': str(timestamp),
            'X-Slack-Signature': signature
        },
        json=data
    )
    print(f"response:[{response}], content:[{response.content}]")
    return response

def test_team_join():
    data= {"token": "does_not_matter",
           "team_id":"T9R353D0A",
           "api_app_id":"AJXG7EL20",
           "type": "event_callback", 
           "event": {
              "type": "team_join",
              "user": {
                "id":"test",
                "name":"user_name",
                "real_name": "Oscar Test" 
              }
           }
         }
    response = _send_data(data)    
    assert response.status_code == 200
    

def test_url_verification():
    data= {"token": "does_not_matter", 
           "challenge": "3eZbrw1aBm2rZgRNFdxV2595E9CY3gmdALWMmHkvFXO7tYXAYM8P", 
           "type": "url_verification"
         }

    response = _send_data(data)    
    assert response.status_code == 200
    assert response.json() == {"challenge": "3eZbrw1aBm2rZgRNFdxV2595E9CY3gmdALWMmHkvFXO7tYXAYM8P"}