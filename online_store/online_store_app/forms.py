from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import UserCustom


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = UserCustom
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = UserCustom
        fields = ("email",)
