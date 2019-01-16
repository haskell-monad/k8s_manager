# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from celery import shared_task, task
from celery.utils.log import get_task_logger
import time
import os

log = get_task_logger("install")


# 准备安装环境
@task
def k8s_prepare_install_env():
    print("------------k8s_prepare_install_env------------------");
    c1 = os.system("yum install epel-release git ansible -y")
    c2 = os.system("which git && which ansible")
    if c2 == 0:
        c3 = os.system("yum update -y")
        c4 = os.system("git clone https://github.com/limengyu1990/k8s-cluster.git /tmp/k8s-cluster")
        if(c4 == 0):
            os.system("rm -rf /etc/ansible/* && mv /tmp/k8s-cluster/* /etc/ansible/ && rm -rf /tmp/k8s-cluster")
            result = os.popen("ansible all -m ping")
            log.info(result)
        else:
            log.error("git clone 失败")
    else:
        log.error("安装 git/ansible 异常")

    print("------------k8s_prepare_install_env--end----------------");


# 生成host配置文件
@task
def k8s_generate_hosts(ts_id):
    print "++++++++++++++++++++++++++++++++++++"
    print('jobs[ts_id=%s] running....' % ts_id)
    time.sleep(10.0)
    print('jobs[ts_id=%s] done' % ts_id)
    result = True
    return result

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



























