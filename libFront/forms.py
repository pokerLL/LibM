from captcha.fields import CaptchaField
from django import forms


class loginForm(forms.Form):
    account = forms.CharField(label="账号", max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Account", 'autofocus': ''}))
    password = forms.CharField(label="密码", max_length=256,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Password"}))
    captcha = CaptchaField(label='验证码')
