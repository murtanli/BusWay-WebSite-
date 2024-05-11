from django.urls import path
from .views import *

urlpatterns = [
    path('', main_page, name="main_page"),
    path('logout_func/', logout_func, name="logout_func"),
    path('search_routes/', search_routes, name="search_routes"),
]