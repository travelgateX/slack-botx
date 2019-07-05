import logging

from fastapi import APIRouter,HTTPException
from pydantic import BaseModel,Schema
from app.utils.config import Config

Config.init_config()
logger = logging.getLogger(__name__)
logger.info("events starts")

#https://api.slack.com/types/event 
class SlackEventModelIn(BaseModel):
   #token: str = Schema(...,title="A verification token to validate the event originated from Slack.")
   challenge: str = Schema(None,title="Slack verification protocol.")
   team_id: str = Schema(...,title="The unique identifier of the workspace where the event occurred.")
   api_app_id: str = Schema(...,title="The unique identifier your installed Slack application.")
   type: str = Schema(...,title="Indicates which kind of event dispatch this is, usually `event_callback`.")

class SlackChallengeOut(BaseModel):
   challenge:str

router = APIRouter()

@router.post("/slack/events", tags=["events"])
async def post_event(event:SlackEventModelIn):
   if event.type == "url_verification": 
         url_verification(event)
      
   raise HTTPException( status_code=405, detail="Event type not allowed")

def url_verification(event:SlackEventModelIn):
   return SlackChallengeOut(**event.dict())