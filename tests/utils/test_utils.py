import json
from time import time

from app.main import SLACK_SIGNING_SECRET
from app.utils.slack import create_slack_signature,validate_slack_signature

def test_slack_signature():
    timestamp = int(time())
    signature = create_slack_signature(SLACK_SIGNING_SECRET, timestamp, "test_data")
    assert True==validate_slack_signature(SLACK_SIGNING_SECRET, "test_data", timestamp, signature )
    assert False==validate_slack_signature(SLACK_SIGNING_SECRET, "test_data_err", timestamp, signature )