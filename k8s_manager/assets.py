# -*- coding: utf-8 -*-

from django.shortcuts import render

from .models import Assets

def index(request):
    context = {}

    service_list = ["内部服务器","内部虚拟机","阿里云","腾讯云", "交换机","防火墙"]
    status_list = ["上架","在线","离线","下架"]

    context['service_list'] = service_list
    context['status_list'] = status_list
    contect['listData'] = listData


    return render(request, 'assets/index.html', context)
