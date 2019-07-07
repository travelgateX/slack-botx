from app.common.slack_models import EventModelIn, EventModelOut

class Event:
   def __init__(self, event_model_in:EventModelIn):
      self.event_model_in = event_model_in

   async def execute(self):
      raise NotImplementedError("The method not implemented")
