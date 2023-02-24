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
