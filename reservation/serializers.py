from rest_framework import serializers 
from .models import Reservation 


class ReservationSerializer(serializers.ModelSerializer):

	class Meta:
		model = Reservation # 모델 설정 fields = ('id','title','genre','year') # 필드 설정
		fields = ('name','phone_num','reservation_date','reservation_time', 'variety', 'reg_date') # 필드 설정
