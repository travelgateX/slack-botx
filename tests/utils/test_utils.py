import pytest
import json
from time import time
import app.common.util
from fastapi.encoders import jsonable_encoder
from app.common.util import create_slack_signature,validate_slack_signature
from app.common.config import Config
from app.common.slack_models import CommandModelOut, MessageModelOut,SectionBlock,MessageModelOut 

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
    out =  CommandModelOut( type='in_channel', replace_original=True)
    assert out != None
    blocks = await app.common.util.get_message_blocks_payload( ["alertsx_status"], {'count_ok': 100, 'count_err': 1} )
    block_list = []
    for block in blocks:
        #section_block = json.loads(block)
        block_list.append( block )
    out.blocks = block_list
    assert out != None
    assert len(out.blocks) == 4
    out.blocks = blocks
    assert out != None
    assert len(out.blocks) == 4
    out_json = jsonable_encoder( out, include_none=False)
    print(out_json)
    assert out_json['replace_original'] == True
    assert 'delete_original' not in out_json
    
    