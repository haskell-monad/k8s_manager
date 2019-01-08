# -*- coding: utf-8 -*-

from django.shortcuts import render


def index(request):
    context = {}
    context['hello'] = "Hello World!"
    return render(request, 'kube/index.html', context)
