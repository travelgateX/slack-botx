import json
import os
import logging
import urllib.parse
from time import time
from datetime import datetime

from starlette.testclient import TestClient

from app.common.config import Config
from app.main import app
from app.common.util import create_slack_signature

client = TestClient(app)

def _send_data( payload ):
    response = client.post(
        url="onwebchange/webhook",
        headers={'content-type':'application/x-www-form-urlencoded'},
        data=payload
    )
    print(f"response:[{response}], content:[{response.content}]")
    return response

def test_onwebchange_callback(mock_env_slack):
    today = datetime.today().strftime('%Y-%m-%d')
    params = { "femtoo_callback_url": "https://docs.travelgatex.com/hotel-x/release-notes/changelog/",
               "femtoo_callback_data": "Alerts-X changelog    Edit page  Easily accessible log of notable changes to Alerts-X  "+ today +"    After an alert configuration update their past  events will be deleted.  2019-06-12    Fixed an error that was causing an unsuccessful alert create or update to set  clients ,  suppliers and  accesses to the alert for Travelgate Teams users.  2019-06-11    Fixed an error to return all the  events of the alerts.  2019-06-06    Added  /Health to check service status.  2019-05-23    Alerts-X  product documentation is available   Comments",
               "femtoo_callback_label":"Hotel-X"
             }
    response = _send_data(urllib.parse.urlencode(params))
    assert response.status_code == 200
    