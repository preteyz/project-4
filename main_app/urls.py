from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name = "home"),
    path('browse/', views.Browse.as_view(), name = "browse"),
    path('browse/new', views.Location_Create.as_view(), name = "location_create"),
    path('browse/<int:pk>', views.Location_Detail.as_view(), name = "location_detail"),
    path('browse/<int:pk>/update', views.Location_Update.as_view(), name="location_update"),
    path('browse/<int:pk>/delete', views.Location_Delete.as_view(), name="location_delete"),
]