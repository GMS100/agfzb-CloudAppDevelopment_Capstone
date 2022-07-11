from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from .restapis import get_dealers_by_state, get_dealers_by_id
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

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
            return redirect('djangoapp:index')
        else:
            # If not, return to login page again
            context['message'] = "Invalid username or password."
            context['user'] = username
            print("login_request: context=", context)
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
        context = {}
        url = "https://49b0e2fc.us-south.apigw.appdomain.cloud/api/dealership/dealer-get"

        # Get dealers by state and add to context
        dealerships = get_dealers_by_state(url, state)
        context["dealership_list"] = dealerships

        return render(request, 'djangoapp/index.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealership_by_id(request, id):
    if request.method == "GET":
        context = {}
        url = "https://49b0e2fc.us-south.apigw.appdomain.cloud/api/dealership/dealer-get"

        # Get dealers by id and add to context
        dealerships = get_dealers_by_id(url, id)
        context["dealership_list"] = dealerships
        return render(request, 'djangoapp/index.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        # Context will contain the dealership objects
        context = {}
        url = "https://49b0e2fc.us-south.apigw.appdomain.cloud/api/dealership/dealer-get"
        
        # Get dealers from the URL and add to context
        dealerships = get_dealers_from_cf(url)
        context["dealership_list"] = dealerships

        return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, id):
    if request.method == "GET":
        # Context will contain dealer and review objects
        context = {}
        dealer_url = "https://49b0e2fc.us-south.apigw.appdomain.cloud/api/dealership/dealer-get"

        # Get dealer object and add to context
        dealer = get_dealers_by_id(dealer_url, id=id)
        context["dealer"] = dealer

        #get review objects and add to context
        review_url = "https://49b0e2fc.us-south.apigw.appdomain.cloud/api/review/review-get"
        reviews = get_dealer_reviews_from_cf(review_url, id=id)
        context["reviews"] = reviews
        
        # Return the dealer detail page info
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, id):
    context = {}
    dealer_url = "https://49b0e2fc.us-south.apigw.appdomain.cloud/api/dealership/dealer-get"

    # Get dealer and add to context
    dealer = get_dealers_by_id(dealer_url, id=id)
    context["dealer"] = dealer

    if request.method == 'GET':
        print("add_review: GET request=", request)
        # Get cars by dealer and add to context
#        cars = CarModel.objects.all()
        cars = CarModel.objects.filter(dealerID=id)
        context["cars"] = cars      
        print("add_review: context to be returned from GET=")
        print(context) 
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == 'POST':
        print("add_review: POST request=", request)
        # Get user information from request.POST
        if request.user.is_authenticated:
            username = request.user.username
            # Create review object
            review = dict()
            car_id = request.POST["car"]
            car = CarModel.objects.get(pk=car_id)
            review["dealership"] = id
            review["name"] = username
            # Set review id to the date/time saved
            review["id"] = datetime.utcnow().isoformat()
            review["review"] = request.POST["content"]
            if "purchasecheck" in request.POST:
                if request.POST["purchasecheck"] == 'on':
                    review["purchase"] = "true"
                    review["purchase_date"] = request.POST["purchasedate"]
                    review["car_make"] = car.make.name
                    review["car_model"] = car.name
                    review["car_year"] = int(car.year.strftime("%Y"))
            else:
                review["purchase"] = "false"
                review["purchase_date"] = ""
                review["car_make"] = ""
                review["car_model"] = ""
                review["car_year"] = ""

            review_url = "https://49b0e2fc.us-south.apigw.appdomain.cloud/api/review"
            print("add_review: calling post_request id=", id)
            print("add_review: calling post_request review_url=", review_url)
            print("add_review: calling post_request payload=", review)
            response = post_request(review_url, review, id=id)

            print("add_review: post_request response=", response)
            return redirect("djangoapp:dealer_details", id=id)
        else: 
            response =  [{"statusCode":"404"},{"message":"Please login to add a review"}]
    else:
        response = [{"statusCode":"404"},{"message":"Not a GET or POST request"}]

    return HttpResponse(response)
