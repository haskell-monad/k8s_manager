# -*- coding: utf-8 -*-

from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators import csrf
from django.http import HttpResponseRedirect
import logging
from django import forms
from .models import KubeConfig, KubeCluster
from .forms import KubeClusterForm
from django.db import models
from . import common

logger = logging.getLogger('django')


def build_context():
    context = {}
    return context

def index(request,kube_id):
    context = build_context()

    context['kube_id'] = kube_id
    context['listData'] = KubeCluster.objects.filter(kube_id=kube_id)

    return render(request, 'kube_cluster/index.html', context)

def add(request,kube_id):
    context = build_context()
    default_line = 0
    KubeClusterFormSet = forms.formset_factory(KubeClusterForm,extra=default_line,)

    if request.method == 'GET':
        formset = KubeClusterFormSet(initial = [{"kube_id":kube_id,"node_status":common.K8S_NODE_STATUS[0][0]}])
        context['title'] = "新增集群节点"
        context['formUrl'] = "/k8s/cluster/add/"+kube_id
        context['defalut_line'] = 1
        context['formset'] = formset
        return render(request,"kube_cluster/form.html",context)

    formset = KubeClusterFormSet(request.POST)
    context['formset'] = formset
    print("-------add cluster-----------")
    print(formset.errors)
    if formset.is_valid():
        flag = False  # 标志位
        for row in formset.cleaned_data:
            if row:
                # **表示将字典扩展为关键字参数
                res = KubeCluster.objects.create(**row)
                if res:  # 判断返回信息
                    flag = True

    return HttpResponseRedirect('/k8s/cluster/'+kube_id)


# def edit(request, pk):
#     context = build_context()
#     obj = KubeConfig.objects.filter(pk=pk).first()
#     if not obj:
#         return redirect('/k8s')
#     if request.method == "GET":
#         form = KubeClusterForm(instance=obj)
#         context['form'] = form
#         context['title'] = "编辑"
#         context['formUrl'] = "/k8s/edit/"+pk
#         return render(request, 'kube/form.html', context)
#     else:
#         form = KubeClusterForm(request.POST, instance=obj)
#         if form.is_valid():
#             kube = form.save(commit=False)
#             kube.create_user = "admin"
#             kube.save()
#         return redirect('/k8s')



