from pydantic import BaseModel,Schema

#https://api.slack.com/types/event 
class UserModel(BaseModel):
   id: str
   name: str
   real_name: str

class EventModel(BaseModel):
   type: str = Schema(...,title="Indicates which kind of event dispatch this is, usually `event_callback`.")
   user: UserModel = None

class EventModelIn(BaseModel):
   #token: str = Schema(...,title="A verification token to validate the event originated from Slack.")
   type: str = Schema(...,title="Indicates which kind of event dispatch this is, usually `event_callback`.")
   challenge: str = Schema(None,title="Slack verification protocol.")
   team_id: str = Schema(None,title="The unique identifier of the workspace where the event occurred.")
   api_app_id: str = Schema(None,title="The unique identifier your installed Slack application.")
   event: EventModel = Schema(None, title="The actual event, an object, that happened. You'll find the most variance in properties beneath this node.")

class ChallengeModelOut(BaseModel):
   challenge:str
