#coding=utf-8  
from django import template  
  
register = template.Library()  
  

@register.filter(name='filter_list')  
def filter_list(list_, key):  
    return list_[key-1]