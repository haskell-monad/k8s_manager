# -*- coding: utf-8 -*-
from .models import (Assets,Product)
from django.forms import ModelForm
from django.forms import widgets as wid
from . import common

class AssetsForm(ModelForm):
    class Meta:
        model = Assets
        fields = ('assetType','status','idc','cabinetNo','cabinetOrder','tags','id')
        exclude = None          #排除的字段
        labels = None           #提示信息
        help_texts = None       #帮助提示信息
        widgets = None          #自定义插件
        error_messages = None   #自定义错误信息
        # error_messages = {
        #     'name':{'required':"用户名不能为空",},
        #     'age':{'required':"年龄不能为空",},
        # }
        widgets = {
            "assetType": wid.Select(choices=common.TYPE_VALUE),
            "status": wid.Select(choices=common.STATUS_VALUE),
            "idc": wid.TextInput(attrs={'class':'smallinput', 'placeholder':"如：10.24.22.12"}),
            "cabinetNo": wid.TextInput(attrs={'class':'smallinput', 'placeholder':"如：10.24.22.12"}),
            "cabinetOrder": wid.TextInput(attrs={'class':'smallinput', 'placeholder':"如：10.24.22.12"}),
            "tags": wid.TextInput(attrs={'class':'smallinput', 'placeholder':"如：阿里云 高配"}),
            "id": wid.HiddenInput()
        }
        labels= {
            "idc": "IDC机房(可选)",
            "cabinetNo": "机柜号(可选)",
            "cabinetOrder": "机柜中序号(可选)",
            "tags": "资产标签(可选)" 
        }

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ('productName','productWiki','productManager','productContact','devManager','devContact','qaManager','qaContact','safeManager','safeContact','productDesc','id')
        exclude = None          #排除的字段
        labels = None           #提示信息
        help_texts = None       #帮助提示信息
        widgets = None          #自定义插件
        error_messages = None   #自定义错误信息
        widgets = {
            "productName": wid.TextInput(attrs={'class':'smallinput', 'placeholder':"如：支付系统"}),
            "productWiki": wid.TextInput(attrs={'class':'smallinput'}),
            "productManager": wid.TextInput(attrs={'class':'smallinput', 'placeholder':"如：张启山"}),
            "productContact": wid.TextInput(attrs={'class':'smallinput', 'placeholder':"如：qishan.zhang@gmail.com"}),
            "devManager": wid.TextInput(attrs={'class':'smallinput'}),
            "devContact": wid.TextInput(attrs={'class':'smallinput'}),
            "qaManager": wid.TextInput(attrs={'class':'smallinput'}),
            "qaContact": wid.TextInput(attrs={'class':'smallinput'}),
            "safeManager": wid.TextInput(attrs={'class':'smallinput'}),
            "safeContact": wid.TextInput(attrs={'class':'smallinput'}),
            "productDesc": wid.Textarea(attrs={'cols': 80, 'rows': 5, 'class':'mediuminput'}),
            "id": wid.HiddenInput()
        }

class ProductVersionForm(ModelForm):
    class Meta:
        model = ProductVersion
        fields = ('versionName','tags','versionStatus','startTime','endTime','versionWiki','productManager','productContact','devManager','devContact','qaManager','qaContact','safeManager','safeContact','productId','id')
        exclude = None          #排除的字段
        labels = None           #提示信息
        help_texts = None       #帮助提示信息
        widgets = None          #自定义插件
        error_messages = None   #自定义错误信息
        widgets = {
            "versionName": wid.TextInput(attrs={'class':'smallinput', 'placeholder':"如：v2.1.0"}),
            "tags": wid.TextInput(attrs={'class':'smallinput', 'placeholder':"如：uat,payment,v2.0.0或者uat|payment|v2.0.0"}),
            "versionStatus": wid.Select(choices=common.VERSION_STATUS_VALUE),
            "startTime": wid.TextInput(attrs={'class':'smallinput'}),
            "endTime": wid.TextInput(attrs={'class':'smallinput'}),
            "versionWiki": wid.TextInput(attrs={'class':'smallinput'}),
            "productManager": wid.TextInput(attrs={'class':'smallinput', 'placeholder':"如：张启山"}),
            "productContact": wid.TextInput(attrs={'class':'smallinput', 'placeholder':"如：qishan.zhang@gmail.com"}),
            "devManager": wid.TextInput(attrs={'class':'smallinput'}),
            "devContact": wid.TextInput(attrs={'class':'smallinput'}),
            "qaManager": wid.TextInput(attrs={'class':'smallinput'}),
            "qaContact": wid.TextInput(attrs={'class':'smallinput'}),
            "safeManager": wid.TextInput(attrs={'class':'smallinput'}),
            "safeContact": wid.TextInput(attrs={'class':'smallinput'}),
            "productId": wid.HiddenInput(),
            "id": wid.HiddenInput()
        }

