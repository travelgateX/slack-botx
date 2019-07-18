import json
import os
from time import time
from datetime import datetime

from starlette.testclient import TestClient

from app.main import app,SLACK_SIGNING_SECRET
from app.common.util import create_slack_signature

client = TestClient(app)

def _send_data( payload ):
    response = client.post(
        url="onwebchange/webhook",
        headers={'content-type':'application/x-www-form-urlencoded'},
        data=payload
    )
    print(f"response:[{response}], content:[{response.content}]")
    return response

def test_onwebchange_callback(mock_env_slack):
    print(f"Environment: {os.environ.get('SLACK_CHANNEL_ANNOUNCEMENTS')} ") 

    today = datetime.today().strftime('%Y-%m-%d')
    #payload= 'femtoo_callback_data=Stats%2Bchangelog%2B%2B%2B%2BEdit%2Bpage%2B%2BEasily%2Baccessible%2Blog%2Bof%2Bnotable%2Bchanges%2Bto%2BStats%2B%2B'+today+'%2B%2B%2B%2Btest222%2Bchangelog.%2B%2B2019-06-12%2B%2B%2B%2BFix%2Ban%2Berror%2Bthat%2Bwas%2Bcausing%2Bto%2Bhave%2Bempty%2B%2Boperations%2Bin%2Bthe%2Bresponse.%2B%2B2019-06-03%2B%2B%2B%2BNew%2Bscalar%2Btype%2BInt64%2Bhas%2Bbeen%2Bcreated.%2B%2Bhits%2Bin%2B%2BStatsData%2B%252C%2B%2BtotalHits%2Bin%2B%2BOperationDetailed%2Band%2B%2Bhits%2Bin%2B%2BStatsInfo%2Bhave%2Bchanged%2Bits%2Btype%2Bto%2Bthis%2Bnew%2Bscalar.%2B%2B2019-05-30%2B%2B%2B%2BNow%2B%2BadviceMessage%2B%25E2%2580%2599s%2Bfrom%2Bothers%2BTravelgateX%2Bproducts%2Bare%2Breturned%2Bas%2B%2Bexternal%2Bin%2Bowns%2B%2BadviceMessage%2B%25E2%2580%2599s.%2B%2B2019-05-23%2B%2B%2B%2BNow%2B%2Btype%2Bof%2B%2BStatsInfo%2Breturns%2Bthe%2Bcorrect%2Bvalue.%2B%2B2019-05-22%2B%2B%2B%2BNow%2Bstats%2Bare%2Bavailable%2Bfrom%2B01%252F01%252F2018.%2BRequests%2Bby%2B%2BaccessCode%2Bare%2Bavailable%2Bonly%2Bfrom%2B15%252F05%252F2019.%2B%2B2019-05-14%2B%2B%2B%2BFix%2Ban%2Berror%2Bthat%2Bwas%2Bcausing%2B%2BaccessCode%2Bnot%2Bbeing%2Bstored%2Bsuccessfully.%2B%2BFix%2Ban%2Berror%2Bto%2Bshow%2B100%2Bassets%2Bper%2B%2BerrorCode%2Band%2Bper%2B%2Boperation%2B.%2B%2B2019-05-03%2B%2B%2B%2BFix%2Ban%2Berror%2Bthat%2Bwas%2Bcausing%2Bthat%2Bassets%2Bof%2BHUB%2Berror%2Btypes%2Bwere%2BNULL.%2B%2B2019-05-02%2B%2B%2B%2BInput%2Bfield%2B%2BretrieveAssets%2Bmade%2Boptional.%2B%2Bfalse%2Bby%2Bdefault.%2B%2B2019-04-30%2B%2B%2B%2BNew%2Brequired%2Binput%2Bfield%2B%2BretrieveAssets%2Badded%2Bto%2Bindicate%2Bif%2Bassets%2Bare%2Bneeded.%2B%2B%2B%2BAssets%2Breturned%2Blimited%2Bto%2B100%2Bto%2Bavoid%2Btoo%2Bbig%2Bresponses.%2BThis%2Blimitation%2Bmakes%2Bsense%2Bsince%2Bthe%2Bmain%2Bobjective%2Bis%2Bnot%2Bto%2Baccess%2Ball%2Bthe%2Basset%2Bnodes.%2B%2B2019-04-23%2B%2B%2B%2BFix%2Ban%2Berror%2Bbuilding%2Binternal%2Bqueries%2Bwhen%2BQuote%252FBooking%2Band%2BOther%2Bare%2Brequested.%2B%2B2019-04-11%2B%2B%2B%2BNew%2Binput%2Bfield%2B%2Bowner%2Badded%2Bto%2Ballow%2Bfilter%2Bby%2Borganization.%2B%2B2019-04-08%2B%2B%2B%2B%2Blabel%2Bin%2B%2BOperationData%2Badded.%2BReason%253A%2BShare%2Bthe%2Boperation%2Bcode%2Bin%2BEnglish.%2B%2B%2Bhits%2Bin%2B%2BStatsData%2Badded.%2BReason%253A%2BShare%2Ba%2Bsummary%2Bof%2Bhits%2Bat%2B%2BStatsData%2Blevel.%2B%2B%2B%2BInternal%2Bqueries%2Bto%2BStats%2BDB%2Boptimized.%2B%2B2019-04-03%2B%2B%2B%2B%2BtrafficType%2Bin%2B%2BOperationDetailed%2Badded.%2BReason%253A%2BTo%2Bdifferentiate%2Bexistent%2Btraffic%2Btypes%253A%2BBASIC%252C%2BSPEED%252C%2BOPTIMIZED.%2B%2B2019-03-14%2B%2B%2B%2BStats%2B%2Bproduct%2Bdocumentation%2B%2B%2BComments&femtoo_callback_url=https%253A%252F%252Fdocs.travelgatex.com%252Fstats%252Frelease-notes%252Fchangelog%252F&femtoo_callback_label=Stats'
    payload = {"femtoo_callback_url": "https://docs.travelgatex.com/hotel-x/release-notes/changelog/",
               "femtoo_callback_data":"Alerts-X changelog    Edit page  Easily accessible log of notable changes to Alerts-X  "+today+"    After an alert configuration update their past  events will be deleted.  2019-06-12    Fixed an error that was causing an unsuccessful alert create or update to set  clients ,  suppliers and  accesses to the alert for Travelgate Teams users.  2019-06-11    Fixed an error to return all the  events of the alerts.  2019-06-06    Added  /Health to check service status.  2019-05-23    Alerts-X  product documentation is available   Comments",
               "femtoo_callback_label":"Hotel-X"
             }
    response = _send_data(payload)
    assert response.status_code == 200
    