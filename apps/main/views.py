from django.shortcuts import render
from .webscrape import web_scraping


def small(request):
    web_scraping()
    return request(render, "email.html")

# Create your views here.
