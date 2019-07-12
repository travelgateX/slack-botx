import logging
import time
from fastapi import BackgroundTasks,APIRouter,HTTPException
from pydantic import BaseModel,Schema
from app.common.config import Config
from app.common.slack_models import EventModelIn, ChallengeModelOut, EventModelOut
from app.tasks.slack_commands import Macro, Command, factory

Config.init_config()
logger = logging.getLogger(__name__)
logger.info("events start")

router = APIRouter()

@router.post("/slack/events", tags=["events"])
async def post_event(event:EventModelIn, background_tasks: BackgroundTasks):
   logger.info(f"POST event:[{event.type}]")
   if event.type == "url_verification": 
      return ChallengeModelOut(**event.dict())
   else:  #Other events are executed in background 
     macro = Macro()
     macro.add(  factory(event) )
     background_tasks.add_task( macro.run )
     return EventModelOut()
   