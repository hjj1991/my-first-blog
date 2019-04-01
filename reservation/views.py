from django.shortcuts import render
from .models import Reservation
from .forms import ReservationReg
from django.db.models import Q
from rest_framework import viewsets 
from .serializers import ReservationSerializer
import requests,json
from django.utils import timezone


# Create your views here.

# class ReservationViewSet(viewsets.ModelViewSet):
# 	queryset = Reservation.objects.all()
# 	serializer_class = ReservationSerializer


def reservation_oauth(request):
	code = str(request.GET.get('code'))
	url = "https://kauth.kakao.com/oauth/token"
	payload = "grant_type=authorization_code&client_id=656c5afa5455de8f5ad9eb51e09e3720&redirect_uri=http://211.217.41.72:8000/reservation/oauth&code=" + code
	headers = {
			'Content-Type' : "application/x-www-form-urlencoded",
			'Cache-Control' : "no-cache",
			}
	response = requests.request("POST", url, data=payload, headers= headers)
	access_token = json.loads(((response.text).encode('utf-8')))['access_token']


	item = {
	"object_type": "text", 
	"text": "텍스트 영역입니다. 최대 200자 표시 가능합니다.", 
	"link": {
		"web_url": "https://developers.kakao.com",
		"mobile_web_url": "https://developers.kakao.com"
	},
	"button_title": "바로 확인"
	}

	item_result = 'template_object=' + str(json.dumps(item))

	resp = requests.post("https://kapi.kakao.com/v2/api/talk/memo/default/send", 
				data=item_result,  # serialize the dictionary from above into json
				headers={
						# "Content-Type":"application/json",
						'Content-Type' : "application/x-www-form-urlencoded",
						'Cache-Control' : "no-cache",
						'Authorization': "Bearer " + str(access_token)
						})

	result = json.loads(((resp.text).encode('utf-8')))
	return render(request, 'reservation/reservation_result.html', {'resp': result})

def reservaiton_send(request):
	
	return render(request, 'reservation/reservation_send.html')


def reservation_view(request):
	if request.method == "GET":
		reservation_date = request.GET.get('date', '')
		if reservation_date != '':
			reservation_list = Reservation.objects.filter(reservation_date=reservation_date)
			ablelist = []
			reservation = []

			for a in reservation_list:
				reservation.append(a.reservation_time)


			for a in range(11, 21):
				if a not in reservation:
					ablelist.append(a)
			return render(request, 'reservation/reservation_view.html', {'ablelist' : ablelist, 'date' : reservation_date })

	return render(request, 'reservation/reservation_view.html')

def reservation_reg(request):
	if request.method == "POST":
		form = ReservationReg(request.POST)
		if form.is_valid():
			reserv_reg = form.save(commit=False)
			reserv_reg.reservation_date = request.POST.get('date')
			reserv_reg.reservation_time = request.POST.get('time')
			if Reservation.objects.filter(
				Q(reservation_date=request.POST.get('date')) & Q(reservation_time=request.POST.get('time'))
				):
				return render(request, 'reservation/reservation_done.html', {'result' : '예약이 실패되었습니다. (이미 예약된 시간입니다.)'})
			else:
				reserv_reg.save()
				if reserv_reg.variety == 1:
					vari = "커트"
				elif reserv_reg.variety == 2:
					vari = "면도"
				else:
					vari = "수염정리"

				url = "https://notify-api.line.me/api/notify"

				resrvation_message = "\n예약일자: " + reserv_reg.reservation_date + " " + reserv_reg.reservation_time + ":00 \n예약자: " + reserv_reg.name +"\n전화번호: " + reserv_reg.phone_num + "\n예약종류: " + vari + "\n요청사항: " + reserv_reg.request_text

				payload = {
						"message": resrvation_message
						# "imageFullsize": "http://211.217.41.72:8000/media/santa.jpg"
						}
				headers = {
					'Content-Type' : "application/x-www-form-urlencoded",
					'Cache-Control' : "no-cache",
					'Authorization' : "Bearer ePBI7jhhiJSlvfmEgkjjYCUOKqwYBmL6FLMKeGCO3MI",
				}
				reponse = requests.request("POST",url,data=payload, headers=headers)

				return render(request, 'reservation/reservation_done.html', {'result' : '예약이 완료되었습니다.'})
	else:
		date = request.GET.get('date', '')
		time = request.GET.get('time', '')

		form = ReservationReg()
		return render(request, 'reservation/reservation_reg.html', {'form': form, 'date': date, 'time': time })

	