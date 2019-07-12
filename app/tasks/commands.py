import logging
import os
import slack
import time
import aiofiles
import sys
import json
from string import Template
from typing import (List)
from app.common.slack_models import EventModelIn
from app.common.config import Config

Config.init_config()
logger = logging.getLogger(__name__)
logger.info("commands start")

class Command:

    web_client = slack.WebClient(token=Config.get_or_else('SLACK', 'BOT_TOKEN',None), run_async=True)

    def __init__(self,event:EventModelIn):
        self.event_in=event

    async def execute(self): pass

    async def get_message_payload(self, messages_file_names:List[str], substitutions:dict={}) -> List[str]:
        blocks = []
        for resource_name in messages_file_names:
            file_name = 'resources/slack-messages/' + resource_name + '.json'
            logger.info(f"Reading file_name {file_name}")
            async with aiofiles.open(file_name, mode='r', encoding='utf-8') as f:
               file_str = await f.read()
               str_template = Template(file_str)
               file_str = str_template.safe_substitute(substitutions)
               #file_str.format(**substitutions)
               json_blocks = json.loads( file_str)

            for block in json_blocks:
                blocks.append( block ) 
        return blocks
    
    async def send_message(self, channel:str, blocks:List[str]):
        try:
            response = await self.web_client.chat_postMessage(
                    channel=channel, 
                    blocks = blocks
                    )
            logger.info(f"response {response}")
        except slack.errors.SlackApiError as err:
             logger.error(f"Exception SlackApiError [{err}]")
             raise


    def _get_task_block(self,text, information):
        return [
            {"type": "section", "text": {"type": "mrkdwn", "text": text}},
            {"type": "context", "elements": [{"type": "mrkdwn", "text": information}]},
        ]    

# Commands
class TeamJoin(Command):
    async def execute(self):
        logger.info(f"TeamJoin.execute[{self.event_in}]")
        
        # Get the onboarding message payload
        blocks = await self.get_message_payload( ["onboarding"], {'user_real_name': self.event_in.event.user.real_name} )

        # Post the onboarding message in Slack member channel
        response = await self.send_message( channel=self.event_in.event.user.id, blocks=blocks)
        
        logger.info(f"postMessageResponse[{response}]")


class NonImplementedCommand(Command):
    async def execute(self):
       logger.warn(f"Command non implemented {self.event_in}")

