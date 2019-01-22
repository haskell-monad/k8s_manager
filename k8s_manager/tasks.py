# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from celery import shared_task, task
from celery.utils.log import get_task_logger
import time
import os
from .models import KubeConfig, KubeCluster, InstallCheck, InstallStep, InstallLock
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
    last_step_id = install_step.last_step_id
    log.debug("更新集群[%s]节点部署状态deploy_status[%s ---> %s]" % (kube_id,last_step_id,step_id))
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

# 生成id_rsa
def before_generate_id_rsa(_kube_config,_install_step):
    if not os.path.exists("/root/.ssh/id_rsa"):
        k = exec_system("ssh-keygen -N '' -f /root/.ssh/id_rsa")
        if k != 0:
            log.error("任务[%s:%s][免密钥登陆]执行失败,执行ssh-keygen失败" % (kube_id,step_id))
            return False
    return True


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


# 执行步骤前，检测集群是否已经部署过
def before_check_k8s_deploy_status(_kube_config,_install_step):
    if _kube_config.deploy != common.COMMON_STATUS[0][0]:
        log.error("此集群还未部署，不可以执行相应操作[%s:%s]" % (_kube_config.id,_install_step.step_id))
        return False
    return True

# 基础步骤执行完后，更新集群部署状态deploy为：已部署
def after_update_kube_config_deploy_status(_kube_config,_install_step):
    kube_id = _kube_config.kube_id
    step_id = _install_step.step_id
    if step_id == common.K8S_INSTALL_COMPLETE_STEP:
        # 更新集群部署状态->已完成
        log.info("更新集群部署状态deploy为[已部署][%s:%s]" % (kube_id,step_id))
        KubeConfig.objects.filter(id=kube_id).update(deploy=common.COMMON_STATUS[0][0])

def after_update_kube_cluster_master_node_status(_kube_config,_install_step):
    kube_id = _kube_config.kube_id
    step_id = _install_step.step_id
    # 更新master节点状态为->已部署
    log.info("更新master节点状态为[已部署][%s:%s]" % (kube_id,step_id))
    KubeCluster.objects.filter(kube_id=kube_id).filter(node_type=common.K8S_NODE_TYPE[0][0]).filter(node_role=common.K8S_NODE_ROLE[0][0]).filter(install_type=common.COMMON_STATUS[0][0]).filter(node_status=common.K8S_NODE_STATUS[0][0]).update(node_status=common.K8S_NODE_STATUS[1][0])


def after_update_kube_cluster_node_node_status(_kube_config,_install_step):
    kube_id = _kube_config.kube_id
    step_id = _install_step.step_id
    # 更新node节点状态为->已部署
    log.info("更新node节点状态为[已部署][%s:%s]" % (kube_id,step_id))
    KubeCluster.objects.filter(kube_id=kube_id).filter(node_type=common.K8S_NODE_TYPE[0][0]).filter(node_role=common.K8S_NODE_ROLE[1][0]).filter(install_type=common.COMMON_STATUS[0][0]).filter(node_status=common.K8S_NODE_STATUS[0][0]).update(node_status=common.K8S_NODE_STATUS[1][0])


# 执行自定义函数
def exec_custom_function(_function,_kube_config,_install_step):
    if not _function:
        return
    try:
        rs = eval(_function)(_kube_config,_install_step)
        print("========exec_custom_function结果===========")
        print(rs)
    except (NameError,KeyError):
        log.error(u"执行自定义函数失败[%s][%s][%s],请检查函数名称是否配置正确" % (_kube_config.kube_name,_install_step.step_name,_function))
    else:
        log.debug(u"执行自定义函数成功[%s][%s][%s]" % (_kube_config.kube_name,_install_step.step_name,_function))


@task
def install_template(kube_id,step_id):
    kube_config = KubeConfig.objects.get(id=kube_id)
    install_step = InstallStep.objects.get(step_id=step_id)
    if not _kube_config:
        log.error("集群不存在,不可以执行相应操作")
        return False
    elif not _install_step:
        log.error("集群安装步骤不存在,不可以执行相应操作")
        return False
    before_fun = install_step.step_before_function
    after_fun = install_step.step_after_function
    step_name = install_step.step_name
    yml_file = install_step.step_yml_file

    log.debug("开始执行任务[%s:%s][%s]" % (kube_id,step_id,step_name))

    if before_fun:
        before_rs = exec_custom_function(before_fun,kube_config,install_step)
        if not before_rs:
            return False
    if yml_file:
        r = exec_system("ansible-playbook -i /etc/ansible/hosts /etc/ansible/"+yml_file)
        if r == 0:
            if step_id <= common.K8S_INSTALL_COMPLETE_STEP:
                update_kube_deploy_status(kube_id,step_id)
            if after_fun:
                exec_custom_function(after_fun,kube_config,install_step)
            log.debug("任务[%s:%s][%s]执行完成" % (kube_id,step_id,step_name))
            return True
        else:
            log.error("任务[%s:%s][%s]执行失败" % (kube_id,step_id,step_name))
            return False
    else:
        log.error("任务[%s:%s][%s]执行失败,yml文件缺失" % (kube_id,step_id,step_name))
        return False
    

