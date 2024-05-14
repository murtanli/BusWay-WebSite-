from django.urls import path
from .views import *

urlpatterns = [
    path('', main_page, name="main_page"),
    path('logout_func/', logout_func, name="logout_func"),
    path('search_routes/', search_routes, name="search_routes"),
    path('create_ticket/', create_ticket, name="create_ticket"),
    path('auth/', auth, name="auth"),
    path('sign_up/', sign_up, name="sign_up"),
    path('save_ticket/', save_ticket, name="save_ticket"),
    path('profile_view/', profile_view, name="profile_view"),
    path('bus_layout/<int:schedule_id>/', bus_layout, name='bus_layout'),
    path('delete_ticket/<int:ticket_id>/', delete_ticket, name='delete_ticket'),
]