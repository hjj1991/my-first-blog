from django.urls import path
from . import views

app_name = 'score'

urlpatterns = [
	path('score_view/', views.score_view, name='score_view'),
]