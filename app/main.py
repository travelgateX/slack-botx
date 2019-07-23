import json
import logging
import hashlib
import hmac
import json
from time import time

from fastapi import Depends, FastAPI, Header, HTTPException

from starlette.requests import Request
from starlette.responses import JSONResponse

from app.routers import (slack_events, onwebchange_webhooks,slack_commands)
from app.common.util import validate_slack_signature, validate_github_signature
from app.common.config import Config


Config.init_config()
logger = logging.getLogger(__name__)
logger.info("main start")

async def log_request(request: Request):
   for header in request.headers:
      logger.info(f"Request header:[{header}]:[{request.headers[header]}]")   
   body = await request.body()
   data_str = body.decode()
   logger.info(f"Request body:[{data_str}]")
 
async def is_valid_slack_signature(request: Request):
   logger.info("Validating slack signature...")

   # Each request comes with request timestamp and request signature
   # emit an error if the timestamp is out of range
   req_timestamp = request.headers.get('X-Slack-Request-Timestamp')
   if ( (not req_timestamp) or (abs(time() - int(req_timestamp)) > 60 * 5) ):
      logger.error("Bad X-Slack-Request-Timestamp")
      raise HTTPException( status_code=403, detail="Request header X-Slack-Request-Timestamp out of range")

   req_signature = request.headers.get('X-Slack-Signature')
   if (not req_signature):
      logger.error("Bad X-Slack-Signature")
      raise HTTPException( status_code=403, detail="Bad X-Slack-Signature")

   body = await request.body()
   data_str = body.decode()
   SLACK_SIGNING_SECRET = Config.get_or_else('SLACK','SIGNING_SECRET',None)
   signature_ok = validate_slack_signature( signing_secret=SLACK_SIGNING_SECRET, data=data_str, timestamp=req_timestamp, signature=req_signature) 
   logger.debug(f"validate signature data: [{data_str}], signature_ok:[{signature_ok}]")
   if (not signature_ok):
      logger.error("Bad request signature")
      raise HTTPException( status_code=403, detail="Bad request signature")
    

app = FastAPI()

app.include_router(
   slack_events.router,
   tags=["slack","events"],
   dependencies=[Depends(is_valid_slack_signature)]
)

# Pending to validate signature ad dependency. https://github.com/encode/starlette/issues/495#issuecomment-494008175
app.include_router(
   slack_commands.router,
   tags=["slack_test","commands_test"],
   dependencies=[]
)

app.include_router(
   onwebchange_webhooks.router,
   tags=["onwebchange","webhook"],
   dependencies=[],
)
