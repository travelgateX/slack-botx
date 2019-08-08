import logging
import time
from fastapi import BackgroundTasks,APIRouter,HTTPException
from pydantic import BaseModel,Schema
from app.common.config import Config
from app.common.models import EventModelOut
from app.common.slack_models import EventModelIn, ChallengeModelOut
from app.tasks.factory import Macro, event_factory
from app.common.prometheus import TASKS_REQUESTS

Config.init_config()
logger = logging.getLogger(__name__)
logger.info("slack events start")

router = APIRouter()

@router.post("/slack/events", tags=["slack","events"])
async def post_event(event:EventModelIn, background_tasks: BackgroundTasks):
   logger.info(f"POST event:[{event.type}]")
   
   
   if event.type == "url_verification": 
      #Prometheus metric
      TASKS_REQUESTS.labels(type="event", name=event.type).inc()
      return ChallengeModelOut(**event.dict())
   else:  #Other events are executed in background 
     #Prometheus metric
     TASKS_REQUESTS.labels(type="event", name=event.event.type).inc()

     macro = Macro()
     macro.add(  event_factory(event.event.type, event) )
     background_tasks.add_task( macro.run )
     return EventModelOut()
   