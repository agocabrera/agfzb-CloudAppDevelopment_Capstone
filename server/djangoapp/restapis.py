import json
import os
import requests
from .models import CarDealer, DealerReview
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth


def get_request(url, api_key="", **kwargs):
    response = {}
    if api_key:
        # IBM Watson NLU request.
        try:
            response = requests.get(url, kwargs, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth("apikey", api_key))
        except requests.exceptions.RequestException as error:
            print(error)

        if response.text:
            result = json.loads(response.text)
            return result

    else:
        try:
            response = requests.get(url, params=kwargs, headers={'Content-Type': 'application/json'})
        except requests.exceptions.RequestException as error:
            print(error)

        if response.text:
            result = json.loads(response.text)
            return result


def get_dealers_from_cf(url, **kwargs):
    if kwargs:
        response = get_request(url, **kwargs)
        return response["docs"][0]
    else:
        results = []
        json_result = get_request(url)
        if json_result:
            dealers = json_result["rows"]
            for dealer in dealers:
                dealer_doc = dealer["doc"]
                dealer_obj = CarDealer(address=dealer_doc.get("address"), city=dealer_doc.get("city"),
                                       full_name=dealer_doc.get("full_name"), id=dealer_doc.get("id"),
                                       lat=dealer_doc.get("lat"), long=dealer_doc.get("long"),
                                       short_name=dealer_doc.get("short_name"),
                                       st=dealer_doc.get("st"), zip=dealer_doc.get("zip"))
                results.append(dealer_obj)
            return results


def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url, **kwargs)
    if json_result:
        reviews = json_result["docs"]
        for review in reviews:
            review_obj = DealerReview(id=review.get("id"), name=review.get("name"),
                                      dealership=review.get("dealership"), review=review.get("review"),
                                      purchase=review.get("purchase"), purchase_date=review.get("purchase_date"),
                                      car_make=review.get("car_make"), car_model=review.get("car_model"),
                                      car_year=review.get("car_year"),
                                      sentiment=analyze_review_sentiments(review.get("review")))
            results.append(review_obj)

    return results


def analyze_review_sentiments(review):
    load_dotenv()
    key = os.getenv("WATSON_NLU_KEY")
    url = os.getenv("WATSON_NLU_URL")
    params = {
        "text": review,
        "features": ["sentiment"],
        "return_analyzed_text": True,
        "version": "2022-04-07"
    }
    response = get_request(url, key, **params)
    if response.get("sentiment"):
        return response["sentiment"]["document"]["label"]


def post_request(url, payload, **kwargs):
    try:
        response = requests.post(url, json=payload, params=kwargs, headers={'Content-Type': 'application/json'})
    except requests.exceptions.RequestException as error:
        print(error)
    else:
        if response.text:
            result = json.loads(response.text)
            print("POST_REQUEST RESULT", result)
            return result
