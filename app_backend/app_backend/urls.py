"""app_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import view, order_api, user_api
from django.contrib import admin


urlpatterns = [
    url(r'^$', view.render_hello),
    url(r'^orders$', order_api.fetch_orders),
    url(r'^specific$', order_api.fetch_specific_order),
    url(r'^new_order$', order_api.new_order),
    url(r'^order_plus$', order_api.order_plus),
    url(r'^order_done$', order_api.order_done),
    url(r'^sign_up$', user_api.user_sign_up),
    url(r'^log_in$', user_api.user_log_in)
]
