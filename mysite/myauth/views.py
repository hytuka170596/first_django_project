from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LogoutView
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import (
    login_required,
    permission_required,
    user_passes_test,
)
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    TemplateView,
    CreateView,
    UpdateView,
    ListView,
    DetailView,
)
from django.views import View
from django.utils.translation import gettext_lazy as _, ngettext
from django.db.models import Model
from django.forms.models import ModelForm
from django.views.decorators.cache import cache_page

from typing import List, Any
from random import random
from .forms import ProfileForm, RegisterForm
from .models import Profile


class HelloView(View):
    """
    A view that displays a welcome message and the number of products.

    Attributes:
        welcome_message (str): A translated welcome message.
    """

    welcome_message: str = _(message="Welcome hello world!")

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Handle GET requests to display the welcome message and product count.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            HttpResponse: An HTTP response containing the welcome message
                           and product count.
        """
        items_str: str = request.GET.get("items", default="0")
        items: int = int(items_str)
        product_line: str = ngettext(
            singular="one product", plural="{count} products", number=items
        ).format(count=items)

        return HttpResponse(
            "<h1>{welcome_message}</h1>\n<h2>{product_line}</h2>".format(
                welcome_message=self.welcome_message, product_line=product_line
            )
        )


class AboutMeView(TemplateView):
    """
    A view that renders the 'About Me' page.

    Attributes:
        template_name (str): The template to render.
        form_class (ProfileForm): The form class used in this view.
        model (Profile): The model associated with this view.
        success_url (str): URL to redirect after a successful form submission.
    """

    template_name: str = "myauth/about-me.html"
    form_class: ModelForm = ProfileForm
    model: Model = Profile
    success_url: str = reverse_lazy("myauth:about-me")


class ProfileListView(ListView):
    """
    A view that displays a list of user profiles.

    Attributes:
        template_name (str): The template to render for the profile list.
        context_object_name (str): The name of the context variable to
                                   use in the template.
        queryset (QuerySet): The queryset of profiles to display.
    """

    template_name: str = "myauth/profile-list.html"
    context_object_name: str = "profiles"
    queryset: List[Model] = Profile.objects.all()


class ProfileDetailsView(DetailView):
    """
    A view that displays details of a specific user profile.

    Attributes:
        template_name (str): The template to render for profile details.
        context_object_name (str): The name of the context variable to
                                   use in the template.
        model (Profile): The model associated with this view.

    Methods:
        test_func() -> bool: Determines if the current user has permission
                             to access this profile's details.
    """

    template_name: str = "myauth/profile-details.html"
    context_object_name: str = "profile"
    model: Model = Profile

    def get(self, request, *args, **kwargs) -> HttpResponse:
        """
        Checks if the user's details page is the personal page of the requester,
        then transfer to the about-me page
        """
        self.object = self.get_object()

        if request.user == self.object.user:
            return redirect(reverse("myauth:about-me"))

        return super().get(request, *args, **kwargs)

    def test_func(self) -> bool:
        """
        Check if the user has permission to access the profile details.

        Returns:
            bool: True if the user is staff or owns the profile; otherwise False.
        """
        self.object: Any = self.get_object()

        return self.request.user.is_staff or self.request.user == self.object.user


class ProfileUpdateView(UserPassesTestMixin, UpdateView):
    """
    A view for updating a user profile.

    Attributes:
        permission_required (str): The permission required to access this view.
        template_name (str): The template to render for updating profiles.
        model (Profile): The model associated with this view.
        form_class (ProfileForm): The form class used for updating profiles.
        success_url (str): URL to redirect after a successful update.

    Methods:
        test_func() -> bool: Determines if the current user has permission
                             to update this profile.
        form_valid(form) -> HttpResponse: Handles valid form submission
                                           and assigns the updater.
    """

    permission_required: str = "myauth:change_profile"
    template_name: str = "myauth/profile-update.html"
    model: Model = Profile
    form_class: ModelForm = ProfileForm
    success_url: str = reverse_lazy("myauth:about-me")

    def get_object(self, queryset=None):
        pk = self.kwargs.get("pk")
        print(f"Trying to retrieve Profile with PK: {pk}")
        return super().get_object(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.object
        return context

    def test_func(self) -> bool:
        """
        Check if the user has permission to update the profile.

        Returns:
            bool: True if the user is staff or owns the profile; otherwise False.
        """
        self.object: Any = self.get_object()

        return self.request.user.is_staff or self.request.user == self.object.user

    def form_valid(self, form) -> HttpResponse:
        """
        Handle valid form submission and set the updater field.

        Args:
            form (ProfileForm): The submitted form instance.

        Returns:
            HttpResponse: A response redirecting to the success URL after
                           successful form processing.
        """

        form.instance.updated_by = Profile.objects.get(user=self.request.user)
        form.save()
        return super().form_valid(form)


class RegisterView(CreateView):
    form_class: ModelForm = RegisterForm
    template_name: str = "myauth/register.html"
    success_url: str = reverse_lazy("myauth:about-me")
    model: Model = Profile

    def form_valid(self, form):
        response: HttpResponse = super().form_valid(form)

        username: str = form.cleaned_data.get("username")
        email: str = form.cleaned_data.get("email")
        first_name: str = form.cleaned_data.get("first_name")
        last_name: str = form.cleaned_data.get("last_name")
        password: str = form.cleaned_data.get("password1")
        sex: str = form.cleaned_data.get("sex")

        user: User = self.object
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.sex = sex
        user.save()

        Profile.objects.create(user=user, username=username)

        user = authenticate(request=self.request, username=username, password=password)
        login(request=self.request, user=user)

        return response


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect("/admin/")

        return render(request=request, template_name="myauth/login.html")

    username: str = request.POST["username"]
    password: str = request.POST["password"]

    user: User = authenticate(
        request=request,
        username=username,
        password=password,
    )
    if user is not None:
        login(request=request, user=user)
        return redirect("/admin/")

    return render(
        request=request,
        template_name="myauth/login.html",
        context={"error": "Invalid login credentials"},
    )


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request=request)
    return redirect(reverse_lazy("myauth:login"))
    # return redirect(reverse("myauth:login", args=()))


class MyLogoutView(LogoutView):
    template_name: str = "myauth/logout.html"
    next_page: str = reverse_lazy("myauth:login")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
        return redirect(reverse_lazy("myauth:login"))


@user_passes_test(lambda user: user.is_superuser)
def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response: HttpResponse = HttpResponse("Coockie set")
    response.set_cookie(
        "fizz",
        "buzz",
        max_age=3660,
    )
    return response


@cache_page(60 * 2)
def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value: request.COOKIES = request.COOKIES.get("fizz", "default value")
    return HttpResponse(
        'Cookie value: "{cookie_value}" + {random_value}'.format(
            cookie_value=value, random_value=random()
        )
    )


@permission_required(perm="myauth.view_profile", raise_exception=True)
def set_session_view(requset: HttpRequest) -> HttpResponse:
    requset.session["foobar"]: str = "spameggs"
    return HttpResponse("Session set!")


@login_required
def get_session_view(request: HttpRequest) -> HttpResponse:
    value: request.COOKIES = request.session.get("foobar", "default")
    return HttpResponse("Session value: '{session_value}'".format(session_value=value))


class FooBarView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({"foo": "bar", "spam": "eggs"})
