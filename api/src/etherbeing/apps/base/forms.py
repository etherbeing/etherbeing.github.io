from django import forms
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.forms import CharField, HiddenInput

from .admin_auth import recaptcha_is_enabled, verify_recaptcha_token


class RecaptchaAdminAuthenticationForm(AdminAuthenticationForm):
    recaptcha_token = CharField(required=False, widget=HiddenInput())

    def clean(self):
        cleaned_data = super().clean()
        if recaptcha_is_enabled():
            token = cleaned_data.get("recaptcha_token", "")
            result = verify_recaptcha_token(
                token,
                action="admin_login",
                remoteip=self.request.META.get("REMOTE_ADDR"),
            )
            if not result.success:
                raise ValidationError(
                    "reCAPTCHA verification failed. Please try again.",
                    code="invalid_recaptcha",
                )
        return cleaned_data


class BootstrapSuperuserForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField(required=False)
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    def clean_username(self):
        username = self.cleaned_data["username"]
        User = get_user_model()
        if User.objects.filter(username=username).exists():
            raise ValidationError("A user with that username already exists.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("The two password fields did not match.")
        if password1:
            validate_password(password1)
        return cleaned_data

    def save(self):
        User = get_user_model()
        return User.objects.create_superuser(
            username=self.cleaned_data["username"],
            email=self.cleaned_data.get("email", ""),
            password=self.cleaned_data["password1"],
        )
