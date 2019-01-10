# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from . import common
# Create your models here.
# python manage.py migrate   # create table
# python manage.py makemigrations k8s_manager   # change model
# python manage.py migrate k8s_manager   # create table

class Assets(models.Model):

    productName = models.CharField(max_length=50)
    assetType = models.IntegerField(choices=common.TYPE_VALUE)
    status = models.IntegerField(choices=common.STATUS_VALUE)
    activeDate = models.DateField()
    createDate = models.DateField(auto_now_add=True)
    updateDate = models.DateField()
    createUser = models.CharField(max_length=20)
    updateUser = models.CharField(max_length=20)
    idc = models.CharField(max_length=200)
    cabinetNo = models.CharField(max_length=200)
    cabinetOrder = models.CharField(max_length=200)
    tags = models.CharField(max_length=200)

    class Meta:
        db_table = "assets"


class Product(models.Model):
    productName = models.CharField(max_length=50)
    productDesc = models.CharField(max_length=255)
    productStatus = models.CharField(max_length=50)
    productManager = models.CharField(max_length=20)
    productContact = models.CharField(max_length=50)

    devManager = models.CharField(max_length=20)
    devContact = models.CharField(max_length=50)
    qaManager = models.CharField(max_length=20)
    qaContact = models.CharField(max_length=50)
    safeManager = models.CharField(max_length=20)
    safeContact = models.CharField(max_length=50)

    onlineVersion = models.CharField(max_length=30)
    productWiki = models.CharField(max_length=200)

    createDate = models.DateField(auto_now_add=True)
    updateDate = models.DateField(auto_now = True)
    createUser = models.CharField(max_length=20)
    updateUser = models.CharField(max_length=20)

    lastOnline = models.DateField()
    productTags = models.CharField(max_length=255)

    class Meta:
        db_table = "product"


class ProductVersion(models.Model):
    productId = models.IntegerField()
    versionName = models.CharField(max_length=20)
    productManager = models.CharField(max_length=20)
    startTime = models.DateField()
    endTime = models.DateField()

    versionWiki = models.CharField(max_length=255)
    versionStatus = models.IntegerField()
    versionEnv = models.IntegerField()

    productContact = models.CharField(max_length=50)
    devManager = models.CharField(max_length=20)
    devContact = models.CharField(max_length=50)
    qaManager = models.CharField(max_length=20)
    qaContact = models.CharField(max_length=50)
    safeManager = models.CharField(max_length=20)
    safeContact = models.CharField(max_length=50)

    createDate = models.DateField(auto_now_add=True)
    updateDate = models.DateField(auto_now = True)
    createUser = models.CharField(max_length=20)
    updateUser = models.CharField(max_length=20)

    tags = models.CharField(max_length=255)

    class Meta:
        db_table = "product_version"


