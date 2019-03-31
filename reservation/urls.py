from django.urls import path
from . import views

app_name = 'reservation'

urlpatterns = [
	path('', views.reservation_view, name='reservation_view'),
	path('reg',views.reservation_reg, name='reservation_reg'),
	path('send', views.reservaiton_send, name='reservaiton_send'),
	path('oauth', views.reservation_oauth, name='reservation_oauth'),
]