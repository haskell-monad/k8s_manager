# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from celery import shared_task, task
from celery.utils.log import get_task_logger
import time
import os
from .models import KubeConfig, KubeCluster, InstallCheck, InstallStep
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
    data = result.read()
    log.debug("命令执行结果[%s]: \n%s" % (command,data))
    return data

def update_kube_deploy_status(kube_id,step_id):
    # 获取到当前步骤的依赖步骤，然后根据步骤id更新
    install_step = InstallStep.objects.get(step_id=step_id)
    last_step_id = install_step.step_before
    log.debug("更新集群[%s]部署状态[%s,%s]" % (kube_id,last_step_id,step_id))
    KubeConfig.objects.filter(id=kube_id).filter(deploy_status=last_step_id).update(deploy_status=step_id)


# 用来验证集群部署时，每步部署的是否正确，通过执行相应的验证命令
@task
def k8s_install_check_command(kube_id,command_id):
    check_command = InstallCheck.objects.get(id=command_id)
    log.debug("开始执行集群部署[%s]验证命令[%s]: %s" % (kube_id,command_id,check_command.command))
    if not check_command:
        log.warn("安装验证命令不存在[%s]" % (command_id))
        return "安装验证命令不存在"
    result = exec_system_result(check_command.command)
    return result

# 准备安装环境
@task
def k8s_prepare_install_env(kube_id,step_id):
    log.debug("开始执行任务[%s:%s][ansible环境准备]" % (kube_id,step_id))
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
            c5 = exec_system("mkdir -p /etc/ansible && rm -rf /etc/ansible/* && mv /tmp/k8s-cluster/* /etc/ansible/  && rm -rf /tmp/k8s-cluster")
            if (c5 != 0):
                log.error("安装ansible异常")
                return 
        else:
            log.error("git clone 失败")
            return
    hf = k8s_generate_hosts(kube_id,common.K8S_DEPLOY_TYPE[0][0])
    if hf and os.path.exists("/etc/ansible/hosts"):
        result = exec_system("ansible all -m ping")
        if result == 0:
            exec_system_result("ansible all -m ping")
            # 任务成功执行
            update_kube_deploy_status(kube_id,step_id)
        else:
            log.debug("命令[%s:%s][ansible all -m ping]执行失败" % (kube_id,step_id))
        log.debug("任务[%s:%s][ansible环境准备]执行完成" % (kube_id,step_id))
    else:
        log.error("生成/etc/ansible/hosts失败")


# 执行免密钥登陆
@task
def k8s_config_ssh_login(kube_id,step_id):
    log.debug("开始执行任务[%s:%s][免密钥登陆]" % (kube_id,step_id))

    if not os.path.exists("/root/.ssh/id_rsa"):
        k = exec_system("ssh-keygen -N '' -f /root/.ssh/id_rsa")
        if k != 0:
            log.error("任务[%s:%s][免密钥登陆]执行失败,执行ssh-keygen失败" % (kube_id,step_id))
            return
    r = exec_system("ansible-playbook -i /etc/ansible/hosts /etc/ansible/_ssh.yml")
    if r == 0:
        update_kube_deploy_status(kube_id,step_id)
    else:
        log.error("任务[%s:%s][免密钥登陆]执行失败" % (kube_id,step_id))
    log.debug("任务[%s:%s][免密钥登陆]执行完成" % (kube_id,step_id))

# 执行自定义操作   
@task
def k8s_install_custom(kube_id,step_id):
    log.debug("开始执行任务[%s:%s][自定义操作]" % (kube_id,step_id))
    r = exec_system("ansible-playbook -i /etc/ansible/hosts /etc/ansible/_custom.yml")
    if r == 0:
        update_kube_deploy_status(kube_id,step_id)
    else:
        log.error("任务[%s:%s][自定义操作]执行失败" % (kube_id,step_id))
    log.debug("任务[%s:%s][自定义操作]执行完成" % (kube_id,step_id))

