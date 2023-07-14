from datetime import date
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, authenticate, login, logout, update_session_auth_hash
from django.core.mail import send_mail
from django.conf import settings


# your views here.

def handle_not_found(request, exception):
    return render(request, 'page_404/404.html')
