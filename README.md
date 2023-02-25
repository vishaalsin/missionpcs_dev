# missionpcs_dev
cd /tmp
curl -O https://repo.anaconda.com/archive/Anaconda3-2021.05-Linux-x86_64.sh
bash Anaconda3-2021.05-Linux-x86_64.sh
conda create -n prepfreak python=3.8
conda activate prepfreak
sudo apt-get update
sudo apt-get install libpq-dev
sudo apt-get install python-dev
sudo apt-get install gcc
sudo reboot
pip install -r requirements/requirements-common.txt
pip install python-decouple
pip install django-robots
pip install django-sslserver
pip install django-extensions
pip install django-celery-results --upgrade
pip install psycopg2-binary
pip install django-mysql
pip install social-auth-app-django --upgrade
pip install django-celery-beat --upgrade
pip install django-cors-headers --upgrade
pip install django==3.2 --upgrade
