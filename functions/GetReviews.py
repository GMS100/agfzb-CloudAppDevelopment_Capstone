#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
import sys
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import requests


def main(dict):
    COUCH_URL = dict['COUCH_URL']
    IAM_API_KEY = dict['IAM_API_KEY']
    COUCH_USERNAME = dict['COUCH_USERNAME']

    dbname = "reviews"
    dealershipID = dict["dealerId"]
    
    try:
        authenticator = IAMAuthenticator(IAM_API_KEY)
        client = CloudantV1(authenticator = authenticator)
        client.set_service_url(COUCH_URL)
        
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}


    try:
        print("about to query db for dealer " + str(dealershipID))
        dealershipReviews = client.post_find(db=dbname,selector={'dealership':dealershipID},execution_stats=True).get_result()
        print("after query")
        #print(dealershipReviews)
        #print("Length=" + str(dealershipReviews['execution_stats']['results_returned']))
        if (dealershipReviews['execution_stats']['results_returned'] == 0):
            print("going to throw 404 error")
            return {"error": "Error 404: Dealer Id does not exist"}
    
    except (ValueError) as err:
        print("Value Error: " + err)
        return {"error": "100 Value Error"}
    

    return {"reviews":dealershipReviews["docs"]}
    
    
    
    
    
    
    
