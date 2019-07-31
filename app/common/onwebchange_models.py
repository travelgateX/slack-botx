from pydantic import BaseModel,Schema


class CallbackPOSTModelIn(BaseModel):
   #token: str = Schema(...,title="A verification token to validate the event originated from Slack.")
   femtoo_callback_url: str
   femtoo_callback_data: str
   femtoo_callback_label: str
