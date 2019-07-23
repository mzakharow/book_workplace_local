from django.contrib.auth.views import LogoutView
from django.urls import path
from booking.views import index, login_view, reserve_view, unreserve_view, vacant_view

urlpatterns = [
    path('', index, name='index'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),
    path('reserve/<path:str_date>', reserve_view, name='reserve'),
    path('unreserve/<path:str_date>', unreserve_view, name='unreserve'),
    path('vacant/<path:start_date>/<path:finish_date>/', vacant_view, name='vacant'),
]