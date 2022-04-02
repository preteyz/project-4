from nis import cat
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from django.http import HttpResponse , HttpResponseRedirect
from django.urls import reverse

from main_app.models import TravelLocation

# Create your views here.
class Home(TemplateView):
    template_name = 'home.html'

class Browse(TemplateView):
    template_name = 'browse.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name")
        if name != None:
            context["TravelLocations"] = TravelLocation.objects.filter(name__icontains=name)
            context["header"] = f"Searching for {name}"
        else: 
            context['TravelLocations'] = TravelLocation.objects.all() # this is where we add the key into our context object for the view to use
            context['header'] = "Our Travel Locations!"
        return context

