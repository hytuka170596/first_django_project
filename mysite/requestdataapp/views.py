from collections.abc import Callable
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .forms import UploadForm
from loguru import logger as log
from functools import wraps


def too_many_requests_decorator(func: Callable):
    @wraps(func)
    def wrapper(request: HttpRequest, *args, **kwargs):

        if getattr(request, "is_rate_limited", False):
            log.warning(
                f"Rate limit exceeded for IP: {request.META.get('REMOTE_ADDR')}"
            )
            return render(request, "requestdataapp/too-many-requests.html", status=429)
        return func(request, *args, **kwargs)

    return wrapper


@too_many_requests_decorator
def process_get_view(request: HttpRequest) -> HttpResponse:
    """
    GET Request Handler.

    Args:
        request: The HttpRequest object containing the GET data.

    Returns:
        HttpResponse: The rendered HTML page displaying the concatenated result.
    """
    a = request.GET.get("a", "")
    b = request.GET.get("b", "")
    result = a + b
    context = {
        "result": result,
    }
    return render(
        request=request,
        template_name="requestdataapp/request-query-params.html",
        context=context,
    )


@too_many_requests_decorator
def user_form(request: HttpRequest) -> HttpResponse:
    """
    Renders a form for user bio submission.

    This view displays a form where users can submit their bio data.

    Args:
        request: The HttpRequest object.

    Returns:
        HttpResponse: The rendered HTML page containing the user bio form.
    """
    return render(
        request=request,
        template_name="requestdataapp/user-bio-form.html",
    )


@too_many_requests_decorator
def handle_file_upload(request: HttpRequest) -> HttpResponse:
    """
    Handles file upload via a POST request and saves the file.

    This view processes file uploads from a form. If a file is uploaded via POST,
    it is saved using Django's FileSystemStorage, and a log entry is made.

    Args:
        request: The HttpRequest object containing the uploaded file data.

    Returns:
        HttpResponse: The rendered HTML page with the file upload form.
    """
    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            # если не используются формы джанго, то можно использовать request.FILES напрямую
            # myfile = request.FILES["myfile"]

            myfile = form.cleaned_data["file"]

            if myfile.size > 1024 * 1024:
                return render(
                    request=request, template_name="requestdataapp/file-size-error.html"
                )
            fs = FileSystemStorage()
            filename = fs.save(name=myfile.name, content=myfile)
            log.info("saved file to " + filename)
    else:
        form = UploadForm()

    context = {
        "form": form,
    }
    return render(
        request=request,
        template_name="requestdataapp/file-upload.html",
        context=context,
    )
