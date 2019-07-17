import logging
from fastapi import BackgroundTasks,APIRouter,HTTPException
from pydantic import BaseModel,Schema
from app.common.models import EventModelOut
from app.common.onwebchange_models import CallbackPOSTModelIn
from app.common.config import Config
from app.tasks.commands_factory import Macro, Command, factory

Config.init_config()
logger = logging.getLogger(__name__)
logger.info("OnWebChange webhooks start")

router = APIRouter()
              
@router.post("/onwebchange/webhook", tags=["onwebchange", "webhook"])
#async def post_event(callback:CallbackPOSTModelIn, background_tasks: BackgroundTasks):
async def post_event(background_tasks: BackgroundTasks):
   callback = CallbackPOSTModelIn 
   logger.info(f"OnWebChange webhook:[{callback}]")
   macro = Macro()
   macro.add(  factory("onwebchange_callback", callback) )
   background_tasks.add_task( macro.run )
   return EventModelOut()