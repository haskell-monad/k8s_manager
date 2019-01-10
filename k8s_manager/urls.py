"""k8s_manager URL Configuration

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
from django.contrib import admin
from . import (home,assets,product,kube)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index$', home.index),

    #assets
    url(r'^assets$', assets.index),
    url(r'^assets/add$', assets.add),
    url(r'^assets/edit/(\d+)$', assets.edit),


    url(r'^product$', product.index),
    url(r'^product/add$', product.add),
    url(r'^product/edit/(\d+)$', product.edit),

    url(r'^kube$', kube.index),
]
