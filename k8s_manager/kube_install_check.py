# -*- coding: utf-8 -*-

from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators import csrf
from django.http import HttpResponseRedirect
import logging
import json

from .models import InstallCheck
from .forms import InstallCheckForm
from . import common

logger = logging.getLogger('django')



# 安装验证命令列表
def check_command_list(request):
    listData = InstallCheck.objects.all()
    context = {}
    context['listData'] = listData
    return render(request, 'install_check/list.html', context)

# 新增_安装验证命令
def add_check_command(request):
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
def edit_check_command(request,pk):
    context = {}
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








