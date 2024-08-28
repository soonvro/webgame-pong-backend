#!/bin/sh

apt update
apt install -y openssh-server
passwd root
echo "PermitRootLogin yes" >> /etc/ssh/sshd_config
service ssh start

echo "Running Space-Pin-Pong Dev Server"
python manage.py runserver 0.0.0.0:8000
