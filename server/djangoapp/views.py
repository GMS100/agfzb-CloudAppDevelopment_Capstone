from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
#from .models import related models
from .restapis import get_dealers_from_cf, get_dealers_by_state, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
# def about(request):
# ...
def about(request):
    return render(request, 'djangoapp/about.html')

# Create a `contact` view to return a static contact page
#def contact(request):
def contact(request):
    return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...
def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
 # Change pages for redirects?
            return redirect('djangoapp:index')
        else:
            # If not, return to login page again
            context['message'] = "Invalid username or password."
            context['user'] = username
            #return render(request, 'djangoapp/index.html', context)
            print(str(context))
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...
def logout_request(request):
    # Logout user in the request
    logout(request)
    # Redirect user back to home page
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...
def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            # Login the user and redirect to course list page
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships_by_state(request, state):
    if request.method == "GET":
        # url = "your-cloud-function-domain/dealerships/dealer-get"
        url = "https://49b0e2fc.us-south.apigw.appdomain.cloud/api/dealership/dealer-get"
        # Get dealers by state
        dealerships = get_dealers_by_state(url, state)

        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        # Context will contain the dealership objects
        context = {}

        # url = "your-cloud-function-domain/dealerships/dealer-get"
        url = "https://49b0e2fc.us-south.apigw.appdomain.cloud/api/dealership/dealer-get"
        
        # Get dealers from the URL and add to context
        dealerships = get_dealers_from_cf(url)
        context["dealership_list"] = dealerships

        # Concat all dealer's short name *** stub code for testing
        #dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        #return HttpResponse(dealer_names)
        
        return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealerId):
    if request.method == "GET":
        # Context will contain dealer and review objects
        context = {}
        #url = "your-cloud-function-domain/review/review-get"
        url = "https://49b0e2fc.us-south.apigw.appdomain.cloud/api/review/review-get"
#        url = "https://49b0e2fc.us-south.apigw.appdomain.cloud/api/dealership/review-get"
        # Get dealers from the URL
        reviews = get_dealer_reviews_from_cf(url, dealerId)
        context["results"] = reviews
        
        # Concat all dealer's short name  ** Stub code for testing
        #review_list = ' '.join([("Review: " + review.review + " Sentiment: " + review.sentiment) for review in reviews])
        # Return a list of reviews
        
        # Return the dealer detail page info
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id):
    print("in add_review")
    if request.method == 'POST':
        url = "https://49b0e2fc.us-south.apigw.appdomain.cloud/api/dealership/dealer-get"
        # Get user information from request.POST
        print("in add_review POST")
        if request.user.is_authenticated:
            print("in True if")
#            username = request.user.username
            username = "TestUser1"
            # Create review object
            review["dealership"] = 46
            review["name"] = username
#            if "purchasecheck" in request.POST:
#                if request.POST["purchasecheck"] == 'on':
#                    review["purchase"] = True
            review["purchase"] = "false"
            review["review"] = "This is an awful dealer. Don't go there."
            review["purchase_date"] = datetime.utcnow().isoformat()
            review["car_make"] = "Honda"
            review["car_model"] = "Civic"
            review["car_year"] = 2022
            review["sentiment"] = "Neutral"
            review["review_id"] = 5500

            json_payload["review"] = review
            response = post_request(url, json_payload, dealerId=dealer_id)
        else: 
            response =  [{"statusCode":"404"},{"message":"User not logged in"}]
    else:
        response = [{"statusCode":"404"},{"message":"Not a POST request"}]

    return HttpResponse(response)
