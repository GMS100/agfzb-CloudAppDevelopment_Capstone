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

    try:
        authenticator = IAMAuthenticator(IAM_API_KEY)
        client = CloudantV1(authenticator = authenticator)
        client.set_service_url(COUCH_URL)
        
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}


    try:
        print("Code to post a review will go here")
        jsonReview = {"review": 
            {
            "id": 5000,
            "name": "Fred Tester",
            "dealership": 46,
            "review": "Great service!",
            "purchase": False,
            "another": "field",
            "purchase_date": "02/16/2021",
            "car_make": "Audi",
            "car_model": "Car",
            "car_year": 2021
            }
        }
        
    except (ValueError) as err:
        print("Value Error: " + err)
        return {"error": "Error 100: Value Error"}

#What do i want to return for a post...
    return jsonReview
