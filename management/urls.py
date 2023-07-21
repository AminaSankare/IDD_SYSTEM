from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('staff/login', views.registrarLogin, name='registrar_login'),
    path('staff/logout', views.registrarLogout, name='registrar_logout'),
    path('staff/dashboard', views.dashboard, name='dashboard'),
    path('staff/new_application', views.newApplication, name='new_application'),
    path('staff/archived_request', views.archivedRequest, name='archived_request'),
    path('staff/services', views.services, name='services'),
    path('staff/citizens_list', views.citizenList, name='citizenList'),
]
