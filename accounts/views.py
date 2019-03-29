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
			#if form.cleaned_data['password'] == form.cleaned_data['verify_password']:
				#new_user = User.objects.create_user(**form.cleaned_data)
			new_user = User.objects.create_user(form.cleaned_data['username'],form.cleaned_data['email'],form.cleaned_data['password'])
			new_user.last_name = form.cleaned_data['last_name']
			new_user.first_name = form.cleaned_data['first_name']
			new_user.save()
			return redirect('home')
		else:
			return render(request, 'signup.html', {'form': form})
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

def myinfo(request, username):
	user_info = User.objects.filter(username=username)
	return render(request, 'myinfo.html', {'user_info' : user_info})