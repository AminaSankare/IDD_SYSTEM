from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('citizen/', views.home, name='home'),
    path('citizen/all_services/', views.all_services, name='all_services'),
    path('citizen/all_services/<str:name>/',
         views.service_details, name='service_details'),
    path('citizen/all_services/<str:name>/application/',
         views.citizen_request, name='citizen_request'),
    path('contact_us/', views.contact_us, name='contact'),

    # staff
    path('staff/login/', views.registrarLogin, name='registrar_login'),
    path('staff/logout/', views.registrarLogout, name='registrar_logout'),
    path('staff/dashboard/', views.dashboard, name='dashboard'),
    path('staff/profile/', views.registrarProfile, name='profile'),
    path('staff/new_application/', views.newApplication, name='new_application'),
    path('staff/archived_request/', views.archivedRequest, name='archived_request'),
    path('staff/services/', views.services, name='services'),
    path('staff/services/<int:pk>/service_detail/',
         views.servicesEdit, name='service_detail'),
    path('staff/citizens/', views.citizenList, name='citizens'),
    path('staff/citizens/<int:pk>/citizen_detail/',
         views.citizenEdit, name='citizen_detail'),
]
