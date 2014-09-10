# coding: utf-8
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.shortcuts import render, redirect

from aefat.auth.forms import SignUpForm
from aefat.feeds.models import Feed
from aefat.core.views import password


def login(request):
    error = ""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None :
            auth_login(request, user)
            if not request.POST.has_key('remember_me'):
                request.session.set_expiry(0)
            return redirect("/feeds")
        error = "Nom d'utilisateur ou mot de passe incorrect"
        return render(request, 'auth/login.html', {"error":error})
    else:
        return render(request, 'auth/login.html', {"error":error})
    
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if not form.is_valid():
            print form.errors
            return render(request, 'auth/signup.html', {'form': form})
        else:
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            User.objects.create_user(username=username, password=password, email=email)
            user = authenticate(username=username, password=password)
            auth_login(request, user)
            welcome_post = u'{0} a rejoint le réseau'.format(user.username, user.username)
            feed = Feed(user=user, post=welcome_post)
            feed.save()
            return redirect('/')
    else:
        return render(request, 'auth/signup.html', {'form': SignUpForm()})
