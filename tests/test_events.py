from time import time
from starlette.testclient import TestClient
from tests.conftest import create_signature

from app.main import app,SLACK_SIGNING_SECRET

client = TestClient(app)

def test_url_verification():
    data={"token": "does_not_matter", 
          "challenge": "3eZbrw1aBm2rZgRNFdxV2595E9CY3gmdALWMmHkvFXO7tYXAYM8P", 
          "type": "url_verification"},
    
    timestamp = int(time())
    signature = create_signature(SLACK_SIGNING_SECRET, timestamp, str(data))

    response = client.post(
        "slack/events",
         headers={
            'X-Slack-Request-Timestamp': str(timestamp),
            'X-Slack-Signature': signature
        },
        json=data
    )
    assert response.status_code == 200
    assert response.json() == {
        "challenge": "3eZbrw1aBm2rZgRNFdxV2595E9CY3gmdALWMmHkvFXO7tYXAYM8P", 
    }