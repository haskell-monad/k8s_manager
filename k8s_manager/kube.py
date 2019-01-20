# -*- coding: utf-8 -*-

from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators import csrf
from django.http import HttpResponseRedirect
import logging
import json

from .models import KubeConfig, KubeCluster, InstallCheck
from .forms import KubeConfigForm, InstallCheckForm
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

# 新增k8s集群
def add(request):
    request.encoding = 'utf-8'
    context = build_context()
    if request.method == "POST":
        form = KubeConfigForm(request.POST)
        print(form.errors)
        if form.is_valid():
             kube = form.save(commit=False)
             kube.create_user = "admin"
             kube.deploy = common.COMMON_STATUS[1][0]
             kube.deploy_status = common.K8S_INSTALL_INIT_STEP
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

# 安装验证命令列表
def command_add_list(request):
    listData = InstallCheck.objects.all()
    context = {}
    context['listData'] = listData
    return render(request, 'install_check/list.html', context)

# 新增_安装验证命令
def command_add(request):
    request.encoding = 'utf-8'
    context = {}
    if request.method == "POST":
        form = InstallCheckForm(request.POST)
        if form.is_valid():
             kube = form.save(commit=False)
             kube.save()
        return HttpResponseRedirect('/k8s')
    else:
        form = InstallCheckForm()
    context['title'] = "新增验证命令"
    context['formUrl'] = "/k8s/command/add"
    context['form'] = form
    return render(request, 'install_check/form.html', context)


# 编辑_安装验证命令
def command_edit(request,pk):
    context = build_context()
    obj = InstallCheck.objects.filter(pk=pk).first()
    if not obj:
        return redirect('/k8s')
    if request.method == "GET":
        form = InstallCheckForm(instance=obj)
        context['form'] = form
        context['title'] = "编辑_安装验证命令"
        context['formUrl'] = "/k8s/command/edit/"+pk
        return render(request, 'install_check/form.html', context)
    else:
        form = InstallCheckForm(request.POST, instance=obj)
        if form.is_valid():
            kube = form.save(commit=False)
            kube.save()
        return redirect('/k8s')








