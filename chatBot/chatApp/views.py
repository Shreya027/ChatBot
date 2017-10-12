from django.shortcuts import render


# Create your views here.
#from mysite.forms import ContactForm,ListForm,UserForm
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render

from textblob import TextBlob

import random
import re

def index(request):
    return render(request,'index.html')    


def check_for_recipes(sentence):

    resp = "Check out recipes at Epicurious , Food and Allrecipes :"
    link1 ="http://www.epicurious.com/"
    link2="http://www.food.com/"
    link3="http://allrecipes.com/"
    return resp,link1,link2,link3


def check_for_restaurants(sentence):
    resp = "Check out restaurants at Zomato , Yelp and Foursquare : "
    link1 ="https://www.zomato.com"
    link2 ="https://www.yelp.com"
    link3="https://foursquare.com"
    return resp,link1,link2,link3

def check_for_hotels(sentence):
    resp = "Check out hotels at HotelsCombined , Trivago and Booking.com : "
    link1 ="https://www.hotelscombined.com/"
    link2 ="https://www.trivago.com"
    link3="https://www.booking.com"
    return resp,link1,link2,link3



def check_for_shopping(sentence):
    resp = "Check out e-commerce websites: Amazon, Ebay and Flipkart : "
    link1 ="https://www.amazon.com"
    link2 ="https://www.ebay.com/"
    link3="https://www.flipkart.com/"
    return resp,link1,link2,link3



def check_for_social(sentence):
    resp = "Check out social networking websites: Facebook , Twitter, Linkedin : "
    link1 ="https://www.facebook.com"
    link2 ="https://twitter.com"
    link3="https://www.linkedin.com"
    return resp,link1,link2,link3



recipe_pattern = re.compile("^recipe|^cook|^make|^prepare")
restaurant_pattern = re.compile("^restaurant|^food|^eat|^lunch|^dinner|^brunch|^snack|^cafe|^bar|^hungry")
hotel_pattern = re.compile("^hotel|^stay|^room|^inn|^lodge|^accomodation|^trip|^travel")
social_pattern = re.compile("^social|^network|^facebook|^twitter|^linked|^bored|^fb")
shopping_pattern = re.compile("^shop|^market|^store|^buy|^purchase")


def check_for_keywords(sentence):
    link1=None
    link2=None
    link3=None
    resp=None
    for word in sentence.words:
        
        if recipe_pattern.match(word.lower()):
            resp,link1,link2,link3 =check_for_recipes(sentence)
            
            break
            
        elif restaurant_pattern.match(word.lower()): 
            
            resp,link1,link2,link3 =check_for_restaurants(sentence)
            break
          

        elif hotel_pattern.match(word.lower()):
            resp,link1,link2,link3=check_for_hotels(sentence)
            break
           

        elif social_pattern.match(word.lower()):
            resp,link1,link2,link3 =check_for_social(sentence)
            break

        elif shopping_pattern.match(word.lower()): 
            resp,link1,link2,link3 =check_for_shopping(sentence)
            break

    return resp,link1,link2,link3



greeting_pattern = re.compile("^hello|^hi|^greeting|^sup|^what's up|^hey")

GREETING_RESPONSES = ["Hey, you seem hungry..", "Oh hi there :p ", "Hey food lover :D " , "Hey, what's up ?"]



NONE_RESPONSES = [
    "I didn't get what you said...",
    "I didn't understand. You could ask questions related to restaurants ,recipes ,hotels, shopping ,social networking...",
    "Umm, could you please elaborate ? ",

]


def check_for_greeting(sentence):
    """If any of the words in the user's input was a greeting, return a greeting response"""
    for word in sentence.words:
        if greeting_pattern.match(word.lower()) :
            return random.choice(GREETING_RESPONSES)


def request(sentence):
    #cleaned = preprocess_text(sentence)
    parsed = TextBlob(sentence)

    resp= None
    link1=None
    link2=None
    link3=None

    resp,link1,link2,link3 = check_for_keywords(parsed)


    if not resp:
        resp = check_for_greeting(parsed)

    if not resp:
        resp = random.choice(NONE_RESPONSES)

    return resp,link1,link2,link3



def reply(sentence):
    resp,link1,link2,link3  = request(sentence)
    return resp,link1,link2,link3


def respond(request):
    
    errors = []
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            errors.append('Enter a valid chat')
        
        else:
            resp,link1,link2,link3=reply(q)
            return render(request, 'index.html',
                          {'resp':resp,'link1':link1,'link2':link2,'link3':link3})
        
    return render(request, 'index.html',
              {'errors': errors})

