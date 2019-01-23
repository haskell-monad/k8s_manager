# -*- coding: utf-8 -*-

from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators import csrf
from django.http import HttpResponseRedirect
import logging
import json

from .models import NfsConfig
from .forms import NfsConfigForm
from . import common

logger = logging.getLogger('django')


# nfs 列表
def nfs_list(request):
    listData = InstallStep.objects.all()
    context = {}
    context['listData'] = listData
    return render(request, 'install_nfs/list.html', context)

# 添加 nfs
def add_nfs(request):
    request.encoding = 'utf-8'
    context = {}
    if request.method == "POST":
        form = NfsConfigForm(request.POST)
        print("----add_nfs-----")
        print(form.errors)
        if form.is_valid():
             kube = form.save(commit=False)
             kube.save()
        return HttpResponseRedirect('/k8s')
    else:
        form = NfsConfigForm()
    context['title'] = "新增_NFS"
    context['formUrl'] = "/nfs/install/add"
    context['form'] = form
    return render(request, 'install_nfs/form.html', context)


# 编辑 nfs
def edit_nfs(request,pk):
    context = {}
    obj = NfsConfig.objects.filter(pk=pk).first()
    if not obj:
        return redirect('/k8s')
    if request.method == "GET":
        form = NfsConfigForm(instance=obj)
        context['form'] = form
        context['title'] = "编辑_NFS"
        context['formUrl'] = "/nfs/install/edit/"+pk
        return render(request, 'install_nfs/form.html', context)
    else:
        form = NfsConfigForm(request.POST, instance=obj)
        if form.is_valid():
            kube = form.save(commit=False)
            kube.save()
        return redirect('/k8s')








