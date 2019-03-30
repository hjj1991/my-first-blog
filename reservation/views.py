from django.shortcuts import render
from .models import Reservation
from .forms import ReservationReg
from django.db.models import Q

# Create your views here.

def reservation_view(request):
	if request.method == "GET":
		reservation_date = request.GET.get('date', '')
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
				return render(request, 'reservation/reservation_done.html', {'result' : '예약이 완료되었습니다.'})
	else:
		date = request.GET.get('date', '')
		time = request.GET.get('time', '')

		form = ReservationReg()
		return render(request, 'reservation/reservation_reg.html', {'form': form, 'date': date, 'time': time })