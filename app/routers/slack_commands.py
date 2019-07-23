import logging
import urllib.parse
from fastapi import BackgroundTasks,APIRouter,HTTPException,Form
from pydantic import BaseModel,Schema
from app.common.config import Config
from app.common.models import EventModelOut
from app.common.slack_models import CommandModelIn, CommandModelOut
from app.tasks.commands_factory import Macro, Command, factory

Config.init_config()
logger = logging.getLogger(__name__)
logger.info("slack commands start")

router = APIRouter()

#https://api.slack.com/slash-commands#best_practices
@router.post("/slack/commands", tags=["slack","commands"])
async def post_event(*, command: str = Form(...), response_url: str = Form(...), background_tasks: BackgroundTasks):
   logger.info(f"POST Slack")
   command_model = CommandModelIn( command=urllib.parse.unquote(command), response_url=urllib.parse.unquote( response_url ) ) 
   logger.info(f"Slack commands:[{command_model}]")
   if command_model.command == "/insightsx": 
      return CommandModelOut(text="Command received")
   else:  #Other comevents are executed in background 
     logger.warning(f"Command not implemented:[{command_model.command}]")
     #macro = Macro()
     #macro.add(  factory(event.event.type, event) )
     #background_tasks.add_task( macro.run )
     return CommandModelOut(**command_model.dict())
