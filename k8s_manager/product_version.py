# -*- coding: utf-8 -*-

from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators import csrf
from django.http import HttpResponseRedirect
import logging

from .models import ProdutVersion
from .forms import ProdutVersionForm
from . import common

logger = logging.getLogger('django')


def build_context():
    context = {}
    context['version_status_list'] = common.version_status_list
    return context

def index(request):
    context = build_context()

    listData = ProdutVersion.objects.all()

    
    context['listData'] = listData

    return render(request, 'product_version/index.html', context)

def add(request):
    request.encoding = 'utf-8'
    context = build_context()
    if request.method == "POST":
        form = ProdutForm(request.POST)
        if form.is_valid():
             product_version = form.save(commit=False)
             product_version.createUser("admin")
             product_version.save()
        return HttpResponseRedirect('/product/version')
    else:
        form = ProdutForm()
    context['title'] = "新增"
    context['formUrl'] = "/product/version/add"
    context['form'] = form
    return render(request, 'product_version/form.html', context)


def edit(request, pk):
    logger.info("-----------edit product_version----------"+pk)
    context = build_context()
    obj = Produt.objects.filter(pk=pk).first()
    if not obj:
        return redirect('/product/version')
    if request.method == "GET":
        form = ProdutForm(instance=obj)
        context['form'] = form
        context['title'] = "编辑"
        context['formUrl'] = "/product/version/edit/"+pk
        return render(request, 'product_version/form.html', context)
    else:
        form = ProdutForm(request.POST, instance=obj)
        logger.info("-----------edit product_version----------")
        logger.info(form)
        if form.is_valid():
            product_version = form.save(commit=False)
            product_version.updateUser("admin")
            product_version.save()
        return redirect('/product/version')








