from app.tasks.base_tasks import Command
from app.common.slack_models import CommandModelIn, CommandModelOut 
from fastapi.encoders import jsonable_encoder
import app.common.util
import argparse
import json

class Task(Command):
    async def execute(self):
        command_in : CommandModelIn = self.event_in
        self.logger.info(f"AlertsX.execute[{command_in}]")
        
        #get all suppliers
        gql_query = await app.common.util.format_graphql_query( "suppliers_all")
        response_json = await self.http_gql_client.query(  gql_query )
        self.logger.info(f"gql_response [{response_json}]")
        suppliers_all =[]
        for edges in response_json['data']['admin']['suppliers']['edges']:
            for supplier_data in edges['node']['supplierData']:
                suppliers_all.append(supplier_data)
        
        #get alerts status
        gql_query = await app.common.util.format_graphql_query( "alertsx_status", {'criteria_group':"platform-alerts"})
        response_json = await self.http_gql_client.query(  gql_query )
        self.logger.info(f"gql_response [{response_json}]")

        #create the response message
        suppliers_alerts_err = []
        for edges in response_json['data']['alertsX']['alerts']['edges']:
            for node_edges in edges['node']['alertData']['events']['edges']:
                event_data = node_edges['node']['eventData']
                if event_data['status'] != "OK":
                    suppliers_alerts_err.append(event_data['groupBy']) 

        count_ok = len(suppliers_all) - len(suppliers_alerts_err)
        count_err = len(suppliers_alerts_err)

        blocks = await app.common.util.get_message_blocks_payload( ["alertsx_status"], {'count_ok': count_ok, 'count_err': count_err} )
        self.logger.info(f"blocks:[{command_in.response_url}][{blocks}]")
        
        out =  CommandModelOut( response_type='in_channel', replace_original=True )
        out.blocks = blocks
        self.logger.info(f"out json:[{jsonable_encoder(out)}]")
        #response to slack
        #https://api.slack.com/reference/messaging/payload
        response = app.common.util.send_slack_post_model(url = command_in.response_url, data_model = out)
        self.logger.info(f"AlertsX execution OK [{response}]")

    async def needs_help(self)->bool:
        parser = argparse.ArgumentParser()
        parser.add_argument("status")
        parser.add_argument("help")
        args = parser.parse_args( self.event_in.text )
        if (args.help):
            return True
        if not (args.status):
            return True
        return False

    
