# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
# python manage.py migrate   # create table
# python manage.py makemigrations k8s_manager   # change model
# python manage.py migrate k8s_manager   # create table

class Assets(models.Model):
	productName = models.CharField(max_length=50)
	assetType = models.IntegerField()
	status = models.IntegerField()
	activeDate = models.DateField()
	createDate = models.DateField(auto_now_add=True)
	updateDate = models.DateField()
	createUser = models.CharField(max_length=20)
	updateUser = models.CharField(max_length=20)
	idc = models.CharField(max_length=255)
	cabinetNo = models.CharField(max_length=255)
	cabinetOrder = models.CharField(max_length=255)
	tags = models.CharField(max_length=255)
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
	updateDate = models.DateField()
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
	updateDate = models.DateField()
	createUser = models.CharField(max_length=20)
	updateUser = models.CharField(max_length=20)

	tags = models.CharField(max_length=255)
	class Meta:
		db_table = "product_version"


class KubeConfig(models.Model):
	kubeName = models.CharField(max_length=255)
	kubeVersion = models.CharField(max_length=255)
	kubeCniVersion = models.CharField(max_length=255)
	etcdVersion = models.CharField(max_length=255)
	dockerVersion = models.CharField(max_length=255)
	netMode = models.CharField(max_length=255)
	clusterIP = models.CharField(max_length=255)
	serviceClusterIP = models.CharField(max_length=255)
	dnsIP = models.CharField(max_length=255)
	dnsDN = models.CharField(max_length=255)
	kube_api_ip = models.CharField(max_length=255)
	ingressVIP = models.CharField(max_length=255)
	sshUser = models.CharField(max_length=255)
	sshPort = models.CharField(max_length=255)
	masterAddress = models.CharField(max_length=255)
	masterHostName = models.CharField(max_length=255)
	nodeHostName = models.CharField(max_length=255)
	etcdAddress = models.CharField(max_length=255)
	yamlDir = models.CharField(max_length=255)
	nodePort = models.CharField(max_length=255)
	kubeToken = models.CharField(max_length=255)
	loadBalance = models.CharField(max_length=255)
	kubeDesc = models.CharField(max_length=255)
	createDate = models.DateField(auto_now_add=True)
	createUser = models.CharField(max_length=255)
	updateDate = models.DateField()
	updateUser = models.CharField(max_length=20)
	keepalivedAddress = models.CharField(max_length=255)
	nodeAddress = models.CharField(max_length=255)
	etcd_ca_dir = models.CharField(max_length=255)
	kube_dir = models.CharField(max_length=255)
	kube_api_port = models.IntegerField()
	deploy = models.IntegerField()
	etcd_default_port = models.IntegerField()
	haproxy_default_port = models.IntegerField()
	class Meta:
		db_table = "kube_config"

class KubeCluster(models.Model):
	ip = models.CharField(max_length=20)
	nodeType = models.CharField(max_length=16)
	ssh = models.IntegerField()
	cluster = models.CharField(max_length=20)
	user = models.CharField(max_length=30)
	password = models.CharField(max_length=30)
	port = models.IntegerField()
	class Meta:
		db_table = "kube_cluster"

class Server(models.Model):
	id = models.IntegerField(primary_key = True)
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
	updateDate = models.DateField()
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
	updateDate = models.DateField()
	createUser = models.CharField(max_length=20)
	updateUser = models.CharField(max_length=20)
	class Meta:
		db_table = "version_env"















