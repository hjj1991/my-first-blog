from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )




class SignupForm(forms.ModelForm):
    verify_password = forms.CharField(
        label = '패스워드 확인', 
        widget=forms.PasswordInput( 
            attrs={
            'class': 'form-control',
            }
        )
    )
    class Meta:
        model = User
        fields = ['username',  'password', 'verify_password', 'email',  'last_name', 'first_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '15자 이내로 입력 가능합니다.'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '영문자 포함 최소 8문자를 포함해야 합니다.'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'username': '아이디',
            'password': '패스워드',
            'email': '이메일',
            'first_name': '이름',
            'last_name': '성'
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('아이디가 이미 사용중입니다')
        return username

    def clean_verify_password(self):
        password1 = self.cleaned_data.get('password')
        verify_password = self.cleaned_data.get('verify_password')
        try:
            validate_password(password1, self.instance)
        except forms.ValidationError as error:
            # Method inherited from BaseForm
            self.add_error('password', error)
        if password1 != verify_password:
            raise forms.ValidationError('패스워드가 일치하지 않습니다.')
        return verify_password

    #글자수 제한
    # def __init__(self, *args, **kwargs):
    #     super(SignupForm, self).__init__( *args, **kwargs)
    #     self.fields['username'].widgets.attrs['maxlength'] = 15
