from django.urls import path
from typing import List
from .views import process_get_view, user_form, handle_file_upload

app_name = "requestdataapp"


urlpatterns: List[path] = [
    path("get/", process_get_view, name="get-view"),
    path("bio/", user_form, name="user-form"),
    path("upload/", handle_file_upload, name="file-upload"),
]
