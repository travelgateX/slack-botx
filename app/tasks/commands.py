import logging
import os
import slack
import time
from datetime import datetime
import aiofiles
import requests
import aiohttp
import sys
import json
from string import Template
from typing import (List)
from pydantic import BaseModel
from app.common.slack_models import EventModelIn,CommandModelIn,CommandModelOut
from app.common.config import Config

Config.init_config()
logger = logging.getLogger(__name__)
logger.info("commands start")

class Http:
    async def __aenter__(self):
        self._session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, *err):
        await self._session.close()
        self._session = None

    async def post(self, url,data):
        async with self._session.get(url, data=data) as resp:
            if "https://test.com" not in url: 
                resp.raise_for_status()
            return await resp.read()

class Command:
    
    def __init__(self,event:BaseModel):
        logger.info("Command init")
        self.event_in=event
        self.CHANNEL_TGX_ANNOUNCEMENTS = Config.get_or_else('SLACK', 'CHANNEL_TGX_ANNOUNCEMENTS',None)
        self.CHANNEL_ALL_ANNOUNCEMENTS = Config.get_or_else('SLACK', 'CHANNEL_ALL_ANNOUNCEMENTS',None)
        self.web_client = slack.WebClient(token=Config.get_or_else('SLACK', 'BOT_TOKEN',None), run_async=True)

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
            logger.info(f"slack response {response}")
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
            logger.info(f"Channel announcements TGX:[{self.CHANNEL_TGX_ANNOUNCEMENTS}], ALL:[{self.CHANNEL_ALL_ANNOUNCEMENTS}]")
            response = await self.send_message( channel=self.CHANNEL_TGX_ANNOUNCEMENTS, as_user=True, blocks=blocks)
            logger.info(f"ChangelogNotify: OK[{response}]")
        else:
            logger.info(f"ChangelogNotify: not changes to notify")

class AlertsX(Command):
    async def execute(self):
        command_in : CommandModelIn = self.event_in
        logger.info(f"AlertsX.execute[{command_in}]")
        command_out = CommandModelOut(text="Hello world")
        data = command_out.dict()
        async with Http() as http:
            response = await http.post(url = command_in.response_url, data = data)
        logger.info(f"AlertsX execution OK [{response}]")

class NonImplementedCommand(Command):
    async def execute(self):
       logger.warning(f"Command non implemented {self.event_in}")

