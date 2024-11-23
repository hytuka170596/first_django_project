"""
Module for handling forms profile users.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Profile
from django.utils.translation import gettext_lazy as _
from django.db.models import Model

from typing import List, Dict

GENDER_CHOICES = [
    ("-", _("--Choose a gender--")),
    ("male", _("Male")),
    ("female", _("Female")),
]


class ProfileForm(forms.ModelForm):
    """
    A form for creating and updating user profiles.

    This ModelForm is based on the Profile model and includes fields
    for the user's username, first name, last name, email, bio,
    and avatar. It also provides translated labels for each field.

    Attributes:
        Meta (class): Inner class that defines the model and fields
                      associated with this form.
    """

    class Meta:
        model: Model = Profile
        fields: List[str] = [
            "username",
            "sex",
            "first_name",
            "last_name",
            "email",
            "bio",
            "avatar",
        ]
        labels: Dict[str, str] = {
            "username": _("Username"),
            "first_name": _("First Name"),
            "last_name": _("Last Name"),
            "email": _("Email"),
            "bio": _("Bio"),
            "avatar": _("Avatar"),
        }


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        label=_("Username"),
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": _("Enter your username")}
        ),
    )
    sex = forms.ChoiceField(
        choices=GENDER_CHOICES,
        label=_("Gender"),
        widget=forms.Select(attrs={"class": "form-control"}),
        required=True,
    )
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": _("Enter your email")}
        ),
    )
    first_name = forms.CharField(
        max_length=30,
        label=_("First Name"),
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": _("Enter your first name")}
        ),
        required=False,
    )
    last_name = forms.CharField(
        max_length=30,
        label=_("Last Name"),
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": _("Enter your last name")}
        ),
        required=False,
    )
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": _("Enter your password")}
        ),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": _("Confirm your password")}
        ),
    )
    bio = forms.CharField(
        label=_("Bio"),
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": _("Tell us about yourself"),
                "rows": 3,
            }
        ),
        required=False,
    )
    avatar = forms.ImageField(
        label=_("Avatar"),
        required=False,
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("The two password fields must match."))

        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if username and Profile.objects.filter(username=username).exists():
            raise forms.ValidationError(_("This username is already taken."))
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and Profile.objects.filter(email=email).exists():
            raise forms.ValidationError(_("This email is already taken."))
        return email

    def clean_sex(self):
        sex = self.cleaned_data.get("sex")
        if sex == "-":
            raise forms.ValidationError(_("Please choose a gender."))
        return sex
