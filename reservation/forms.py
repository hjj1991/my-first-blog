from django import forms

from .models import Reservation
from django.core.exceptions import ValidationError


class ReservationReg(forms.ModelForm):
    VARIETYLIST = (
        (1, "커트"),
        (2, "면도"),
        (3, "수염정리"),
    )
    variety = forms.ChoiceField(
        choices=VARIETYLIST, 
        label='원하는 것',
        widget=forms.RadioSelect(
            attrs={ 'style' : "list-style-type: none;"
            
            }
        )
    )
    class Meta:
        model = Reservation
        fields = ['name',  'phone_num', 'variety', 'request_text']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '이름을 적어주세요'}),
            'phone_num': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '연락처를 적어주세요'}),
            'request_text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '요청사항을 적어주세요'}),
        }
        labels = {
            'name': '이름',
            'phone_num': '연락처',
            'request_text': '요청사항',
        }
