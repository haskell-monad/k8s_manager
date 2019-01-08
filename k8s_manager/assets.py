# -*- coding: utf-8 -*-

from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators import csrf
from django.http import HttpResponseRedirect
import logging

from .models import Assets
from .forms import AssetsForm

service_list = ["内部服务器", "内部虚拟机", "阿里云", "腾讯云", "交换机", "防火墙"]
status_list = ["上架", "下架", "在线", "离线"]
logger = logging.getLogger('django')


def index(request):
    context = {}

    listData = Assets.objects.all()

    context['service_list'] = service_list
    context['status_list'] = status_list
    context['listData'] = listData

    return render(request, 'assets/index.html', context)

def add(request):
    request.encoding = 'utf-8'
    context = {}
    context['service_list'] = service_list
    context['status_list'] = status_list
    if request.method == "POST":
        form = AssetsForm(request.POST)
        logger.info("-----------add assets----------")
        logger.info(form.is_valid())
        if form.is_valid():
             form.save()
        return HttpResponseRedirect('/assets')
    else:
        form = AssetsForm()
    context['title'] = "新增"
    context['formUrl'] = "/assets/add"
    context['form'] = form
    return render(request, 'assets/addPage.html', context)


def edit(request, pk):
    logger.info("-----------edit assets----------"+pk)
    context = {}
    context['service_list'] = service_list
    context['status_list'] = status_list
    obj = Assets.objects.filter(pk=pk).first()
    if not obj:
        return redirect('/assets')
    if request.method == "GET":
        form = AssetsForm(instance=obj)
        context['assets'] = form
        context['title'] = "编辑"
        context['formUrl'] = "/assets/edit/"+pk
        return render(request, 'assets/editPage.html', context)
    else:
        form = AssetsForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
        return redirect('/assets')








