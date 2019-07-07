import logging
from fastapi import BackgroundTasks,APIRouter,HTTPException
from pydantic import BaseModel,Schema
from app.common.config import Config
from app.common.slack_models import EventModelIn, ChallengeModelOut, EventModelOut
from app.tasks.slack_tasks import Event

Config.init_config()
logger = logging.getLogger(__name__)
logger.info("events start")

router = APIRouter()

@router.post("/slack/events", tags=["events"])
async def post_event(event:EventModelIn, background_tasks: BackgroundTasks):
   logger.info(f"Executing event:[{event}]")
   if event.type == "url_verification": 
      return ChallengeModelOut(**event.dict())
   else:  #Other eventa are executed events in background 
     event = Event(event) 
     background_tasks.add_task( event.execute )
     return EventModelOut()
     # event = Event(event)
     # return event.execute()   
   