# 检测集群是否已部署过，然后生成hosts文件
def before_generate_hosts_file(_kube_config,_install_step):
    flag = before_check_k8s_deploy_status(_kube_config,_install_step)
    if not flag:
        return False
    rs = k8s_generate_hosts(_kube_config.id,common.K8S_DEPLOY_TYPE[1][0])
    if not rs:
        return False
    elif not os.path.exists("/etc/ansible/hosts"):
        return False
    else:
        return True


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


# 检测harbor服务器是否配置
def before_check_harbor_config(_kube_config,_install_step):
    rs = before_check_k8s_deploy_status(_kube_config,_install_step)
    if not rs:
        return False
    kube_id = _kube_config.id
    harbor_list = KubeCluster.objects.filter(kube_id=kube_id).filter(node_type=common.K8S_NODE_TYPE[3][0])
    if not harbor_list:
        log.error("harbor节点没有配置,请先配置[%s]" % kube_id)
        return False
    new_node = filter(lambda obj : obj.node_status == common.K8S_NODE_STATUS[0][0],harbor_list)    
    if not new_node:
        log.error("已经部署过harbor,不可以重复部署[%s]" % kube_id)
        return False
    return True

# 更新harbor部署状态为：已部署
def after_update_harbor_install_status(_kube_config,_install_step):
    kube_id = _kube_config.id
    log.info("更新harbor部署状态为:已部署[%s]" % kube_id)
    KubeCluster.objects.filter(kube_id=kube_id).filter(node_type=common.K8S_NODE_TYPE[3][0]).filter(node_status=common.K8S_NODE_STATUS[1][0]).update(node_status=common.K8S_NODE_STATUS[0][0])

# 检测helm是否已经安装
def before_check_helm(_kube_config,_install_step):
    rs = before_check_k8s_deploy_status(_kube_config,_install_step)
    if not rs:
        return False
    if os.path.exists("/opt/kube/bin/helm"):
        log.error("helm已经安装,不可以重复安装[%s]" % kube_id)
        return False
    r = exec_system("which helm")
    if r == 0:
        log.error("helm已经安装,不可以重复安装[%s]" % kube_id)
        return False
    try:
        InstallLock.objects.create(kube_id=_kube_config.id,lock_key=common.HELM_LOCK_KEY)
    except Exception as e:
        log.error("helm正在安装,请稍后重试[%s]" % kube_id)
        return False
    return True

# 离线安装helm,准备配置文件
def before_install_helm_offline(_kube_config,_install_step):
    rs = before_check_helm(_kube_config,_install_step)
    if not rs:
        return False
    exec_system("mkdir -p /opt/helm-repo")
    r = exec_system("nohup helm serve --address 127.0.0.1:8879 --repo-path /opt/helm-repo &")
    if r != 0:
        log.error("启动helm repo server失败[%s]" % _kube_config.id)
        return False
    # 准备配置文件
    rp = os.system(u'sed -i ".bak" "s/^repo_url/#&/g" /etc/ansible/roles/helm/default/main.yml')
    os.system(u'echo "repo_url: http://127.0.0.1:8879" >> /etc/ansible/roles/helm/default/main.yml')
    return True

# 离线安装helm后，还原配置文件
def after_install_helm_offline(_kube_config,_install_step):
    # 删除添加的地址
    os.system('sed -i ".bak" "/repo_url: http:\\/\\/127.0.0.1:8879/d" /etc/ansible/roles/helm/default/main.yml')
    # 还原被注释的地址
    str = os.system(u'sed -i ".bak" "1,/^#repo_url/ s/^#//" /etc/ansible/roles/helm/default/main.yml')
    after_install_helm(_kube_config,_install_step)
    
# 安装helm完成后，释放锁
def after_install_helm(_kube_config,_install_step):
    InstallLock.objects.filter(kube_id=_kube_config.id).filter(lock_key=common.HELM_LOCK_KEY).delete()


@task
def install_nfs_server():
    # 需要生成两个文件，一个是：/etc/ansible/nfs-hosts 另一个是/etc/ansible/roles/nfs/default/main.yml
    #generate_nfs_hosts()

    exec_system("ansible-playbook -i /etc/ansible/nfs-hosts /etc/ansible/_nfs.yml")


# 安装jenkins前，检测配置
def before_install_jenkins(_kube_config,_install_step):
    rs = before_check_k8s_deploy_status(_kube_config,_install_step)
    if not rs:
        return False

# 安装traefik
@task
def k8s_install_traefik():
    return

# 安装jenkins
@task
def k8s_install_jenkins():
    return

# 安装Gitlab
@task
def k8s_install_gitlab():
    return


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

