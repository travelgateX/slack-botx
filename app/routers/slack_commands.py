import logging
import urllib.parse
from fastapi import BackgroundTasks,APIRouter,HTTPException,Form
from pydantic import BaseModel,Schema
from app.common.config import Config
from app.common.models import EventModelOut
from app.common.slack_models import CommandModelIn, CommandModelOut
from app.tasks.factory import Macro,command_factory
from app.tasks.base_tasks import Task,Command

Config.init_config()
logger = logging.getLogger(__name__)
logger.info("slack commands start")

router = APIRouter()

#https://api.slack.com/slash-commands#best_practices
@router.post("/slack/commands", tags=["slack","commands"])
async def post_event(*, command: str = Form(...), response_url: str = Form(...), text: str = Form(None), background_tasks: BackgroundTasks):
   command_model = CommandModelIn( command=command, response_url=response_url, text=text ) 
   logger.info(f"Slack commands:[{command_model}]")
   #Standarize command name to task name
   command_name = command_model.command[1:]
   #Check if commands need help
   command:Command = command_factory(command_name, command_model)

   #Add background task
   macro = Macro()
   macro.add( command )
   background_tasks.add_task( macro.run )
   
   #Immediate response
   return CommandModelOut(text="Command is being processed in background.",text_test=text)
   