# -*- coding: utf-8 -*-

from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators import csrf
from django.http import HttpResponseRedirect
import logging
import json

from .models import KubeConfig, KubeCluster, InstallCheck,InstallStep
from .forms import KubeConfigForm
from django.forms.models import model_to_dict
from . import common
from k8s_manager.celery import app
from k8s_manager.tasks import k8s_prepare_install_env, k8s_config_ssh_login, k8s_import_install_package, k8s_init_depend,k8s_instll_etcd,k8s_install_docker,k8s_install_master, k8s_install_node,k8s_install_network,k8s_install_plugins,k8s_install_clear,k8s_install_custom,k8s_install_check_command,k8s_install_remove_node,k8s_install_harbor 

logger = logging.getLogger('django')


def filter_step_by_category(list,step_category):
    result = filter(lambda obj : obj.step_category == step_category,list)
    return result

# 安装集群页面
def install_index(request,pk):

    context = {}

    step_left_tree = InstallStep.objects.filter(step_category__in=common.category_list)
    
    command_list = InstallCheck.objects.all()
    # 左侧菜单选项
    context['k8s_prepare'] = filter_step_by_category(step_left_tree,common.INSTALL_STEP_CATEGORY[0][0])
    context['k8s_step'] = filter_step_by_category(step_left_tree,common.INSTALL_STEP_CATEGORY[1][0])
    context['k8s_install'] = filter_step_by_category(step_left_tree,common.INSTALL_STEP_CATEGORY[2][0])
    context['k8s_new_node'] = filter_step_by_category(step_left_tree,common.INSTALL_STEP_CATEGORY[3][0])
    context['install_plugins'] = filter_step_by_category(step_left_tree,common.INSTALL_STEP_CATEGORY[5][0])
    context['install_check'] = command_list
    context['kube_id'] = pk
    return render(request, 'install/index.html', context)



# 安装验证，帮助手册
def install_check(request):
    result = InstallCheck.objects.all()
    return HttpResponse(json.dumps(result,ensure_ascii=False),content_type="application/json,charset=utf-8")

# 安装命令
def install_command(request,pk,step_id):

    logging.debug("---------install_command(%s,%s)-------------" % (pk,step_id))
    result = {"status":"ok","data":"","step":step_id}
    
    kube_config = KubeConfig.objects.get(id=pk)
    install_step = InstallStep.objects.get(step_id=step_id)
    
    if not kube_config:
        result = {"status":"error","data":u"集群[%s]不存在" % pk}
    elif not install_step:
        result = {"status":"error","data":u"当前步骤不存在,请检查步骤[%s][%s]配置" % (pk,step_id)}
    else:
        current_step_id = kube_config.deploy_status
        dep_step_id = install_step.step_before
        if dep_step_id and current_step_id < dep_step_id:
            dep_install_step = InstallStep.objects.get(step_id=dep_step_id)
            result = {"status":"error","data": u"请先执行步骤[%s]-[%s]" % (dep_step_id,dep_install_step.step_name)}
        elif not install_step.step_function:
            result = {"status":"error","data":"当前步骤没有配置执行函数，请检查"}
        else:
            step_fun = install_step.step_function+".delay"
            step_id = int(step_id.encode("utf-8"))
            try:
                r = eval(step_fun)(pk,step_id)
                print("========install_command结果===========")
                print(r)
            except (NameError,KeyError):
                result = {"status":"error","data":u"请检查当前步骤[%s]-[%s]对应的函数[%s]是否配置正确" % (step_id,install_step.step_name,install_step.step_function)}  
            else:
                result = {"status":"ok","data":"执行步骤操作成功,请等待异步执行结果","step":step_id}
        
    return HttpResponse(json.dumps(result,ensure_ascii=False),content_type="application/json,charset=utf-8")


# 执行安装检测命令，用来验证安装是否正确
def install_check_command(request,pk,command_id):
    # todo 这里在执行验证命令前，需要判断下是否可以执行该验证命令，通过当前执行的步骤id
    # todo 应该根据集群id，链接到具体的集群上执行，这里默认在部署节点上执行了
    check_command = InstallCheck.objects.get(id=command_id)
    result = model_to_dict(check_command,exclude = ['id',"command_category"])
    json_data = json.dumps(result,ensure_ascii=False,indent=2)

    if check_command.command_exec == common.COMMON_STATUS[0][0]:
        s = k8s_install_check_command.delay(pk,command_id)
        print(s)
    return HttpResponse(json_data,content_type="application/json,charset=utf-8")

# 删除某个集群节点
def k8s_remove_node(request,pk,node_id):

    kube_cluster = KubeCluster.objects.get(id=node_id)
    result = {}
    if not kube_cluster:
        result = {"status":"error","data":"该节点不存在，不可以删除"}
    elif kube_cluster.install_type != common.COMMON_STATUS[0][0]:
        result = {"status":"error","data":"该节点未安装，不可以删除"}   
    elif kube_cluster.node_status == common.COMMON_STATUS[0][0]:
        result = model_to_dict(kube_cluster,exclude = ['id'])
        s = k8s_install_remove_node.delay(pk,node_id)
    else:
        result = {"status":"error","data":"该节点未部署，不可以删除"}

    return HttpResponse(json.dumps(result,ensure_ascii=False,indent=2),content_type="application/json,charset=utf-8")














