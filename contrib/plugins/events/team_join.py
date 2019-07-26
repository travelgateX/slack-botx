from app.tasks.base_tasks import Event
import app.common.util

# Commands
class Task(Event):
    async def execute(self):
        self.logger.info(f"TeamJoin.execute[{self.event_in}]")
        # Get the onboarding message payload
        blocks = await app.common.util.get_message_blocks_payload( ["onboarding"], {'user_real_name': self.event_in.event.user.real_name} )
        # Post the onboarding message in Slack member channel
        response = await app.common.util.send_slack_message(  web_client=self.web_client, channel=self.event_in.event.user.id,  as_user=True, blocks=blocks)
        self.logger.info(f"TeamJoin execution OK [{response}]")