# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from celery import shared_task, task
from celery.utils.log import get_task_logger
import time
import os
from .models import KubeConfig, KubeCluster


log = get_task_logger("install")


def exec_system(command):
    log.debug("开始执行: %s" % command)
    result = os.system(command)
    log.debug("执行结果: (%s,%s)" % (result,command))
    return result

def exec_system_result(command):
    log.debug("开始执行命令: %s" % command)
    result = os.popen(command)
    log.debug("命令执行结果: (%s|%s)" % (result,command))


def k8s_check(kubeConfig,kubeCluster):
    bool error = False
    if kubeConfig.deploy == "yes":
        log.error("k8s集群[%s]已经部署过，不可以重复部署" % kube_id)
        error = True
    elif kubeCluster
    

    return error


# 生成host配置文件
def k8s_generate_hosts(kube_id):
    kube_config = KubeConfig.objects.filter(pk=pk).first()
    node_list = KubeCluster.objects.all()
    if not kube_config:
        log.error("k8s集群[%s]不存在" % kube_id)
        return
    elif not node_list:
        log.error("k8s集群[%s]" % kube_id)
        return

    k8s_check(kube_config)




# 准备安装环境
@task
def k8s_prepare_install_env(kube_id):
    c1 = exec_system("yum install epel-release git ansible -y")
    c2 = exec_system("which git && which ansible")
    if c2 == 0:
        c3 = exec_system("yum update -y")
        c4 = exec_system("git clone https://github.com/limengyu1990/k8s-cluster.git /tmp/k8s-cluster")
        if(c4 == 0):
            os.exec_system("rm -rf /etc/ansible/* && mv /tmp/k8s-cluster/* /etc/ansible/ && rm -rf /tmp/k8s-cluster")
            k8s_generate_hosts(kube_id)



            result = exec_system_result("ansible all -m ping")
        else:
            log.error("git clone 失败")
    else:
        log.error("安装 git/ansible 异常")



# 执行免密钥登陆
@task
def k8s_config_ssh_login():

    return ""


# 导入k8s二进制文件
@task
def k8s_import_install_package():

    return ""


# 安装依赖
@task
def k8s_init_depend():
    return ""

# 安装etcd集群
@task
def k8s_instll_etcd():
    return ""


# 安装docker
@task
def k8s_install_docker():
    return ""


# 安装master
@task
def k8s_install_master():
    return ""

# 安装node
@task
def k8s_install_node():
    return ""

# 安装network
@task
def k8s_install_network():
    return ""


# 安装插件
@task
def k8s_install_plugins():
    return ""



























