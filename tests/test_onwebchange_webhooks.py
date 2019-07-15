import json
from time import time

from starlette.testclient import TestClient

from app.main import app,SLACK_SIGNING_SECRET
from app.common.util import create_slack_signature

client = TestClient(app)

def _send_data( data ):
    response = client.post(
        "onwebchange/webhook",
        json=data
    )
    print(f"response:[{response}], content:[{response.content}]")
    return response

def test_team_join():
    data= {"femtoo_callback_url": "https://docs.travelgatex.com/hotel-x/release-notes/changelog/",
           "femtoo_callback_data":"testdatattttt",
           "femtoo_callback_label":"Hotel-X"
         }
    response = _send_data(data)    
    assert response.status_code == 200
    