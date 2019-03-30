from django.urls import path
from . import views

app_name = 'reservation'

urlpatterns = [
	path('', views.reservation_view, name='reservation_view'),
	path('reg',views.reservation_reg, name='reservation_reg'),
]