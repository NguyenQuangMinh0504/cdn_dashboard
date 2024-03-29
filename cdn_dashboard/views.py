from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render
import secrets
import redis
import json
import pika

from .db import domain_table_rdb, total_bytes_sent_rdb, cache_key_setting_rdb
from .db import domain_table, user_table
from cdn_dashboard.utils import get_domain_cdn


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
            domains = []
            for domain in domain_table.find({"auth_token": auth_token}):
                domain_data = {}
                domain_name = domain["domain"]
                domain_data["name"] = domain_name
                domain_total_bytes_sent = total_bytes_sent_rdb.get(
                    get_domain_cdn(domain_name)
                    )

                if domain_total_bytes_sent is None:
                    domain_data["total_bytes_sent"] = 0

                else:
                    domain_data["total_bytes_sent"] = int(
                        domain_total_bytes_sent
                        )
                domains.append(domain_data)
            context["domains"] = domains
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
        domain_cdn = get_domain_cdn(domain)
        domain_table_rdb.set(name=domain_cdn, value=domain)
        cache_key_setting_rdb.set(name=domain_cdn, value=1)

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
        domain_cdn = get_domain_cdn(domain)
        domain_table_rdb.delete(domain_cdn)
        cache_key_setting_rdb.delete(domain_cdn)

        return HttpResponseRedirect(redirect_to="/")


def rule(request: HttpRequest):
    if request.method == "POST":
        print(request.POST)
        data = request.POST
        rule_table = redis.Redis(host="10.5.20.169", port=6378, db=4)
        domain_rule = json.loads(
            rule_table.get("saugau.edge.vccloud.vn").decode("utf-8")
            )
        if data["action"] == "ignore-query-string":
            domain_rule["rule:1"]["actions"] = [["ignore_query_string",
                                                 "",
                                                 ""]]

        elif data["action"] == "rewrite-url":
            domain_rule["rule:1"]["actions"] = [["url_rewrite",
                                                 data["source-pattern"],
                                                 data["destination"]]]

        if data["compare-method"] == "not-equal":
            domain_rule["rule:1"]["conditions"] = [
                ["request_method_not_equal", "", "GET"]
                ]
        elif data["compare-method"] == "equal":
            domain_rule["rule:1"]["conditions"] = [
                ["request_method_equal", "", "GET"]
                ]

        rule_table.set("saugau.edge.vccloud.vn", json.dumps(domain_rule))
        print(json.loads(
            rule_table.get("saugau.edge.vccloud.vn").decode("utf-8")
            )
            )

    context = {}
    if "auth_token" in request.COOKIES:
        auth_token = request.COOKIES["auth_token"]
        context["auth_token"] = auth_token

    return render(request=request, template_name="rule.html", context=context)


def setting(request: HttpRequest):
    context = {}

    if "auth_token" in request.COOKIES:
        auth_token = request.COOKIES["auth_token"]
        context["auth_token"] = auth_token

        if domain_table.count_documents({"auth_token": auth_token}) > 0:
            domains = []
            for domain in domain_table.find({"auth_token": auth_token}):
                domains.append(domain["domain"])
            print(domains)

            if request.method == "POST":
                domain_setting = request.POST
                cache_key_setting = 0
                if "querystring-cache-key" in domain_setting:
                    if "device-cache-key" in domain_setting:
                        cache_key_setting = 3
                    else:
                        cache_key_setting = 1
                else:
                    if "device-cache-key" in domain_setting:
                        cache_key_setting = 2
                    else:
                        cache_key_setting = 0
                for domain in domains:
                    cache_key_setting_rdb.set(name=get_domain_cdn(domain),
                                              value=cache_key_setting)

    return render(request=request,
                  template_name="setting.html",
                  context=context)


def cache_delete(request: HttpRequest):
    context = {}
    if "auth_token" in request.COOKIES:
        auth_token = request.COOKIES["auth_token"]
        context["auth_token"] = auth_token
        if request.method == "POST":

            # Publish cache delete message
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host="35.184.46.172",
                    credentials=pika.PlainCredentials("huststudent", "password")
                )
            )
            channel = connection.channel()
            channel.exchange_declare(exchange="cache_delete",
                                     exchange_type="fanout")
            for link in request.POST["delete-link-list"].splitlines():
                channel.basic_publish(exchange="cache_delete",
                                      routing_key="",
                                      body=link)
            connection.close()

    return render(request=request,
                  template_name="cache_delete.html", context=context)


def test(request: HttpRequest):
    if request.method == "POST":
        print(request.POST)
    return render(request=request, template_name="test.html", context={})
