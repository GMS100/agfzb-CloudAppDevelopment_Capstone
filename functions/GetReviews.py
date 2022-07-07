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

    DB_NAME = "reviews"
    status=200
    
    try:
        dealershipID = int(dict["dealerId"])

        authenticator = IAMAuthenticator(IAM_API_KEY)
        client = CloudantV1(authenticator = authenticator)
        client.set_service_url(COUCH_URL)
        
        dealershipReviews = client.post_find(db=DB_NAME,selector={'dealership':dealershipID},
             execution_stats=True).get_result()

        if (dealershipReviews['execution_stats']['results_returned'] == 0):
            print("No results returned: 404")
            return {"statusCode":404,"message":"No reviews for dealer #" + str(dealershipID)}

        return {"statusCode":status,"headers":{"Content-Type":"application/json"}, 
            "result":dealershipReviews["docs"]};         

    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("DB connection error: 500")
        return {"statusCode":500, "message":"DB connection error"}

    except (ValueError) as err:
        print("ValueError: 404")
        return {"statusCode": 404, "message":"Invalid dealer ID: " + str(dict["dealerId"])} 

    except (KeyError) as err:
        print("KeyError: 404")
        return {"statusCode": 404, "message":"Missing dealerId parameter"}
    