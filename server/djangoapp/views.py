import logging
import os
from .models import CarModel
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)


def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)


def logout_request(request):
    if request.method == "GET":
        logout(request)
    return redirect('djangoapp:index')


def registration_request(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)


def get_dealerships(request):
    if request.method == "GET":
        load_dotenv()
        url = os.getenv("GET_DEALERSHIPS_URL")
        dealerships = get_dealers_from_cf(url)
        context = {"dealerships": dealerships}
        return render(request, 'djangoapp/index.html', context)


def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        load_dotenv()
        dealerships_url = os.getenv("GET_DEALERSHIPS_URL")
        get_reviews_url = os.getenv("GET_REVIEWS_URL")
        reviews = get_dealer_reviews_from_cf(get_reviews_url, id=dealer_id)
        dealership = get_dealers_from_cf(dealerships_url, id=dealer_id)
        context = {"reviews": reviews, "dealership": dealership}
        return render(request, 'djangoapp/dealer_details.html', context)


def add_review(request, dealer_id):
    load_dotenv()
    dealerships_url = os.getenv("GET_DEALERSHIPS_URL")
    post_reviews_url = os.getenv("POST_REVIEWS_URL")
    dealership = get_dealers_from_cf(dealerships_url, id=dealer_id)

    if request.method == "GET":
        cars = CarModel.objects.all()
        context = {"dealer_id": dealer_id, "cars": cars, "dealership": dealership}
        return render(request, 'djangoapp/add_review.html', context)

    if request.method == "POST":
        if not request.user.is_authenticated:
            return
        car = CarModel.objects.get(pk=request.POST["car"])
        review = {
            "name": request.user.get_full_name(),
            "dealership": dealer_id,
            "review": request.POST["content"],
            "purchase": True if request.POST["purchasecheck"] == "on" else False,
            "purchase_date": request.POST["purchasedate"].replace("-", "/"),
            "car_make": car.make.name,
            "car_model": car.name,
            "car_year": int(car.year.strftime("%Y"))
        }
        post_request(post_reviews_url, review)
    return redirect("djangoapp:dealer_details", dealer_id)