# 导入k8s二进制/镜像文件
# todo 这里需要增加判断，如果二进制/镜像文件已经存在的话，就不再走导入判断逻辑了
@task
def k8s_import_install_package(kube_id,step_id):
    log.debug("开始执行任务[%s:%s][导入k8s二进制/镜像文件]" % (kube_id,step_id))
    kube_config = KubeConfig.objects.get(id=kube_id)
    source_dir = kube_config.bin_dir
    exec_system("mkdir -p "+source_dir)
    target_dir = "/etc/ansible/bin"
    if not os.listdir(source_dir):
        log.warn("请先将k8s二进制文件放到[%s]目录下" % source_dir);
        return
    else:
        r = exec_system("cp -ur "+source_dir+"/* "+target_dir)
        if r != 0:
            log.error("任务[%s:%s][导入k8s二进制文件]执行失败" % (kube_id,step_id))
            return
    # 导入镜像文件
    source_image_dir = "/opt/kube/images"
    exec_system("mkdir -p "+source_image_dir)
    target_image_dir = "/etc/ansible/down"
    if not os.listdir(source_image_dir):
        log.warn("请先将k8s镜像文件放到[%s]目录下" % source_image_dir);
        return
    else:
        i = exec_system("cp -ur "+source_image_dir+"/* "+target_image_dir)
        if i != 0:
            log.error("任务[%s:%s][导入k8s镜像文件]执行失败" % (kube_id,step_id))
            return
    update_kube_deploy_status(kube_id,step_id)
    log.debug("任务[%s:%s][导入k8s二进制/镜像文件]执行完成" % (kube_id,step_id))



def install_template(kube_id,step_id,yml_file):
    install_step = InstallStep.objects.get(step_id=step_id)
    step_name = install_step.step_name
    log.debug("开始执行任务[%s:%s][%s]" % (kube_id,step_id,step_name))

    r = exec_system("ansible-playbook /etc/ansible/"+yml_file)
    if r == 0:
        if step_id <= common.K8S_INSTALL_COMPLETE_STEP:
            update_kube_deploy_status(kube_id,step_id)
        log.debug("任务[%s:%s][%s]执行完成" % (kube_id,step_id,step_name))
        return True
    else:
        log.error("任务[%s:%s][%s]执行失败" % (kube_id,step_id,step_name))
        return False

# 新增master
@task
def k8s_install_new_master(kube_id,step_id):
    kube_config = KubeConfig.objects.get(id=kube_id)
    if kube_config.deploy != common.COMMON_STATUS[0][0]:
        log.error("此集群还未部署，不可以新增master节点[%s:%s]" % (kube_id,step_id))
        return
    flag = k8s_generate_hosts(kube_id,common.K8S_DEPLOY_TYPE[1][0])
    if flag and os.path.exists("/etc/ansible/hosts"):
        r = install_template(kube_id,step_id,"21.addmaster.yml")
        if r:
            # 更新节点部署状态
            log.error("更新新增master节点状态为[已部署][%s:%s]" % (kube_id,step_id))
            KubeCluster.objects.filter(kube_id=kube_id).filter(node_type=common.K8S_NODE_TYPE[0][0]).filter(node_role=common.K8S_NODE_ROLE[0][0]).filter(install_type=common.COMMON_STATUS[0][0]).filter(node_status=common.K8S_NODE_STATUS[0][0]).update(node_status=common.K8S_NODE_STATUS[1][0])
        else:
            log.error("新增master节点失败[%s:%s]" % (kube_id,step_id))
    else:
       log.error("新增master节点失败,生成hosts文件异常[%s:%s]" % (kube_id,step_id))

# 新增node
@task
def k8s_install_new_node(kube_id,step_id):
    if kube_config.deploy != common.COMMON_STATUS[0][0]:
        log.error("此集群还未部署，不可以新增node节点[%s:%s]" % (kube_id,step_id))
        return
    flag = k8s_generate_hosts(kube_id,common.K8S_DEPLOY_TYPE[1][0])
    if flag and os.path.exists("/etc/ansible/hosts"):
        r = install_template(kube_id,step_id,"20.addnode.yml")
        if r:
            # 更新节点部署状态
            log.error("更新新增node节点状态为[已部署][%s:%s]" % (kube_id,step_id))
            KubeCluster.objects.filter(kube_id=kube_id).filter(node_type=common.K8S_NODE_TYPE[0][0]).filter(node_role=common.K8S_NODE_ROLE[1][0]).filter(install_type=common.COMMON_STATUS[0][0]).filter(node_status=common.K8S_NODE_STATUS[0][0]).update(node_status=common.K8S_NODE_STATUS[1][0])
        else:
            log.error("新增node节点失败[%s:%s]" % (kube_id,step_id))
    else:
       log.error("新增node节点失败,生成hosts文件异常[%s:%s]" % (kube_id,step_id))

