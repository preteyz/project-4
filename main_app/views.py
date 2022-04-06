from nis import cat
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from django.http import HttpResponse , HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from main_app.models import TravelLocation, User

# Create your views here.
class Home(TemplateView):
    template_name = 'home.html'

class Travel_Locations(TemplateView):
    template_name = 'travel_locations.html'
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

@method_decorator(login_required, name='dispatch')
class Location_Create(CreateView):
    model = TravelLocation
    fields = ['name', 'img', 'environment', 'createdby']
    template_name = "location_create.html"
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.createdby = self.request.user
        self.object.save()
        return HttpResponseRedirect('/travel_locations')

@method_decorator(login_required, name='dispatch')
class Location_Update(UpdateView):
    model = TravelLocation
    fields = ['name', 'img', 'environment', 'createdby']
    template_name = "location_update.html"
    def get_success_url(self):
        return reverse('location_detail', kwargs={'pk': self.object.pk})

@method_decorator(login_required, name='dispatch')
class Location_Delete(DeleteView):
    model = TravelLocation
    template_name = "location_delete_confirmation.html"
    success_url = "/travel_locations/"

# Profile for the user  
@login_required
def profile(request, username):
    user = User.objects.get(username=username)
    locations = TravelLocation.objects.filter(user=user)
    return render(request, 'profile.html', {'username': user.username, 'locations': locations})

# Auth
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            print('HEY', user.username)
            return HttpResponseRedirect('/user/'+str(user))
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/cats')

def login_view(request):
     # if post, then authenticate (user submitted username and password)
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        # form = LoginForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username = u, password = p)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/user/'+u)
                else:
                    return render(request, 'login.html', {'form': form})
            else:
                return render(request, 'login.html', {'form': form})
        else: 
            return render(request, 'signup.html', {'form': form})
    else: # it was a get request so send the emtpy login form
        # form = LoginForm()
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})