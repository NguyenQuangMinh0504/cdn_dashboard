from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render
import secrets
import redis
import json

from .db import domain_table, domain_table_rdb, user_table
from cdn_dashboard.utils import get_domain_slug


def login(request: HttpRequest):
    if request.method == "POST":
        data = request.POST
        user = user_table.find_one({"username": data["username"],
                                    "password": data["password"]})
        if user is not None:
            response = HttpResponseRedirect(redirect_to="/")
            response.set_cookie(key="auth_token", value=user["auth_token"])
            return response

    return render(request=request, template_name="login.html", context={})


def index(request: HttpRequest):
    context = {}
    if "auth_token" in request.COOKIES:
        auth_token = request.COOKIES["auth_token"]
        context["auth_token"] = auth_token

        if domain_table.count_documents({"auth_token": auth_token}) > 0:
            context['domains'] = []
            for domain in domain_table.find({"auth_token": auth_token}):
                context['domains'].append(domain)

    return render(request=request,
                  template_name="index.html",
                  context=context)


def register(request: HttpRequest):
    if request.method == "POST":
        data = request.POST
        auth_token = secrets.token_hex(16)
        user_table.insert_one(
            {"username": data["username"],
             "email": data["email"],
             "password": data["password"],
             "auth_token": auth_token,
             }
            )
        response = HttpResponseRedirect(redirect_to="/")
        response.set_cookie(key="auth_token", value=auth_token)
        return response
    return render(request=request, template_name="register.html", context={})


def logout(request: HttpRequest):
    response = HttpResponseRedirect(redirect_to="/")
    response.set_cookie(key="auth_token", value="", max_age=0.01)
    return response


def create(request: HttpRequest):

    context = {}

    if request.method == "POST":
        domain = request.POST["domain"]

        domain_table.insert_one(
            {"auth_token": request.COOKIES["auth_token"],
             "domain": domain}
            )

        domain_slug = get_domain_slug(domain)

        domain_table_rdb.set(name=domain_slug + ".sapphirecdn.com",
                             value=domain)

        return HttpResponseRedirect(redirect_to="/")

    if "auth_token" in request.COOKIES:
        auth_token = request.COOKIES["auth_token"]
        context["auth_token"] = auth_token

    return render(request=request,
                  template_name="create.html",
                  context=context)


def delete(request: HttpRequest):
    if request.method == "POST":
        data = request.POST
        domain = data["domain"]
        domain_table.delete_many({"domain": domain})
        domain_slug = get_domain_slug(domain)
        domain_table_rdb.delete(domain_slug + ".sapphirecdn.com")

        return HttpResponseRedirect(redirect_to="/")


def rule(request: HttpRequest):
    if request.method == "POST":
        print(request.POST)
        rule_table = redis.Redis(host="10.5.20.169", port=6378, db=4)
        domain_rule = json.loads(rule_table.get("saugau.com").decode("utf-8"))
        print(request.POST["action"])
        print(domain_rule.get("saugau.com"))

    context = {}
    if "auth_token" in request.COOKIES:
        auth_token = request.COOKIES["auth_token"]
        context["auth_token"] = auth_token

    return render(request=request, template_name="rule.html", context=context)


def setting(request: HttpRequest):
    context = {}
    if request.method == "POST":

        rule_table = redis.Redis(host="10.5.20.169", port=6378, db=4)
        domain_rule = json.loads(rule_table.get("saugau.com").decode("utf-8"))
        print(request.POST)
        if "querystring-cache-key" in request.POST:
            domain_rule["cache_key"] = 5
        else:
            domain_rule["cache_key"] = 4
        rule_table.set("saugau.com", json.dumps(domain_rule))
        print(json.loads(rule_table.get("saugau.com").decode("utf-8")))

    if "auth_token" in request.COOKIES:
        auth_token = request.COOKIES["auth_token"]
        context["auth_token"] = auth_token
    return render(request=request,
                  template_name="setting.html",
                  context=context)


def test(request: HttpRequest):
    if request.method == "POST":
        print(request.POST)
    return render(request=request, template_name="test.html", context={})
