# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from celery import shared_task, task
from celery.utils.log import get_task_logger
import time
import os
from .models import KubeConfig, KubeCluster
from . import common

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


def filter_by_node_type(node_list,node_type):
    node_data = filter(lambda node: node.node_type == node_type,node_list)
    return node_data

def filter_by_node_role(node_list,node_role):
    node_data = filter(lambda node: node.node_role == node_role,node_list)
    return node_data

# 准备安装环境
@task
def k8s_prepare_install_env(kube_id,step_id):
    # todo 判断ansible环境是否已经存在
    c1 = exec_system("which git && which ansible")
    if c1 != 0:
        c2 = exec_system("yum install epel-release git ansible -y")
        if c2 != 0:
            log.error("安装ansible失败")
            return
        else:
            c3 = exec_system("yum update -y")

    if not os.path.exists("/etc/ansible/ansible.cfg"):
        c4 = exec_system("git clone https://github.com/limengyu1990/k8s-cluster.git /tmp/k8s-cluster")
        if(c4 == 0):
            c5 = exec_system("mkdir -p /etc/ansible && rm -rf /etc/ansible/* && mv /tmp/k8s-cluster/* /etc/ansible/ && rm -rf /tmp/k8s-cluster")
            if (c5 != 0):
                log.error("安装ansible异常")
                return 
        else:
            log.error("git clone 失败")
            return
    k8s_generate_hosts(kube_id)
    if os.path.exists("/etc/ansible/hosts"):
        result = exec_system_result("ansible all -m ping")
    else:
        log.error("生成/etc/ansible/hosts失败")



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


# 生成host配置文件
def k8s_generate_hosts(kube_id):
    kube_config = KubeConfig.objects.get(id=kube_id)
    node_list = KubeCluster.objects.filter(kube_id=kube_id).filter(node_status=common.K8S_NODE_STATUS[0][0])
    if not kube_config:
        log.warn("k8s集群[%s]不存在" % kube_id)
        return
    elif not node_list:
        log.warn("k8s集群[%s]节点配置缺失" % kube_id)
        return
    elif kube_config.deploy == "yes":
        log.warn("k8s集群[%s]已经部署过，不可以重复部署" % kube_id)
        return
    else:
        hosts_file = kube_config.base_dir + "/hosts"
        # filter install node
        k8s_list = filter_by_node_type(node_list,common.K8S_NODE_TYPE[0][0])   
        k8s_master_list = filter_by_node_role(k8s_list,common.K8S_NODE_ROLE[0][0])
        k8s_node_list = filter_by_node_role(k8s_list,common.K8S_NODE_ROLE[1][0])


        lb_node_list = filter_by_node_type(node_list,common.K8S_NODE_TYPE[1][0])

        etcd_node_list = filter_by_node_type(node_list,common.K8S_NODE_TYPE[2][0])

        harbor_node_list = filter_by_node_type(node_list,common.K8S_NODE_TYPE[3][0])

        log.debug("集群[%s]k8s-master节点配置: %s" % (kube_id,k8s_master_list))
        log.debug("集群[%s]k8s-node节点配置: %s" % (kube_id,k8s_node_list))
        log.debug("集群[%s]k8s-loadbalance节点配置: %s" % (kube_id,lb_node_list))
        log.debug("集群[%s]k8s-etcd节点配置: %s" % (kube_id,etcd_node_list))
        log.debug("集群[%s]k8s-harbor节点配置: %s" % (kube_id,harbor_node_list))

        # generate hosts file
        with open(hosts_file,'w') as f:
            # 时钟同步
            f.write("[deploy]\n")
            for node in node_list:
                f.write("%s NTP_ENABLED=%s\n" % (node.node_ip,node.ntp_enabled))
            f.write("\n\n")
            # etcd
            f.write("[etcd]\n")
            for node in etcd_node_list:
                f.write("%s NODE_NAME=%s\n" % (node.node_ip,node.node_name))
            f.write("\n\n")

            # loadbalance
            f.write("[lb]\n")
            for node in lb_node_list:
                f.write("%s LB_ROLE=%s\n" % (node.node_ip,node.node_role))
            f.write("\n\n")

            # k8s-master
            f.write("[kube-master]\n")
            for node in k8s_master_list:
                f.write("%s\n" % node.node_ip)
            f.write("\n\n")

            # k8s-node
            f.write("[kube-node]\n")
            for node in k8s_node_list:
                f.write("%s\n" % node.node_ip)
            f.write("\n\n")

            # harbor
            f.write("[harbor]\n")
            for node in harbor_node_list:
                f.write("%s HARBOR_DOMAIN=\"%s\" NEW_INSTALL=%s\n" % (node.node_ip,node.node_domain,node.install_type))
            f.write("\n\n")

            # ssh-login
            f.write("[ssh-addkey]\n")
            for node in node_list:
                f.write("%s ansible_ssh_user=\"%s\" ansible_ssh_pass=\"%s\" ansible_ssh_port=\"%s\"\n" % (node.node_ip,node.node_user,node.node_password,node.node_port))
            f.write("\n\n")

            # [all:vars]
            f.write("[all:vars]\n")
            f.write("DEPLOY_MODE=%s\n" % kube_config.deploy_mode)
            f.write("K8S_VER=\"%s\"\n" % kube_config.kube_version)
            f.write("MASTER_IP=\"%s\"\n" % kube_config.master_ip)
            f.write("KUBE_APISERVER=\"%s\"\n" % kube_config.kube_api_server)

            f.write("CLUSTER_NETWORK=\"%s\"\n" % kube_config.cluster_network)
            f.write("SERVICE_CIDR=\"%s\"\n" % kube_config.service_cidr)
            f.write("CLUSTER_CIDR=\"%s\"\n" % kube_config.cluster_cidr)
            f.write("NODE_PORT_RANGE=\"%s\"\n" % kube_config.node_port_range)

            f.write("CLUSTER_KUBERNETES_SVC_IP=\"%s\"\n" % kube_config.cluster_k8s_svc_ip)
            f.write("CLUSTER_DNS_SVC_IP=\"%s\"\n" % kube_config.cluster_dns_svc_ip)
            f.write("CLUSTER_DNS_DOMAIN=\"%s\"\n" % kube_config.cluster_dns_domain)

            f.write("BASIC_AUTH_USER=\"%s\"\n" % kube_config.basic_auth_user)
            f.write("BASIC_AUTH_PASS=\"%s\"\n" % kube_config.basic_auth_pass)

            f.write("bin_dir=\"%s\"\n" % kube_config.bin_dir)
            f.write("ca_dir=\"%s\"\n" % kube_config.ca_dir)
            f.write("base_dir=\"%s\"\n" % kube_config.base_dir)

























