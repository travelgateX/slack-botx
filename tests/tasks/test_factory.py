from app.tasks.factory import event_factory, command_factory
from app.common.config import Config

def test_event_teams_join(mock_env_slack):
    ret = event_factory("team_join",None)
    assert ret != None

def test_command_alertsx(mock_env_slack):
    ret = command_factory("alertsx",None)
    assert ret != None