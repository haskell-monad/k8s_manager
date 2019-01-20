### 安装说明

本项目依赖[kubeasz](https://github.com/gjmzj/kubeasz/)项目(作者可厉害了^-^)，提供了web操作界面，用于快速搭建k8s集群

```
# 安装python-pip
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo python get-pip.py

# 使用pip安装依赖
pip install Django==1.11.4
pip install celery==celery-4.2.1
pip install redis

# 修改k8s_manager/settings.py文件，配置成自己的redis服务器
CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/0"
CELERY_TASK_SERIALIZER = "json"

# 启动 django
python manage.py runserver 127.0.0.1:8000

# 启动 celery
celery -A k8s_manager worker -l debug

```

### 其他说明
```
# 当前使用的是sqlite3数据库，如需使用其他数据库，请自行配置
# 生成表
python manage.py migrate
python manage.py makemigrations k8s_manager 
python manage.py migrate k8s_manager

# init.sql 中 默认录入了一些初始数据，可以导入进去

```

### TODO
```
1.实时输出/查看日志
2.执行远程命令
3.集群状态查看
4.安装常用插件/个性化插件配置
5.部署应用
...

```


![image](https://github.com/limengyu1990/k8s_manager/raw/master/images/1.jpg)
![image](https://github.com/limengyu1990/k8s_manager/raw/master/images/2.jpg)
![image](https://github.com/limengyu1990/k8s_manager/raw/master/images/3.jpg)
![image](https://github.com/limengyu1990/k8s_manager/raw/master/images/4.jpg)
![image](https://github.com/limengyu1990/k8s_manager/raw/master/images/5.jpg)
![image](https://github.com/limengyu1990/k8s_manager/raw/master/images/6.jpg)
![image](https://github.com/limengyu1990/k8s_manager/raw/master/images/7.jpg)
![image](https://github.com/limengyu1990/k8s_manager/raw/master/images/8.jpg)
![image](https://github.com/limengyu1990/k8s_manager/raw/master/images/9.jpeg)
