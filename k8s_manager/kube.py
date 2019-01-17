# -*- coding: utf-8 -*-

from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators import csrf
from django.http import HttpResponseRedirect
import logging
import json

from .models import KubeConfig, KubeCluster
from .forms import KubeConfigForm
from . import common

logger = logging.getLogger('django')


def build_context():
    context = {}
    context['type_list'] = common.type_list
    context['status_list'] = common.status_list
    return context

def index(request):
    context = build_context()

    listData = KubeConfig.objects.all()

    context['listData'] = listData

    return render(request, 'kube/index.html', context)

# 新增k8s集群配置
def add(request):
    request.encoding = 'utf-8'
    context = build_context()
    if request.method == "POST":
        form = KubeConfigForm(request.POST)
        print(form.errors)
        if form.is_valid():
             kube = form.save(commit=False)
             kube.create_user = "admin"
             kube.deploy_status = -100
             kube.save()

        return HttpResponseRedirect('/k8s')
    else:
        form = KubeConfigForm()

    context['title'] = "新增"
    context['formUrl'] = "/k8s/add"
    context['form'] = form
    return render(request, 'kube/form.html', context)

def edit(request, pk):
    context = build_context()
    obj = KubeConfig.objects.filter(pk=pk).first()
    if not obj:
        return redirect('/k8s')
    if request.method == "GET":
        form = KubeConfigForm(instance=obj)
        context['form'] = form
        context['title'] = "编辑"
        context['formUrl'] = "/k8s/edit/"+pk
        return render(request, 'kube/form.html', context)
    else:
        form = KubeConfigForm(request.POST, instance=obj)
        if form.is_valid():
            kube = form.save(commit=False)
            kube.create_user = "admin"
            kube.save()
        return redirect('/k8s')


# 安装集群页面
def install(request,pk):

    context = build_context()

    context['k8s_prepare'] = common.K8S_INSTALL_PRE
    context['k8s_install'] = common.K8S_INSTALL
    context['k8s_step'] = common.K8S_INSTALL_STEP
    context['k8s_clean'] = common.K8S_INSTALL_CLEAN
    context['kube_id'] = pk
    return render(request, 'install/index.html', context)














