# -*- coding: utf-8 -*-


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
from . import home, assets, product, product_version, kube, kube_cluster, kube_install


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', home.index),

    #assets
    url(r'^assets$', assets.index),
    url(r'^assets/add$', assets.add),
    url(r'^assets/edit/(\d+)$', assets.edit),


    url(r'^product$', product.index),
    url(r'^product/add$', product.add),
    url(r'^product/edit/(\d+)$', product.edit),

    url(r'^product/version/(\d+)$', product_version.index),
    url(r'^product/version/add/(\d+)$', product_version.add),
   

    url(r'^k8s$', kube.index),
    url(r'^k8s/add$', kube.add),
    url(r'^k8s/edit/(\d+)$', kube.edit),
    # 安装页面
    url(r'^k8s/install/(\d+)$', kube.install),

    # 安装命令
    url(r'^k8s/install/command/(\d+)/(-?\d+)$', kube_install.install_command),

    url(r'^k8s/cluster/(\d+)$', kube_cluster.index),
    url(r'^k8s/cluster/add/(\d+)$', kube_cluster.add),
    # url(r'^k8s/cluster/edit/(\d+)$', kube_cluster.edit),


]