class KubeConfigForm(ModelForm):
    class Meta:
        model = ProductVersion
        fields = ('versionName','tags','versionStatus','startTime','endTime','versionWiki','productManager',
                'productContact','devManager','devContact','qaManager','qaContact','safeManager','safeContact','productId','id'
        )
        exclude = None          #排除的字段
        labels = None           #提示信息
        help_texts = None       #帮助提示信息
        widgets = None          #自定义插件
        error_messages = None   #自定义错误信息
        widgets = {
            "kubeName": wid.TextInput(attrs={'class':'smallinput', 'placeholder':"如：Test"}),
            "clusterIP": wid.TextInput(attrs={'class':'smallinput', 'placeholder':"如：10.244.0.0/16"}),
            "serviceClusterIP": wid.TextInput(attrs={'class':'smallinput', 'placeholder':"如：10.96.0.0/12"}),
            "dnsIP": wid.TextInput(attrs={'class':'smallinput', 'placeholder':"如：10.96.0.10"}),

            "dnsDN": wid.TextInput(attrs={'class':'smallinput', 'placeholder':"如：cluster.local"}),
            "apiVIP": wid.TextInput(attrs={'class':'smallinput', 'placeholder':"如：11.11.11.109"}),
            "ingressVIP": wid.TextInput(attrs={'class':'smallinput', 'placeholder':"如：11.11.11.110"}),
            "sshUser": wid.TextInput(attrs={'class':'smallinput', 'placeholder':"如：root"}),

            "sshPort": wid.TextInput(attrs={'class':'smallinput', 'placeholder':"如：22"}),
            "masterAddress": wid.TextInput(attrs={'class':'smallinput', 'placeholder':"如：10.10.10.1[1,2,3]  test.k8s-[1-3].cluster"}),
            "masterHostName": wid.TextInput(attrs={'class':'smallinput', 'placeholder':"如：K8S-M"}),
            "nodeHostName": wid.TextInput(attrs={'class':'smallinput', 'placeholder':"如：K8S-N"}),

            "etcdAddress": wid.TextInput(attrs={'class':'smallinput', 'placeholder':"如：10.20.20.1[1,2],10.20.20.22"}),
            "yamlDir": wid.TextInput(attrs={'class':'smallinput'}),
            "nodePort": wid.TextInput(attrs={'class':'smallinput', 'placeholder':"200010"}),
            "kubeToken": wid.TextInput(attrs={'class':'smallinput'}),

            "keepalivedAddress": wid.TextInput(attrs={'class':'smallinput', 'placeholder':"如：v2.1.0"}),
            "kubeDesc": wid.TextInput(attrs={'class':'smallinput', 'placeholder':"如：v2.1.0"}),
            "id": wid.HiddenInput(),
            "deploy": wid.HiddenInput(),

            
            "kubeVersion": wid.Select(choices=common.VERSION_STATUS_VALUE),
            "kubeCniVersion": wid.Select(choices=common.VERSION_STATUS_VALUE),
            "etcdVersion": wid.Select(choices=common.VERSION_STATUS_VALUE),
            "dockerVersion": wid.Select(choices=common.VERSION_STATUS_VALUE),
            "netMode": wid.Select(choices=common.VERSION_STATUS_VALUE),

            "loadBalance": wid.Select(choices=common.VERSION_STATUS_VALUE),
 
        }










