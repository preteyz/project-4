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


    path('travel_locations/<int:pk>/create_review/', views.Review_Create.as_view(), name = "review_create"),

    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    
    # Profile
    path('user/<username>/', views.profile, name='profile'),

    # Review CRUD
    path('reviews/', views.reviews_index, name='reviews_index'),
    path('reviews/create/', views.Review_Create.as_view(), name='review_create'),
    path('reviews/<int:pk>/update/', views.Review_Update.as_view(), name='review_update'),
    path('reviews/<int:pk>/delete/', views.Review_Delete.as_view(), name='review_delete'),


]