@task
def k8s_install_remove_node(kube_id,node_id):
    kube_cluster = KubeCluster.objects.get(id=node_id)
    if not kube_cluster:
        log.error("节点不存在，不可以删除该节点[%s:%s]" % (kube_id,node_id))
        return
    node_ip = kube_cluster.node_ip
    cp = os.system("cp /etc/ansible/tools/clean_one_node.yml /etc/ansible/tools/clean_one_node_1.yml")
    if cp == 0 and os.path.exists("/etc/ansible/tools/clean_one_node_1.yml"):
        os.system("sed -i \"s/NODE_TO_DEL/"+node_ip+"/g\" /etc/ansible/tools/clean_one_node_1.yml")
        r = os.system("ansible-playbook /etc/ansible/tools/clean_one_node_1.yml")
        if r == 0:
            log.debug("删除k8s集群节点成功[%s:%s]" % (kube_id,node_ip))
        else:
            log.debug("执行删除k8s集群节点操作完成，请自行验证该节点是否已删除[%s:%s]" % (kube_id,node_ip))
        os.system("rm -rf /etc/ansible/tools/clean_one_node_1.yml")
        log.error("更新集群节点状态为[未部署][%s:%s]" % (kube_id,node_ip))
        KubeCluster.objects.filter(kube_id=kube_id).filter(install_type=common.COMMON_STATUS[0][0]).filter(node_status=common.K8S_NODE_STATUS[1][0]).update(node_status=common.K8S_NODE_STATUS[0][0])
    return

# 安装harbor
@task
def k8s_install_harbor(kube_id,step_id):
    print("%s : %s" % (kube_id,step_id))
    return

# 安全安装 helm（在线）
@task
def k8s_install_helm_online():
    return

# 安全安装 helm（离线）
@task
def k8s_install_helm_offline():
    return

# 安装jenkins
@task
def k8s_install_jenkins():
    return

# 安装Gitlab
@task
def k8s_install_gitlab():
    return


# 清理集群
@task
def k8s_install_clear(kube_id,step_id):
    install_step = InstallStep.objects.get(step_id=step_id)
    step_name = install_step.step_name
    log.debug("开始清理集群[%s:%s][%s]" % (kube_id,step_id,step_name))
    r = exec_system("ansible-playbook /etc/ansible/99.clean.yml")
    if r == 0:
        log.debug("成功清理集群[%s:%s]" % (kube_id,step_id))
    else:
        log.debug("清理集群失败[%s:%s]" % (kube_id,step_id))

# 安装依赖
@task
def k8s_init_depend(kube_id,step_id):
    install_template(kube_id,step_id,"01.prepare.yml")

# 安装etcd集群
@task
def k8s_instll_etcd(kube_id,step_id):
    install_template(kube_id,step_id,"02.etcd.yml")

# 安装docker
@task
def k8s_install_docker(kube_id,step_id):
    install_template(kube_id,step_id,"03.docker.yml")

# 安装master
@task
def k8s_install_master(kube_id,step_id):
    flag = install_template(kube_id,step_id,"04.kube-master.yml")
    if flag:
        # 更新节点状态为->已部署
        log.error("更新master节点状态为[已部署][%s:%s]" % (kube_id,step_id))
        KubeCluster.objects.filter(kube_id=kube_id).filter(node_type=common.K8S_NODE_TYPE[0][0]).filter(node_role=common.K8S_NODE_ROLE[0][0]).filter(install_type=common.COMMON_STATUS[0][0]).filter(node_status=common.K8S_NODE_STATUS[0][0]).update(node_status=common.K8S_NODE_STATUS[1][0])


# 安装node
@task
def k8s_install_node(kube_id,step_id):
    flag = install_template(kube_id,step_id,"05.kube-node.yml")
    if flag:
        # 更新节点状态为->已部署
        log.error("更新node节点状态为[已部署][%s:%s]" % (kube_id,step_id))
        KubeCluster.objects.filter(kube_id=kube_id).filter(node_type=common.K8S_NODE_TYPE[0][0]).filter(node_role=common.K8S_NODE_ROLE[1][0]).filter(install_type=common.COMMON_STATUS[0][0]).filter(node_status=common.K8S_NODE_STATUS[0][0]).update(node_status=common.K8S_NODE_STATUS[1][0])

# 安装network
@task
def k8s_install_network(kube_id,step_id):
    install_template(kube_id,step_id,"06.network.yml")

# 安装插件
@task
def k8s_install_plugins(kube_id,step_id):
    flag = install_template(kube_id,step_id,"07.cluster-addon.yml")
    if flag:
        # 更新集群部署状态->已完成
        log.error("更新集群部署节点状态为[已部署][%s:%s]" % (kube_id,step_id))
        KubeConfig.objects.filter(id=kube_id).update(deploy=common.COMMON_STATUS[0][0])


def filter_by_node_type(node_list,node_type):
    node_data = filter(lambda node: node.node_type == node_type,node_list)
    return node_data

def filter_by_node_role(install_node_list,node_role):
    node_data = filter(lambda node: node.node_role == node_role,install_node_list)
    return node_data

def filter_k8s_node(install_k8s_node_list,node_status,node_role):
    node_data = filter(lambda node: node.node_role == node_role and node.node_status == node_status,install_k8s_node_list)
    return node_data


