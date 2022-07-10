from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(max_length=100, default=None)
    desc = models.CharField(max_length=300)

    def __str__(self):
        return self.name

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    SEDAN = 'SE'
    COUPE = 'CO'
    SUV = 'SU'
    PICKUP = 'PI'
    WAGON = 'WA'
    MINIVAN = 'MI'

    BODY_TYPE_CHOICES = [(SEDAN, 'Sedan'),
                         (COUPE, 'Coupe'),
                         (SUV, 'Sport Utility Vehicle'),
                         (PICKUP, 'Pickup Truck'),
                         (WAGON, 'Station Wagon'),
                         (MINIVAN, 'Minivan')]

    make = models.ForeignKey(CarMake, default=0, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    dealerID = models.IntegerField()
    year = models.DateField(default=now)
    bodyType = models.CharField(max_length=2, choices=BODY_TYPE_CHOICES)

    def __str__(self):
        return (self.make.name + " " + self.name + " " + self.year.strftime('%Y'))

# A plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# A plain Python class `DealerReview` to hold review data
class DealerReview:

    def __init__(self, dealership, name, purchase, review):
        # Dealer Id
        self.dealership = dealership
        # Reviewer Name
        self.name = name
        # Purchase?
        self.purchase = purchase
        # Review
        self.review = review
        #Optional attributes
        # Purchase Date
        self.purchase_date = ""
        # Car Make
        self.car_make = ""
        # Car Model
        self.car_model = ""
        # Car Year
        self.car_year = ""
        # Sentiment - from Watson NLU
        self.sentiment = ""
        # Review Id
        self.review_id = ""

    def __str__(self):
        return "DealerId: " + str(self.dealership) + "  Review: " + self.review

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)