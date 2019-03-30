from django.db import models
from django.utils import timezone

# Create your models here.


class Reservation(models.Model):
	name = models.CharField(max_length=50)
	phone_num = models.CharField(max_length=50)
	reservation_date = models.CharField(max_length=50)
	reservation_time = models.IntegerField()
	variety = models.IntegerField()
	reg_date = models.DateTimeField(
            default=timezone.now)

	def __str__(self):
		return self.name