# 生成host配置文件
def k8s_generate_hosts(kube_id,deploy_type):
    kube_config = KubeConfig.objects.get(id=kube_id)
    cluster_list = KubeCluster.objects.filter(kube_id=kube_id)
    install_cluster_list = filter(lambda node: node.install_type == common.COMMON_STATUS[0][0],cluster_list)
    if not kube_config:
        log.warn("k8s集群[%s]不存在" % kube_id)
        return False
    elif not install_cluster_list:
        log.warn("k8s集群[%s]节点配置缺失" % kube_id)
        return False
    elif kube_config.deploy == "yes":
        log.warn("k8s集群[%s]已经部署过，不可以重复部署" % kube_id)
        return False
    else:
        hosts_file = kube_config.base_dir + "/hosts"
        # filter install node
        k8s_list = filter_by_node_type(install_cluster_list,common.K8S_NODE_TYPE[0][0])

        k8s_old_master_list = []
        k8s_old_node_list = []
        k8s_new_master_list = []
        k8s_new_node_list = []

        if deploy_type == common.K8S_DEPLOY_TYPE[0][0]:
            # 初始部署
            k8s_old_master_list = filter_by_node_role(k8s_list,common.K8S_NODE_ROLE[0][0])
            k8s_old_node_list = filter_by_node_role(k8s_list,common.K8S_NODE_ROLE[1][0])
        else:
            # 新增节点部署
            k8s_old_master_list = filter_k8s_node(k8s_list,common.K8S_NODE_STATUS[1][0],common.K8S_NODE_ROLE[0][0])
            k8s_old_node_list = filter_k8s_node(k8s_list,common.K8S_NODE_STATUS[1][0],common.K8S_NODE_ROLE[1][0])

            k8s_new_master_list = filter_k8s_node(k8s_list,common.K8S_NODE_STATUS[0][0],common.K8S_NODE_ROLE[0][0])
            k8s_new_node_list = filter_k8s_node(k8s_list,common.K8S_NODE_STATUS[0][0],common.K8S_NODE_ROLE[1][0])

            if not k8s_new_master_list and not k8s_new_node_list:
                log.warn("新增节点失败,k8s集群[%s]新增节点缺失" % kube_id)
                return False 

        if not k8s_old_master_list:
            log.warn("k8s集群[%s]master节点缺失" % kube_id)
            return False

        if not k8s_old_node_list:
            log.warn("k8s集群[%s]node节点缺失" % kube_id)
            return False


        lb_node_list = filter_by_node_type(install_cluster_list,common.K8S_NODE_TYPE[1][0])

        etcd_node_list = filter_by_node_type(install_cluster_list,common.K8S_NODE_TYPE[2][0])

        harbor_node_list = filter_by_node_type(cluster_list,common.K8S_NODE_TYPE[3][0])

        log.debug("集群[%s]k8s-master节点配置: %s" % (kube_id,k8s_old_master_list))
        log.debug("集群[%s]k8s-node节点配置: %s" % (kube_id,k8s_old_node_list))
        log.debug("集群[%s]k8s-new-master节点配置: %s" % (kube_id,k8s_new_master_list))
        log.debug("集群[%s]k8s-new-node节点配置: %s" % (kube_id,k8s_new_node_list))
        log.debug("集群[%s]k8s-loadbalance节点配置: %s" % (kube_id,lb_node_list))
        log.debug("集群[%s]k8s-etcd节点配置: %s" % (kube_id,etcd_node_list))
        log.debug("集群[%s]k8s-harbor节点配置: %s" % (kube_id,harbor_node_list))

        # generate hosts file
        with open(hosts_file,'w') as f:
            # 时钟同步
            f.write("[deploy]\n")
            f.write("%s NTP_ENABLED=%s\n" % (kube_config.deploy_node,kube_config.ntp_enabled))
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
            for node in k8s_old_master_list:
                f.write("%s\n" % node.node_ip)
            f.write("\n\n")

            # k8s-node
            f.write("[kube-node]\n")
            for node in k8s_old_node_list:
                f.write("%s\n" % node.node_ip)
            f.write("\n\n")

            # harbor
            f.write("[harbor]\n")
            for node in harbor_node_list:
                f.write("%s HARBOR_DOMAIN=\"%s\" NEW_INSTALL=%s\n" % (node.node_ip,node.node_domain,node.install_type))
            f.write("\n\n")


            f.write("[new-master]\n")
            for node in k8s_new_master_list:
                f.write("%s\n" % node.node_ip)
            f.write("\n\n")

            f.write("[new-node]\n")
            for node in k8s_new_node_list:
                f.write("%s\n" % node.node_ip)
            f.write("\n\n")


            # ssh-login
            f.write("[ssh-addkey]\n")
            for node in install_cluster_list:
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

            return True

        return False
























