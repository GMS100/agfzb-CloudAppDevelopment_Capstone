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

    try:
        authenticator = IAMAuthenticator(IAM_API_KEY)
        client = CloudantV1(authenticator = authenticator)
        client.set_service_url(COUCH_URL)
        
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    try:
        jsonReview ={
            "id": dict["id"],
            "name": dict["name"],
            "dealership": dict["dealership"],
            "review": dict["review"],
            "purchase": dict["purchase"],
            "another": dict["another"],
            "purchase_date": dict["purchase_date"],
            "car_make": dict["car_make"],
            "car_model": dict["car_model"],
            "car_year": dict["car_year"]
            }

        result = client.post_document(db=DB_NAME, document=jsonReview).get_result()

        print("result=",result["ok"])
        if result["ok"]:
            return {"headers":{"Content-Type":"application/json"},"body":{"result":result}}
        else:
            return {"statusCode":500,"message":"Post unsuccessful","body":{"result":result}}
        
    except (ValueError) as err:
        print("Value Error: 500")
        return {"statusCode":500,"message":"ValueError"}
#    except as err:
#        print("Unknown Error: 500", sys.exc_info()[0])
#        raise
        
        
