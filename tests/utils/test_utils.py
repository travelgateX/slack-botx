import json
from time import time
from app.common.util import create_slack_signature,validate_slack_signature
from app.common.config import Config


def test_slack_signature(mock_env_slack):
    timestamp = int(time())
    Config.init_config()
    SLACK_SIGNING_SECRET = Config.get_or_else('SLACK', 'SIGNING_SECRET',None)
    signature = create_slack_signature(SLACK_SIGNING_SECRET, timestamp, "test_data")
    assert True==validate_slack_signature(SLACK_SIGNING_SECRET, "test_data", timestamp, signature )
    assert False==validate_slack_signature(SLACK_SIGNING_SECRET, "test_data_err", timestamp, signature )