import logging
from fastapi import APIRouter,HTTPException
from pydantic import BaseModel,Schema
from app.utils.config import Config

Config.init_config()
logger = logging.getLogger(__name__)
logger.info("events starts")

#https://api.slack.com/types/event 
class SlackEventModel(BaseModel):
   user: str

class SlackEventModelIn(BaseModel):
   #token: str = Schema(...,title="A verification token to validate the event originated from Slack.")
   type: str = Schema(...,title="Indicates which kind of event dispatch this is, usually `event_callback`.")
   challenge: str = Schema(None,title="Slack verification protocol.")
   team_id: str = Schema(None,title="The unique identifier of the workspace where the event occurred.")
   api_app_id: str = Schema(None,title="The unique identifier your installed Slack application.")
   event: SlackEventModel = Schema(None, title="The actual event, an object, that happened. You'll find the most variance in properties beneath this node.")

class SlackChallengeOut(BaseModel):
   challenge:str

class SlackEventOut(BaseModel):
   message:str = "Processed"

router = APIRouter()

@router.post("/slack/events", tags=["events"])
async def post_event(event:SlackEventModelIn):
   logger.info(f"Executing event:[{event}]")
   if event.type == "url_verification": 
      return url_verification(event)
   elif event.type == "team_join":
      return team_join(event)   
   
   raise HTTPException( status_code=405, detail="Event type not allowed")


def url_verification(event:SlackEventModelIn):
   return SlackChallengeOut(**event.dict())


def team_join(event:SlackEventModelIn):
   return SlackEventOut()