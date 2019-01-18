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
from k8s_manager.tasks import k8s_prepare_install_env, k8s_config_ssh_login, k8s_import_install_package, k8s_init_depend,k8s_instll_etcd,k8s_install_docker,k8s_install_master, k8s_install_node,k8s_install_network,k8s_install_plugins,k8s_install_clear 

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
    current_step_id = kube_config.deploy_status
    
    step_id = int(step_id.encode("utf-8"))

    # if current_step_id >= step_id:
    #     result = {"status":"error","data":"已经执行过该命令，无需重复执行"}
    if step_id == common.K8S_INSTALL_PRE[0][0]:
        s = k8s_prepare_install_env.delay(pk,step_id)
    elif step_id == common.K8S_INSTALL_PRE[1][0]:
        if current_step_id < common.K8S_INSTALL_PRE[0][0]:
            result = {"status":"error","data":"请先执行[ansible环境准备]操作"}
        else:
            s = k8s_config_ssh_login.delay(pk,step_id)
    elif step_id == common.K8S_INSTALL_PRE[2][0]:
        if current_step_id < common.K8S_INSTALL_PRE[1][0]:
            result = {"status":"error","data":"请先执行[自定义操作]操作"}
        else:
            s = k8s_install_custom.delay(pk,step_id)
    elif step_id == common.K8S_INSTALL_PRE[3][0]:
        if current_step_id < common.K8S_INSTALL_PRE[2][0]: 
            result = {"status":"error","data":"请先执行[免密钥登陆配置]操作"}
        else:
            s = k8s_import_install_package.delay(pk,step_id)
    elif step_id == common.K8S_INSTALL_STEP[0][0]:
        if current_step_id < common.K8S_INSTALL_PRE[3][0]:
            result = {"status":"error","data":"请先执行[导入k8s二进制文件]操作"}
        else:
            s = k8s_init_depend.delay(pk,step_id)
    elif step_id == common.K8S_INSTALL_STEP[1][0]:
        if current_step_id < common.K8S_INSTALL_STEP[0][0]:
            result = {"status":"error","data":"请先执行[安装准备]操作"}
        else:
            s = k8s_instll_etcd.delay(pk,step_id)
    elif step_id == common.K8S_INSTALL_STEP[2][0]:
        if current_step_id < common.K8S_INSTALL_STEP[1][0]: 
            result = {"status":"error","data":"请先执行[安装k8s-etcd]操作"}
        else:
            s = k8s_install_docker.delay(pk,step_id)
    elif step_id == common.K8S_INSTALL_STEP[3][0]:
        if current_step_id < common.K8S_INSTALL_STEP[2][0]:
            result = {"status":"error","data":"请先执行[安装k8s-docker]操作"}
        else:
            s = k8s_install_master.delay(pk,step_id)
    elif step_id == common.K8S_INSTALL_STEP[4][0]:
        if current_step_id < common.K8S_INSTALL_STEP[3][0]:
            result = {"status":"error","data":"请先执行[安装k8s-master]操作"}
        else:
            s = k8s_install_node.delay(pk,step_id)
    elif step_id == common.K8S_INSTALL_STEP[5][0]:
        if current_step_id < common.K8S_INSTALL_STEP[4][0]:
            result = {"status":"error","data":"请先执行[安装k8s-node]操作"}
        else:
            s = k8s_install_network.delay(pk,step_id)
    elif step_id == common.K8S_INSTALL_STEP[6][0]:
        if current_step_id < common.K8S_INSTALL_STEP[5][0]:
            result = {"status":"error","data":"请先执行[安装k8s-network]操作"}
        else:
            s = k8s_install_plugins.delay(pk,step_id)
    elif step_id == common.K8S_INSTALL[0]:
        if current_step_id < common.K8S_INSTALL_PRE[3][0]:
            result = {"status":"error","data":"请先执行[环境准备]操作"}
        else:
            print("一键安装")
    elif step_id == common.K8S_INSTALL_CLEAN[0]:
        s = k8s_install_clear.delay(pk,step_id)
    else:
        result = {"status":"error","data":"不支持该操作"}
        

    return HttpResponse(json.dumps(result,ensure_ascii=False),content_type="application/json,charset=utf-8")















