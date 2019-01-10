# -*- coding: utf-8 -*-

from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators import csrf
from django.http import HttpResponseRedirect
import logging

from .models import Assets
from .forms import AssetsForm
from . import common

logger = logging.getLogger('django')


def build_context():
    context = {}
    context['type_list'] = common.type_list
    context['status_list'] = common.status_list
    return context

def index(request):
    context = build_context()

    listData = Assets.objects.all()

    
    context['listData'] = listData

    return render(request, 'assets/index.html', context)

def add(request):
    request.encoding = 'utf-8'
    context = build_context()
    if request.method == "POST":
        form = AssetsForm(request.POST)
        if form.is_valid():
             assets = form.save(commit=False)
             assets.createUser("admin")
             assets.save()
        return HttpResponseRedirect('/assets')
    else:
        form = AssetsForm()
    context['title'] = "新增"
    context['formUrl'] = "/assets/add"
    context['form'] = form
    return render(request, 'assets/form.html', context)


def edit(request, pk):
    logger.info("-----------edit assets----------"+pk)
    context = build_context()
    obj = Assets.objects.filter(pk=pk).first()
    if not obj:
        return redirect('/assets')
    if request.method == "GET":
        form = AssetsForm(instance=obj)
        context['form'] = form
        context['title'] = "编辑"
        context['formUrl'] = "/assets/edit/"+pk
        return render(request, 'assets/form.html', context)
    else:
        form = AssetsForm(request.POST, instance=obj)
        logger.info("-----------edit assets----------")
        logger.info(form)
        if form.is_valid():
            form.save()
        return redirect('/assets')








