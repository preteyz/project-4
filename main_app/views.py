from nis import cat
from django.shortcuts import render, get_object_or_404
from os import environ
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
from django.urls import reverse

# Import for OR filter
from django.db.models import Q

from main_app.models import TravelLocation, User, Review

def Favorite_View(request, pk):
    location = get_object_or_404(TravelLocation, id=request.POST.get('location_id'))
    favorited = False
    if location.favorites.filter(id=request.user.id).exists():
        location.favorites.remove(request.user)
        
        favorited = False
    else:
        location.favorites.add(request.user)
        favorited = True
    return HttpResponseRedirect(reverse('location_detail', args=[str(pk)]))

# Create your views here.
class Home(TemplateView):
    template_name = 'home.html'

class Travel_Locations(TemplateView):
    template_name = 'travel_locations.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("query")
        environment = self.request.GET.get("environment_search")
        if query != None:
            context["locations"] = TravelLocation.objects.filter(Q(name = query) | Q(environment = query))
            context["header"] = f"Searching for {query}"
            context["environments"] =TravelLocation.objects.values_list('environment', flat=True).distinct()
        else: 
            context['header'] = "Our travel locations"
            context["locations"] =TravelLocation.objects.all()
            context["environments"] =TravelLocation.objects.values_list('environment', flat=True).distinct()
        if environment != None:
            context["locations"] = TravelLocation.objects.filter(environment__icontains=environment)
        return context
        

class Location_Detail(DetailView):
    model = TravelLocation
    template_name = "location_detail.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        location = get_object_or_404(TravelLocation, id=self.kwargs['pk'])
        faved = False
        if location.favorites.filter(id=self.request.user.id).exists():
            faved = True

        # total_favs = location.total_likes()
        context['location'] = location
        context['faved'] = faved
        context['favorites'] = TravelLocation.objects.values_list('favorites', flat=True).distinct()
        # context['total_favs'] = total_favs
        context['reviews'] = Review.objects.all()
        # context['reviews'] = Review.objects.filter(location__icontains=name)
        return context


@method_decorator(login_required, name='dispatch')
class Location_Create(CreateView):
    model = TravelLocation
#     fields = ['user', 'name', 'img', 'environment', 'favorites']
    fields = ['name', 'img', 'environment', 'description']
    template_name = "location_create.html"
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect('/travel_locations')

@method_decorator(login_required, name='dispatch')
class Location_Update(UpdateView):
    model = TravelLocation
    fields = ['name', 'img', 'environment', 'description']
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
    return HttpResponseRedirect('/')

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


def reviews_index(request):
    reviews = Review.objects.all()
    return render(request, 'reviews_index.html', {'reviews': reviews })

@method_decorator(login_required, name='dispatch')
class Review_Create(CreateView):
    model = Review
    fields = fields = ['travel_location', 'rating', 'body']
    template_name = "reviews_form.html"
    # success_url = '/reviews'
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.location = self.request.user
    #     self.object.save()
        return HttpResponseRedirect('/travel_locations')

@method_decorator(login_required, name='dispatch')
class Review_Update(UpdateView):
    model = Review
    fields = ['rating', 'body']
    template_name = "reviews_update.html"
    success_url = '/reviews'

@method_decorator(login_required, name='dispatch')
class Review_Delete(DeleteView):
    model = Review
    template_name = "reviews_confirm_delete.html"
    success_url = '/reviews'