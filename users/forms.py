from django import forms
from . import models


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "input", "placeholder": "Username"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "input", "placeholder": "Password"})
    )

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(username=username)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError(
                    "incorrect password"))
        except Exception as e:
            print(e)
            self.add_error("username", forms.ValidationError(
                "user does not exist"))


class SignUpForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "email", "username")
        widgets = {
            "first_name": forms.TextInput(
                attrs={"placeholder": "First Name"}
            ),
            "last_name": forms.TextInput(
                attrs={"placeholder": "Last Name"}
            ),
            "email": forms.EmailInput(attrs={"placeholder": "Email"}),
            "username": forms.TextInput(
                attrs={"placeholder": "Username"}
            ),
        }

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "input", "placeholder": "Password"})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "input", "placeholder": "Confirm Password"}
        )
    )

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        print(password, password1)
        if password != password1:
            self.add_error("password", forms.ValidationError(
                "Incorrect password"))
        else:
            return password

    def save(self, *args, **kwargs):
        try:
            username = self.cleaned_data.get("username")
            password = self.cleaned_data.get("password")
            user = super().save(commit=False)
            user.username = username
            user.set_password(password)
            user.save()
        except Exception as e:
            print(e)
            self.add_error("username", forms.ValidationError(
                "username is already being used"))
