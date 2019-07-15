from pydantic import BaseModel

class EventModelOut(BaseModel):
   message:str = "Background task added"