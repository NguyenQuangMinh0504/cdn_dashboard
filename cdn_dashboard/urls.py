"""cdn_dashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import login, index, register, logout, create, delete, rule, test

urlpatterns = [
    path('admin/', admin.site.urls),
    # path("login/", include("login.urls")),
    path(route="login/", view=login, name="login"),
    path(route="", view=index, name="index"),
    path(route="register/", view=register, name="register"),
    path(route="logout/", view=logout, name="logout"),
    path(route="create/", view=create, name="create"),
    path(route="delete/", view=delete, name="delete"),
    path(route="rule/", view=rule, name="rule"),
    path(route="test/", view=test, name="test"),
]
