import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features,SentimentOptions

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print("get_request: kwargs=", kwargs)
    print("get request: url=", "GET from {} ".format(url))
    try:
        response = requests.Response()
        api_key = kwargs.get('apikey', False)
        if api_key:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            # Call get method of requests library with auth, URL and parameters
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        else:
            # Call get method of requests library without auth
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("get_request: Network exception occurred")
    status_code = response.status_code
    print("get_request:", "With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    print("post_request: " + str(kwargs))
    print("post_request: " + "GET from {} ".format(url))
    try:
        # Call post method of requests library without auth
        response = requests.post(url, params=kwargs, json=json_payload)
    except:
        # If any error occurs
        print("post_request: Network exception occurred")
    status_code = response.status_code
    print("post_request: With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Call dealer_json_to_objects() with JSON results
def get_dealers_from_cf(url, **kwargs):
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        results = dealer_json_to_objects(json_result)
    return results

# Create a get_dealers_ method to get dealers from a cloud function
# def get_dealers_by_state(url, **kwargs):
# - Call get_request() with specified arguments
# - Call dealer_json_to_objects() with JSON results
def get_dealers_by_state(url, state):
     # Call get_request with a URL parameter
    json_result = get_request(url, state = state)
    if json_result:
        results = dealer_json_to_objects(json_result)
    return results

# Create a get_dealers_ method to get dealers from a cloud function
# def get_dealers_by_id(url, **kwargs):
# - Call get_request() with specified arguments
# - Call dealer_json_to_objects() with JSON results
def get_dealers_by_id(url, id):
    # Returns a dealer object, not a list of dealers
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, id=id)
    if json_result:
        dealers = json_result["result"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                               id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                               short_name=dealer_doc["short_name"], st=dealer_doc["st"], zip=dealer_doc["zip"])
    return dealer_obj

# Parse JSON results into a CarDealer object list
# def dealer_json_to_objects(json_result):
# - Requires a json object with data for one or more dealers
# - Returns a list of CarDealer object(s)
def dealer_json_to_objects(json_result):
    # Returns a list of dealer objects
    results = []
    # Get the row list in JSON as dealers
    dealers = json_result["result"]
    # For each dealer object
    for dealer in dealers:
        dealer_doc = dealer
        # Create a CarDealer object with values in `doc` object
        dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                               id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                               short_name=dealer_doc["short_name"], st=dealer_doc["st"], zip=dealer_doc["zip"])
        results.append(dealer_obj)
    return results

# get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
#def get_dealer_reviews_from_cf(url, dealerId):
def get_dealer_reviews_from_cf(url, id):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId=id)

    if json_result and (json_result['statusCode'] == 200):
        # Get the result list in JSON as reviews
        reviews = json_result["result"]
        # For each review object
        for review in reviews:
            # Get its content in `doc` object
            review_doc = review
            # Create a DealerReview object with values in `doc` object
            review_obj = DealerReview(dealership=review_doc["dealership"], name=review_doc["name"], 
                       purchase=review_doc["purchase"],review=review_doc["review"])
            if "purchase_date" in review:
                review_obj.purchase_date=review_doc["purchase_date"]
            if "car_make" in review:
                review_obj.car_make = review_doc["car_make"]
            if "car_model" in review:
                review_obj.car_model = review_doc["car_model"]
            if "car_year" in review:
                review_obj.car_year = review_doc["car_year"]
            if "id" in review:
                review_obj.review_id = review_doc["id"]

            review_obj.sentiment = analyze_review_sentiments(review_obj.review)

            results.append(review_obj)
        return results
    else:
        return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealer_review):
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/b38d3838-1a6c-4e92-a7ca-72ba83a4b62e"
    api_key = "pN4oOSB2WX9jkwgEuhVNdlCY2kJysoAoNKmI6n-1Vsah" 
    authenticator = IAMAuthenticator(api_key) 
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator) 
    natural_language_understanding.set_service_url(url) 
    response = natural_language_understanding.analyze( text=(dealer_review + "  make it longer") ,features=Features(sentiment=SentimentOptions(targets=[(dealer_review + "  make it longer")]))).get_result() 
    label=json.dumps(response, indent=2) 
    label = response['sentiment']['document']['label'] 
    return(label)     