class KubeConfig(models.Model):
    # 集群名称/标识，如 Test
    kube_name = models.CharField(max_length=20)
    # 集群主版本号, 如 v1.8, v1.9, v1.10，v1.11, v1.12
    kube_version = models.IntegerField(choices=common.K8S_VERSION)
    # 集群部署模式：allinone, single-master, multi-master
    deploy_mode = models.IntegerField(choices=common.K8S_DEPLOY_MODE)
    
    # 集群是否安装 chrony 时间同步,yes/no
    ntp_enabled = models.CharField(max_length=10)

    # 负载均衡节点，多个使用分号分割， 安装 haproxy+keepalived
    lb_node = models.CharField(max_length=150)

    # etcd 节点,多个使用分号分割
    etcd_node = models.CharField(max_length=150)
    # etcd节点名称
    etcd_node_name_prefix = models.CharField(max_length=150)

    # master节点，多个使用分号分割
    kube_master = models.CharField(max_length=150)

    # node节点，多个使用分号分割
    kube_node = models.CharField(max_length=150)
    
    # harbor节点
    harbor_node = models.CharField(max_length=20)
    # harbor域名
    harbor_domain = models.CharField(max_length=100)
    # yes表示新建，no表示使用已有harbor服务器
    harbor_install = models.CharField(choices=common.COMMON_STATUS)

    # 预留组，后续添加master节点使用，多个使用分号分割
    kube_new_master = models.CharField(max_length=150)
    # 预留组，后续添加node节点使用，多个使用分号分割
    kube_new_node = models.CharField(max_length=150)

    # 是否自动配置免密钥
    ssh_addkey = models.CharField(choices=common.COMMON_STATUS)

    # 服务端口范围 (NodePort Range),如：20000-40000
    node_port_range = models.CharField(max_length=20)
    
    # master_ip即LB节点VIP地址，为区别与默认apiserver端口，设置VIP监听的服务端口8443
    # 公有云上请使用云负载均衡内网地址和监听端口
    master_ip = models.CharField(max_length=20)
    kube_api_server = models.CharField(max_length=100)

    # 集群网络插件，目前支持calico, flannel, kube-router, cilium
    cluster_network = models.CharField(choices=common.K8S_CLUSTER_NETWORK)

    # 服务网段 (Service CIDR），注意不要与内网已有网段冲突
    service_cidr = models.CharField(max_length=40)
    # POD 网段 (Cluster CIDR），注意不要与内网已有网段冲突
    cluster_cidr = models.CharField(max_length=40)
    # kubernetes 服务 IP (预分配，一般是 SERVICE_CIDR 中第一个IP)
    cluster_k8s_svc_ip = models.CharField(max_length=40)
    # 集群 DNS 服务 IP (从 SERVICE_CIDR 中预分配)
    cluster_dns_svc_ip = models.CharField(max_length=40)
    # 集群 DNS 域名
    cluster_dns_domain = models.CharField(max_length=40)

    # 集群basic auth 使用的用户名和密码
    basic_auth_user = models.CharField(max_length=40)
    basic_auth_pass = models.CharField(max_length=40)

    # 默认二进制文件目录
    bin_dir = models.CharField(max_length=40)
    # 证书目录
    ca_dir = models.CharField(max_length=40)
    # 部署目录，即 ansible 工作目录，建议不要修改
    base_dir = models.CharField(max_length=40)

    # 该集群是否已经部署
    deploy = models.IntegerField(choices=common.COMMON_STATUS)
    # 该集群部署错误信息
    deploy_error = models.CharField(max_length=255)
    # 集群描述信息
    kube_desc = models.CharField(max_length=255)

    createDate = models.DateField(auto_now_add=True)
    createUser = models.CharField(max_length=20)
    updateDate = models.DateField(auto_now = True)
    updateUser = models.CharField(max_length=20)

    class Meta:
        db_table = "kube_config"


class KubeCluster(models.Model):
    # 集群id，唯一标识
    kube_id = models.IntegerField(max_length=20)
    # 节点ip
    node_ip = models.CharField(max_length=20)
    # 节点域名
    node_domain = models.CharField(max_length=40)
    # 节点类型
    node_type = models.CharField(choices=common.TYPE_VALUE)
    # 节点用户名
    node_user = models.CharField(max_length=30)
    # 节点密码
    node_password = models.CharField(max_length=100)
    # 节点端口号
    node_port = models.IntegerField()
    # 节点主机名
    node_name = models.CharField(max_length=100)
    # 节点角色，如: master/backup
    node_role = models.CharField(choices=common.TYPE_VALUE)
    # 是否已经配置过ssh免密钥登陆
    ssh_enabled = models.IntegerField()
    # 创建日期
    createDate = models.DateField(auto_now_add=True)
    # 修改日期
    updateDate = models.DateField(auto_now = True)
    class Meta:
        db_table = "kube_cluster"


class Server(models.Model):
    id = models.IntegerField(primary_key=True)
    manageIp = models.CharField(max_length=255)
    sn = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    platform = models.CharField(max_length=255)
    version = models.CharField(max_length=40)
    cpuCount = models.IntegerField()
    cpuPhysicalCount = models.IntegerField()
    cpuModel = models.CharField(max_length=255)
    createDate = models.DateField(auto_now_add=True)
    updateDate = models.DateField(auto_now = True)
    createUser = models.CharField(max_length=20)
    updateUser = models.CharField(max_length=20)
    mac = models.CharField(max_length=255)
    serialNum = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    portNum = models.IntegerField()
    intranetIp = models.CharField(max_length=255)
    user = models.CharField(max_length=255)
    ip = models.CharField(max_length=255)
    port = models.IntegerField()
    desc = models.CharField(max_length=255)

    class Meta:
        db_table = "server"


class Template(models.Model):
    name = models.CharField(max_length=20)
    path = models.CharField(max_length=50)
    tag = models.CharField(max_length=100)
    status = models.IntegerField()
    createDate = models.DateField(auto_now_add=True)

    class Meta:
        db_table = "template"


class VersionEnv(models.Model):
    versionId = models.IntegerField()
    tag = models.CharField(max_length=255)
    env = models.IntegerField()
    imageType = models.IntegerField()
    deployType = models.IntegerField()
    createDate = models.DateField(auto_now_add=True)
    updateDate = models.DateField(auto_now = True)
    createUser = models.CharField(max_length=20)
    updateUser = models.CharField(max_length=20)

    class Meta:
        db_table = "version_env"
