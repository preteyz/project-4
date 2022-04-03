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

class Location_Detail(DetailView):
    model = TravelLocation
    template_name = "location_detail.html"

class Location_Create(CreateView):
    model = TravelLocation
    fields = ['name', 'img', 'environment', 'createdby']
    template_name = "location_create.html"
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.createdby = self.request.user
        self.object.save()
        return HttpResponseRedirect('/browse')

class Location_Update(UpdateView):
    model = TravelLocation
    fields = ['name', 'img', 'environment', 'createdby']
    template_name = "location_update.html"
    def get_success_url(self):
        return reverse('location_detail', kwargs={'pk': self.object.pk})

class Location_Delete(DeleteView):
    model = TravelLocation
    template_name = "location_delete_confirmation.html"
    success_url = "/browse/"