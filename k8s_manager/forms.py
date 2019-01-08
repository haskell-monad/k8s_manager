# -*- coding: utf-8 -*-
from .models import Assets
from django.forms import ModelForm
from django.forms import widgets as wid
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
            "idc": wid.TextInput(attrs={'class':'smallinput', 'placeholder':"如：10.24.22.12"}),
            "cabinetNo": wid.TextInput(attrs={'class':'smallinput', 'placeholder':"如：10.24.22.12"}),
            "cabinetOrder": wid.TextInput(attrs={'class':'smallinput', 'placeholder':"如：10.24.22.12"}),
            "tags": wid.TextInput(attrs={'class':'smallinput', 'placeholder':"如：阿里云 高配"}),
        }
        labels= {
            "idc": "IDC机房(可选)",
            "cabinetNo": "机柜号(可选)",
            "cabinetOrder": "机柜中序号(可选)",
            "tags": "资产标签(可选)" 
        }