from app.common.slack_models import EventModelIn
from app.tasks.commands import (Command, TeamJoin, NonImplementedCommand)

# Command pattern: https://python-3-patterns-idioms-test.readthedocs.io/en/latest/FunctionObjects.html
# An object that holds commands:
class Macro:
    def __init__(self):
        self.commands = []
    def add(self, command:Command):
        self.commands.append(command)
    def run(self):
        for c in self.commands:
            c.execute()

# Create based on class name:
def factory(event:EventModelIn) -> Command:
    if event.type == "team_join": return TeamJoin(event)
    else: return NonImplementedCommand(event)
