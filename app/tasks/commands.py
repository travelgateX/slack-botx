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
import app.common.util
from app.common.config import Config
from app.common.util import HttpGql

Config.init_config()
logger = logging.getLogger(__name__)
logger.info("commands start")

class Command:
    
    def __init__(self,event:BaseModel):
        logger.info("Command init")
        self.event_in=event
        self.CHANNEL_TGX_ANNOUNCEMENTS = Config.get_or_else('SLACK', 'CHANNEL_TGX_ANNOUNCEMENTS',None)
        self.CHANNEL_ALL_ANNOUNCEMENTS = Config.get_or_else('SLACK', 'CHANNEL_ALL_ANNOUNCEMENTS',None)
        self.web_client = slack.WebClient(token=Config.get_or_else('SLACK', 'BOT_TOKEN',None), run_async=True)
        self.http_gql_client = HttpGql(url=Config.get_or_else('TRAVELGATEX', 'GRAPHQL_API_URL',None), api_key=Config.get_or_else('TRAVELGATEX', 'GRAPHQL_API_KEY',None))

    async def execute(self): pass
   

# Commands
class TeamJoin(Command):
    async def execute(self):
        logger.info(f"TeamJoin.execute[{self.event_in}]")
        # Get the onboarding message payload
        blocks = await app.common.util.get_message_payload( ["onboarding"], {'user_real_name': self.event_in.event.user.real_name} )
        # Post the onboarding message in Slack member channel
        response = await app.common.util.send_slack_message(  web_client=self.web_client, channel=self.event_in.event.user.id,  as_user=True, blocks=blocks)
        logger.info(f"TeamJoin execution OK [{response}]")

class ChangelogNotify(Command):
    async def execute(self):
        logger.info(f"ChangelogNotify.execute[{self.event_in}]")
        
        #Only notify on today changes
        today = datetime.today().strftime('%Y-%m-%d')
        if today in self.event_in.femtoo_callback_data:
            # Get the onboarding message payload
            blocks = await app.common.util.get_message_payload( ["changelog"], {'app': self.event_in.femtoo_callback_label, 'url': self.event_in.femtoo_callback_url} )
            # Post the onboarding message in Slack member channel
            logger.info(f"Channel announcements TGX:[{self.CHANNEL_TGX_ANNOUNCEMENTS}], ALL:[{self.CHANNEL_ALL_ANNOUNCEMENTS}]")
            response = await app.common.util.send_slack_message( web_client=self.web_client, channel=self.CHANNEL_TGX_ANNOUNCEMENTS, as_user=True, blocks=blocks)
            logger.info(f"ChangelogNotify: OK[{response}]")
        else:
            logger.info(f"ChangelogNotify: not changes to notify")

class AlertsX(Command):
    async def execute(self):
        command_in : CommandModelIn = self.event_in
        logger.info(f"AlertsX.execute[{command_in}]")
        
        #get alerts status
        gql_query = await app.common.util.format_graphql_query( "alertsx_status", {'criteria_group':"easework-admin"})
        response_json = await self.http_gql_client.query(  gql_query )
        logger.info(f"gql_response [{response_json}]")

        #create the response message
        count_ok:int = 0
        count_err:int = 0
        suppliers_alerts = []
        for edges in response_json['data']['alertsX']['alerts']['edges']:
            for node_edges in edges['node']['alertData']['events']['edges']:
                event_data = node_edges['node']['eventData']
                if event_data['status'] == "OK":
                    count_ok += 1
                else:
                    count_err += 1
                    suppliers_alerts.append(event_data['groupBy']) 
        blocks = await app.common.util.get_message_payload( ["alertsx_status"], {'count_ok': count_ok, 'count_err': count_err} )
        
        #response to slack
        response = app.common.util.send_slack_post(url = command_in.response_url, data = blocks)
        logger.info(f"AlertsX execution OK [{response}]")


class NonImplementedCommand(Command):
    async def execute(self):
       logger.warning(f"Command non implemented {self.event_in}")

