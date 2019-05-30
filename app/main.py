import json
import slack
from config import Config
from slash_command import *
from fastapi import FastAPI


Config.init_config()
SLACK_API_TOKEN = Config.get_or_else('SLACK','SLACK_API_TOKEN',None)
SLACK_VERIFICATION_TOKEN = Config.get_or_else('SLACK','SLACK_VERIFICATION_TOKEN',None)
slack_client = slack.WebClient(SLACK_API_TOKEN)


commander = SlashCommand("Hey there! It works.")

#TODO: Add checks for all responses from slack api calls

def verify_slack_token(request_token):
    if SLACK_VERIFICATION_TOKEN != request_token:
        print("Error: invalid verification token!")
        print("Received {} but was expecting {}".format(request_token, SLACK_VERIFICATION_TOKEN))
        return {"Request contains invalid Slack verification token", 403}

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/slack/test")
async def command(info):
   # # get uid of the user
  # im_id = slack_client.api_call(
  #   "im.open",
  #   user=info["user_id"]
  # )["channel"]["id"]

  # # send user a response via DM
  # ownerMsg = slack_client.api_call(
  #   "chat.postMessage",
  #   channel=im_id,
  #   text=commander.getMessage()

  # send channel a response
  channelMsg = slack_client.chat_postMessage(
    channel="#" + info["channel_name"],
    text=commander.getMessage )

  return {"message": "Hello World"}