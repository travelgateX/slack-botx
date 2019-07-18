import logging
from fastapi import BackgroundTasks,APIRouter,HTTPException,Form
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
async def post_event(*, femtoo_callback_url: str = Form(...), femtoo_callback_data: str = Form(...), femtoo_callback_label: str = Form(...),background_tasks: BackgroundTasks):
   callback = CallbackPOSTModelIn( femtoo_callback_url=femtoo_callback_url,femtoo_callback_data=femtoo_callback_data,femtoo_callback_label=femtoo_callback_label) 
   logger.info(f"OnWebChange webhook:[{callback}]")
   macro = Macro()
   macro.add(  factory("onwebchange_callback", callback) )
   background_tasks.add_task( macro.run )
   return EventModelOut()