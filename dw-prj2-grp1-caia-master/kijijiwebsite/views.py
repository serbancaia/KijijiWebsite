from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from database.models import Item


class HomeView(generic.ListView):
    """
    Home view of the web page displaying a list of items
    """
    model = Item
    template_name = 'home/home.html'
