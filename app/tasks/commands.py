import logging
import os
import slack
import time
from datetime import datetime
import aiofiles
import sys
import json
from string import Template
from typing import (List)
from pydantic import BaseModel
from app.common.slack_models import EventModelIn
from app.common.config import Config

Config.init_config()
logger = logging.getLogger(__name__)
logger.info("commands start")

class Command:
    SLACK_CHANNEL_ANNOUNCEMENTS = Config.get_or_else('SLACK', 'CHANNEL_ANNOUNCEMENTS',None)
    logger.info(f"Channel announcements [{SLACK_CHANNEL_ANNOUNCEMENTS}]")
    web_client = slack.WebClient(token=Config.get_or_else('SLACK', 'BOT_TOKEN',None), run_async=True)

    def __init__(self,event:BaseModel):
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
               json_blocks = json.loads( file_str)

            for block in json_blocks:
                blocks.append( block ) 
        return blocks
    
    async def send_message(self, channel:str, as_user:bool, blocks:List[str]):
        try:
            response = await self.web_client.chat_postMessage(
                    channel=channel, 
                    blocks = blocks,
                    as_user = as_user
                    )
            logger.info(f"response {response}")
            return response
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
        response = await self.send_message( channel=self.event_in.event.user.id,  as_user=True, blocks=blocks)
        
        logger.info(f"TeamJoin execution OK [{response}]")

class ChangelogNotify(Command):
    async def execute(self):
        logger.info(f"ChangelogNotify.execute[{self.event_in}]")
        
        #Only notify on today changes
        today = datetime.today().strftime('%Y-%m-%d')
        if today in self.event_in.femtoo_callback_data:
            # Get the onboarding message payload
            blocks = await self.get_message_payload( ["changelog"], {'app': self.event_in.femtoo_callback_label, 'url': self.event_in.femtoo_callback_url} )
            # Post the onboarding message in Slack member channel
            response = await self.send_message( channel=self.SLACK_CHANNEL_ANNOUNCEMENTS, as_user=True, blocks=blocks)
            logger.info(f"ChangelogNotify OK[{response}]")
        else:
            logger.info(f"ChangelogNotify not changes for today [{response}]")

class NonImplementedCommand(Command):
    async def execute(self):
       logger.warning(f"Command non implemented {self.event_in}")

