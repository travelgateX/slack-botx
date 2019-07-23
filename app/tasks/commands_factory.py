from app.common.slack_models import BaseModel
from app.tasks.commands import (Command, TeamJoin, ChangelogNotify, AlertsX,NonImplementedCommand)

# Command pattern: https://python-3-patterns-idioms-test.readthedocs.io/en/latest/FunctionObjects.html
# An object that holds commands:
class Macro:
    def __init__(self):
        self.commands = []
    def add(self, command:Command):
        self.commands.append(command)
    async def run(self):
        for c in self.commands:
            await c.execute()

# Create based on class name:
def factory(callback_type:str, data:BaseModel) -> Command:
    if callback_type == "team_join": return TeamJoin(data)
    if callback_type == "/alertsx": return AlertsX(data)
    if callback_type == "onwebchange_callback": return ChangelogNotify(data)
    else: return NonImplementedCommand(data)
