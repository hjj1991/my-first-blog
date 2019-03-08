from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.exceptions import ValidationError
from django.shortcuts import render_to_response
from django.http import HttpResponse
from .forms import SignupForm


# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            return redirect('home')
        else:
            return render(request, 'signup.html', {'form': form, 'errors': '중복된 아이디입니다. 다시 시도해주세요.'})
    else:
        form = SignupForm()
        return render(request, 'signup.html', {'form': form})

def login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = auth.authenticate(username = username, password = password)
		if user is not None:
			auth.login(request, user)
			return redirect('home')
		else:
			return render(request, 'blog/home.html', {'some_flag': True})

def logout(request):
	auth.logout(request)
	return redirect('home')