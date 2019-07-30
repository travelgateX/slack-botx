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
        #self.logger.info(f"gql_response suppliers [{response_json}]")
        suppliers_all =[]
        for edges in response_json['data']['admin']['suppliers']['edges']:
            for supplier_data in edges['node']['supplierData']:
                suppliers_all.append(supplier_data)
        
        #get alerts status
        gql_query = await app.common.util.format_graphql_query( "alertsx_status", {'criteria_group':"platform-alerts"})
        response_json = await self.http_gql_client.query(  gql_query )
        self.logger.info(f"gql_response alerts [{response_json}]")

        #create the response message
        suppliers_alerts_err = []
        suppliers_alerts_timeout = []
        for edges in response_json['data']['alertsX']['alerts']['edges']:
            for node_edges in edges['node']['alertData']['events']['edges']:
                alert_code = edges['node']['code']
                event_data = node_edges['node']['eventData']
                if event_data['status'] != "OK":
                    if alert_code == "ALT_216":
                        suppliers_alerts_err.append(event_data['groupBy']) 
                    if alert_code == "ALT_217":
                        suppliers_alerts_timeout.append(event_data['groupBy']) 

        len_suppliers_all =  len(suppliers_all)
        len_suppliers_alerts_err =  len(suppliers_alerts_err)
        len_suppliers_alerts_timeout =  len(suppliers_alerts_timeout)

        count_ok = len_suppliers_all - len_suppliers_alerts_err - len_suppliers_alerts_timeout
        tooltip_err_timeout = tooltip_err_error = ''
        
        if len_suppliers_alerts_err > 0:
            tooltip_err_error = ','.join( suppliers_alerts_err[:max(10,len_suppliers_alerts_err) ])
            if len_suppliers_alerts_err > 10:
                tooltip_err_error += "..."

        if len_suppliers_alerts_timeout > 0:
            tooltip_err_timeout = ','.join( suppliers_alerts_timeout[:max(10,len_suppliers_alerts_timeout)] )
            if len_suppliers_alerts_timeout > 10:
                tooltip_err_timeout += "..."
       
        blocks = await app.common.util.get_message_blocks_payload( ["alertsx_status"], {'count_ok': count_ok, 
                                                                                        'count_err_timeout': len_suppliers_alerts_timeout, 
                                                                                        'count_err_error': len_suppliers_alerts_err,
                                                                                        'tooltip_err_error': tooltip_err_error, 
                                                                                        'tooltip_err_timeout': tooltip_err_timeout
                                                                                        } 
                                                                )
        
        self.logger.info(f"blocks:[{command_in.response_url}][{blocks}]")
        out =  CommandModelOut( response_type='in_channel')
        out.blocks = blocks
        #response to slack https://api.slack.com/reference/messaging/payload
        response = app.common.util.send_slack_post_model(url = command_in.response_url, data_model = out)
        self.logger.info(f"AlertsX execution OK [{response}]")

    async def help_payload(self)->CommandModelOut:
        parser = argparse.ArgumentParser() 
        parser.add_argument("operation")
        valid_operations =['status']
        try:
            args = self.event_in.text.split()
            args = parser.parse_args( args= args )
            if args.operation == 'help':
               raise ValueError("Help requested") 
            if not args.operation in valid_operations:
                raise ValueError("Not valid operation")    
            else:
                return None #Not help and valid operation
        except (ValueError,SystemExit, Exception) as e:
            self.logger.error(f"Argparse: [{repr(e)}], args[{args}]")
            blocks = await app.common.util.get_message_blocks_payload( ["alertsx_help"] )
            out = CommandModelOut( response_type='in_channel', text_test=self.event_in.text_test )
            out.blocks = blocks
            return out
