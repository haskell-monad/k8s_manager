

### 

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo python get-pip.py

pip install Django==1.11.4
pip install celery==celery-4.2.1
pip install redis

python manage.py runserver 127.0.0.1:8000

celery -A k8s_manager  worker -l debug




### todo
1.增加[新增node/master节点]操作
2.增加各个[服务验证/查看日志]操作


### 说明


