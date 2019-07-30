import hashlib
import hmac
import logging
import json
import slack
import requests
from pydantic import BaseModel
from string import Template
from typing import (List)
import aiofiles
from app.common.config import Config
from fastapi.encoders import jsonable_encoder

Config.init_config()
logger = logging.getLogger(__name__)
logger.info("util start")

class HttpGql:
    def __init__(self,url:str,api_key:str):
        self.URL = url
        self.API_KEY = api_key

    async def query( self, query:str)->json:
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Apikey {self.API_KEY}"
                  }
        logger.info(f"url:{self.URL}, apikey:{self.API_KEY}, query:{query}")
        response = requests.post(url=self.URL, data=query, headers=headers)
        response.raise_for_status()  
        return response.json()

def get_slack_task_block(self,text, information):
    return [
        {"type": "section", "text": {"type": "mrkdwn", "text": text}},
        {"type": "context", "elements": [{"type": "mrkdwn", "text": information}]},
    ]    


async def get_message_blocks_payload(messages_file_names:List[str], substitutions:dict={}) -> List[str]:
    blocks = [] 
    for resource_name in messages_file_names:
        file_name = 'contrib/resources/slack-messages/' + resource_name + '.json'
        logger.info(f"Reading file_name {file_name}")
        async with aiofiles.open(file_name, mode='r', encoding='utf-8') as f:
            file_str = await f.read()
            str_template = Template(file_str)
            file_str = str_template.safe_substitute(substitutions)
            json_blocks = json.loads( file_str)

        for block in json_blocks:
            blocks.append( block ) 
    return blocks


async def send_slack_message(web_client, channel:str, as_user:bool, blocks:List[str]):
    try:
        response = await web_client.chat_postMessage(
                channel=channel, 
                blocks = blocks,
                as_user = as_user
                )
        logger.info(f"slack response {response}")
        return response
    except slack.errors.SlackApiError as err:
            logger.error(f"Exception SlackApiError [{err}]")
            raise

async def format_graphql_query(resource_name:str, substitutions:dict={}):
    file_name= 'contrib/resources/graphql/queries/' + resource_name + '.graphql'
    logger.info(f"Reading file_name {file_name}")
    async with aiofiles.open(file_name, mode='r', encoding='utf-8') as f:
        file_str = await f.read()
        str_template = Template(file_str)
        file_str = str_template.safe_substitute(substitutions)

    #Remove white characters, tabs... and escape " in variables
    file_str = file_str.replace("\t"," ").replace("\r"," ").replace("\n"," ").replace('"','\\"')
    
    #Graphql Query starts with query
    return """{\"query\":\"""" + file_str + """\"}"""

def send_slack_post_model( url:str, data_model:BaseModel)->json:
    return send_slack_post_json(url=url, data_json=jsonable_encoder(data_model, include_none=False))

def send_slack_post_json( url:str, data_json:json)->json:
    headers = {"Content-type": "application/json"}
    try:
        logger.debug(f"requests url:[{url}], data:[{data_json}]")
        response = requests.post(url=url, data=data_json, headers=headers)
        response.raise_for_status() 
        return response.json()
    except requests.exceptions.HTTPError as err:
        logger.error(f"Slack post error {err}")
        logger.error(f"Err text { err.response.text}")
        raise
     
   

"""
    Slack creates a unique string for your app and shares it with you. Verify
    requests from Slack with confidence by verifying signatures using your
    signing secret.
    On each HTTP request that Slack sends, we add an X-Slack-Signature HTTP
    header. The signature is created by combining the signing secret with the
    body of the request we're sending using a standard HMAC-SHA256 keyed hash.
    https://api.slack.com/docs/verifying-requests-from-slack#how_to_make_a_request_signature_in_4_easy_steps__an_overview
    Args:
        signing_secret: Your application's signing secret, available in the
            Slack API dashboard
        data: The raw body of the incoming request - no headers, just the body.
        timestamp: from the 'X-Slack-Request-Timestamp' header
        signature: from the 'X-Slack-Signature' header - the calculated signature
            should match this.
    Returns:
        True if signatures matches
"""
   
def create_slack_signature(secret:str, timestamp, data)->str:
    req = str.encode('v0:' + str(timestamp) + ':') + str.encode(data)
    request_signature= 'v0='+hmac.new(
        str.encode(secret),
        req, hashlib.sha256
    ).hexdigest()
   
    return request_signature

def validate_slack_signature(signing_secret: str, data: str, timestamp: str, signature: str) -> bool:
    format_req = str.encode(f"v0:{timestamp}:{data}")
    encoded_secret = str.encode(signing_secret)
    request_hash = hmac.new(encoded_secret, format_req, hashlib.sha256).hexdigest()
    calculated_signature = f"v0={request_hash}"
    
    return hmac.compare_digest(calculated_signature, signature)

def validate_github_signature(signing_secret: str, data: str,signature: str) -> bool:
   format_req = str.encode(data)
   request_hash = hmac.new(signing_secret, format_req, hashlib.sha1).hexdigest()
   return hmac.compare_digest(request_hash,signature )