from django import forms
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm

User = get_user_model()


# Docs: https://docs.djangoproject.com/en/5.1/topics/auth/customizing/#custom-users-and-the-built-in-auth-forms
class UserChangeForm(BaseUserChangeForm):
    class Meta(BaseUserChangeForm.Meta):
        model = User
        fields = ["first_name", "last_name", "username", "email"]


class UserCreationForm(admin_forms.UserCreationForm):
    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        fields = ["first_name", "last_name", "username", "email"]

    error_message = {
        "duplicate_username": "A user with that username already exists.",
        "duplicate_email": "A user with that email already exists.",
    }

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(self.error_message["duplicate_email"])
        return email

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(self.error_message["duplicate_username"])
        return username
