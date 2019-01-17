# -*- coding: utf-8 -*-

from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators import csrf
from django.http import HttpResponseRedirect
import logging
import json

from .models import KubeConfig, KubeCluster
from .forms import KubeConfigForm
from . import common

from k8s_manager.celery import app
from k8s_manager.tasks import k8s_prepare_install_env

logger = logging.getLogger('django')


def build_context():
    context = {}
    return context


# 安装命令
def install_command(request,pk,step_id):

    logging.debug("---------install_command(%s,%s)-------------" % (pk,step_id))
    context = build_context()
    result = {"status":"ok","data":"","step":step_id}
    # return HttpResponse(json.dumps(result,ensure_ascii=False),content_type="application/json,charset=utf-8")

    kube_config = KubeConfig.objects.get(id=pk)
    if kube_config.deploy_status >= step_id:
        result = {"status":"error","data":"已经部署过，不可以重复部署"}
    else:
        k8s_prepare_install_env.delay(pk,step_id);

    return HttpResponse(json.dumps(result,ensure_ascii=False),content_type="application/json,charset=utf-8")















