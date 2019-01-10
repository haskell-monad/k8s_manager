# -*- coding: utf-8 -*-

from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators import csrf
from django.http import HttpResponseRedirect
import logging

from .models import Product, ProductVersion
from .forms import ProductVersionForm
from . import common

logger = logging.getLogger('django')


def build_context():
    context = {}
    context['version_status_list'] = common.version_status_list
    return context

def index(request,product_id):
    context = build_context()
    obj = Product.objects.get(pk=product_id)
    if not obj:
        return redirect('/product/index')
    listData = ProductVersion.objects.filter(product_id=product_id)
    
    context['listData'] = listData
    context['product_id'] = product_id
    return render(request, 'product_version/index.html', context)

def add(request,product_id):
    request.encoding = 'utf-8'
    context = build_context()
    if request.method == "POST":
        form = ProductVersionForm(request.POST)
        if form.is_valid():
             version = form.save(commit=False)
             version.create_user = "admin"
             version.product_id = product_id
             version.save()
        return HttpResponseRedirect("/product/version/"+product_id)
    else:
        form = ProductVersionForm()
    context['title'] = "新增"
    context['formUrl'] = "/product/version/add/"+product_id
    context['form'] = form
    return render(request, 'product_version/form.html', context)


def edit(request, pk):
    context = build_context()
    obj = ProductVersion.objects.get(pk=pk)
    if not obj:
        return redirect('/product/index')
    product_id = obj.product_id
    if request.method == "GET":
        form = ProductVersionForm(instance=obj)
        context['form'] = form
        context['title'] = "编辑"
        context['formUrl'] = "/product/version/edit/"+pk
        return render(request, 'product_version/form.html', context)
    else:
        form = ProductVersionForm(request.POST, instance=obj)
        if form.is_valid():
            version = form.save(commit=False)
            version.update_user = "admin"
            version.save()
        return redirect('/product/version/'+product_id)








