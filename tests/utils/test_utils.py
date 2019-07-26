import pytest
import json
from time import time
import app.common.util
from fastapi.encoders import jsonable_encoder
from app.common.util import create_slack_signature,validate_slack_signature
from app.common.config import Config
from app.common.slack_models import CommandModelOut, MessageModelOut

def test_slack_signature(mock_env_slack):
    timestamp = int(time())
    Config.init_config()
    SLACK_SIGNING_SECRET = Config.get_or_else('SLACK', 'SIGNING_SECRET',None)
    signature = create_slack_signature(SLACK_SIGNING_SECRET, timestamp, "test_data")
    assert True==validate_slack_signature(SLACK_SIGNING_SECRET, "test_data", timestamp, signature )
    assert False==validate_slack_signature(SLACK_SIGNING_SECRET, "test_data_err", timestamp, signature )

# notice our test uses the custom fixture instead of monkeypatch directly
def test_slack_post():
    data = {"key":"value"}
    response = app.common.util.send_slack_post_json(url="dddddddd.es", data_json=data)
    assert response == data

@pytest.mark.asyncio
async def test_command_model_out_json():
      blocks = await app.common.util.get_message_blocks_payload( ["onboarding"], {'user_real_name': 'test_name'} )
      out =  CommandModelOut( response_type='in_channel', replace_original=True, blocks= blocks )
      json_out = jsonable_encoder(out)
      print(f"json_out:[{json_out}]")
      assert json_out != None
      assert json_out["replace_original"]       