from app.tasks.base_tasks import Event
import app.common.util
import time
from datetime import datetime

class Task(Event):
    async def execute(self):
        self.logger.info(f"ChangelogNotify.execute[{self.event_in}]")
        
        #Only notify on today changes
        today = datetime.today().strftime('%Y-%m-%d')
        if today in self.event_in.femtoo_callback_data:
            # Get the onboarding message payload
            blocks = await app.common.util.get_message_blocks_payload( ["changelog"], {'app': self.event_in.femtoo_callback_label, 'url': self.event_in.femtoo_callback_url} )
            # Post the onboarding message in Slack member channel
            self.logger.info(f"Channel announcements TGX:[{self.CHANNEL_TGX_ANNOUNCEMENTS}], ALL:[{self.CHANNEL_ALL_ANNOUNCEMENTS}]")
            response = await app.common.util.send_slack_message( web_client=self.web_client, channel=self.CHANNEL_TGX_ANNOUNCEMENTS, as_user=True, blocks=blocks)
            self.logger.info(f"ChangelogNotify: OK[{response}]")
        else:
            self.logger.info(f"ChangelogNotify: not changes to notify")