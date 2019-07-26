from typing import List
from pydantic import BaseModel,Schema
from enum import Enum, IntEnum


#https://api.slack.com/types/event 
class UserModel(BaseModel):
   id: str
   name: str
   real_name: str


class CommandModelIn(BaseModel):
    command: str
    response_url: str
    text:str = None
    team_id: str = None
    team_domain: str = None
    enterprise_id: str = None
    enterprise_name: str = None
    channel_id: str = None
    channel_name: str = None
    user_id: str = None
    user_name: str = None
    trigger_id: str = None

class AttachmentsModel(BaseModel):
   text: List[str]

class ResponseTypeEnum(str, Enum):
    in_channel = 'in_channel'
    ephemeral = 'ephemeral'

class Text(BaseModel):
   block_type: str = Schema(...,alias='type')
   text: str
   emoji: bool = None
   verbatim: bool =None


class SectionBlock(BaseModel):
   block_type: str = Schema(...,alias='type')
   text: Text
   block_id: str = None

class MessageModelOut(BaseModel):
   text: str = None
   blocks: List[SectionBlock] = None

class CommandModelOut(MessageModelOut):
    response_type: ResponseTypeEnum = None
    text_test: str = None
    replace_original: bool = None
    delete_original: bool = None

class EventModel(BaseModel):
   type: str = Schema(...,title="Indicates which kind of event dispatch this is, usually `event_callback`.")
   user: UserModel = None

class EventModelIn(BaseModel):
   #token: str = Schema(...,title="A verification token to validate the event originated from Slack.")
   type: str = Schema(...,title="Indicates which kind of event dispatch this is, usually `event_callback`.")
   challenge: str = Schema(None,title="Slack verification protocol.")
   team_id: str = Schema(None,title="The unique identifier of the workspace where the event occurred.")
   api_app_id: str = Schema(None,title="The unique identifier your installed Slack application.")
   event: EventModel = Schema(None, title="The actual event, an object, that happened. You'll find the most variance in properties beneath this node.")

class ChallengeModelOut(BaseModel):
   challenge:str
