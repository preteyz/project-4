from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name = "home"),

    # travel_locations CRUD
    path('travel_locations/', views.Travel_Locations.as_view(), name = "travel_locations"),
    path('travel_locations/new', views.Location_Create.as_view(), name = "location_create"),
    path('travel_locations/<int:pk>', views.Location_Detail.as_view(), name = "location_detail"),
    path('travel_locations/<int:pk>/update', views.Location_Update.as_view(), name="location_update"),
    path('travel_locations/<int:pk>/delete', views.Location_Delete.as_view(), name="location_delete"),

    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    # Profile
    path('user/<username>/', views.profile, name='profile'),


]