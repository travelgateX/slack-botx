import logging
import os
import slack
from app.common.slack_models import EventModelIn
from app.common.config import Config

Config.init_config()
logger = logging.getLogger(__name__)
logger.info("commands start")

class Command:

    web_client = slack.WebClient(token=Config.get_or_else('SLACK', 'BOT_TOKEN',None),run_async=True)

    def __init__(self,event:EventModelIn):
        self.event_model_in=event
      
    async def execute(self): pass

# Commands
class TeamJoin(Command):
    async def execute(self):
       logger.info(f"TeamJoin.execute[{self.event_model_in}]")
       await self._onboarding_message()

    async def _onboarding_message(self):
        """Create and send an onboarding welcome message to new users. 
        """
        logger.info("OnBoarding")

   
class NonImplementedCommand(Command):
    async def execute(self):
       logger.warn(f"Command non implemented {self.event_model_in}")

