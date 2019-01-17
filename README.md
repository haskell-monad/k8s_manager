

### 

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo python get-pip.py

pip install Django==1.11.4
pip install celery==celery-4.2.1
pip install redis

python manage.py runserver 0.0.0.0:8000

celery -A k8s_manager  worker -l debug