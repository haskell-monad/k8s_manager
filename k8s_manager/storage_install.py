# -*- coding: utf-8 -*-

from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators import csrf
from django.http import HttpResponseRedirect
import logging
import json

from .models import StorageConfig
from .forms import StorageConfigForm
from . import common

logger = logging.getLogger('django')


# storage 列表
def storage_list(request):
    listData = StorageConfig.objects.all()
    context = {}
    context['listData'] = listData
    return render(request, 'install_storage/list.html', context)

# 添加 storage
def add_storage(request):
    request.encoding = 'utf-8'
    context = {}
    if request.method == "POST":
        form = StorageConfigForm(request.POST)
        print("----add_storage-----")
        print(form.errors)
        if form.is_valid():
             kube = form.save(commit=False)
             kube.save()
        return HttpResponseRedirect('/k8s')
    else:
        form = StorageConfigForm()
    context['title'] = "新增_NFS"
    context['formUrl'] = "/storage/install/add"
    context['form'] = form
    return render(request, 'install_storage/form.html', context)


# 编辑 storage
def edit_storage(request,pk):
    context = {}
    obj = StorageConfig.objects.filter(pk=pk).first()
    if not obj:
        return redirect('/k8s')
    if request.method == "GET":
        form = StorageConfigForm(instance=obj)
        context['form'] = form
        context['title'] = "编辑_Storage"
        context['formUrl'] = "/storage/install/edit/"+pk
        return render(request, 'install_storage/form.html', context)
    else:
        form = StorageConfigForm(request.POST, instance=obj)
        if form.is_valid():
            kube = form.save(commit=False)
            kube.save()
        return redirect('/k8s')








