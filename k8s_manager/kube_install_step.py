# -*- coding: utf-8 -*-

from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators import csrf
from django.http import HttpResponseRedirect
import logging
import json

from .models import InstallStep
from .forms import InstallStepForm
from . import common

logger = logging.getLogger('django')



# 安装步骤列表
def step_list(request):
    listData = InstallStep.objects.all()
    context = {}
    context['listData'] = listData
    context['step_category_list'] = common.step_category_list
    return render(request, 'install_step/list.html', context)

# 添加 安装步骤
def add_step(request):
    request.encoding = 'utf-8'
    context = {}
    if request.method == "POST":
        form = InstallStepForm(request.POST)
        print("----add_step-----")
        print(form.errors)
        if form.is_valid():
             kube = form.save(commit=False)
             kube.save()
        return HttpResponseRedirect('/k8s')
    else:
        form = InstallStepForm()
    context['title'] = "新增_安装步骤"
    context['formUrl'] = "/k8s/install/step/add"
    context['form'] = form
    return render(request, 'install_step/form.html', context)


# 编辑 安装步骤
def edit_step(request,pk):
    context = {}
    obj = InstallCheck.objects.filter(pk=pk).first()
    if not obj:
        return redirect('/k8s')
    if request.method == "GET":
        form = InstallStepForm(instance=obj)
        context['form'] = form
        context['title'] = "编辑_安装步骤"
        context['formUrl'] = "/k8s/install/step/edit/"+pk
        return render(request, 'install_step/form.html', context)
    else:
        form = InstallStepForm(request.POST, instance=obj)
        if form.is_valid():
            kube = form.save(commit=False)
            kube.save()
        return redirect('/k8s')








