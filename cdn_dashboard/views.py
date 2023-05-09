from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render


def login(request: HttpRequest):
    if request.method == "POST":
        data = request.POST
        if data["username"] == "admin" and data["password"] == "password":
            response = HttpResponseRedirect(redirect_to="/")
            response.set_cookie(key="auth_token", value="token")
            return response

    return render(request=request, template_name="login.html", context={})


def index(request: HttpRequest):
    context = {}
    if "auth_token" in request.COOKIES:
        context["auth_token"] = request.COOKIES["auth_token"]

    return render(request=request,
                  template_name="index.html",
                  context=context)


def register(request: HttpRequest):
    return render(request=request, template_name="register.html", context={})


def logout(request: HttpRequest):
    response = HttpResponseRedirect(redirect_to="/")
    response.set_cookie(key="auth_token", value="", max_age=0.01)
    return response


def create(request: HttpRequest):
    if request.method == "POST":
        print("Hello world")
        print(request.POST)
        return HttpResponseRedirect(redirect_to="/")
    return render(request=request, template_name="create.html", context={})
