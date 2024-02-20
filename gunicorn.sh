#!/bin/bash

source env/bin/activate
echo $PWD
cd /var/www/spira_backend  #this is not reflecting in build

# python3 manage.py makemigrations
# python3 manage.py migrate


# echo "Migrations done"

cd /var/www/spira_backend


sudo cp -rf gunicorn.service /etc/systemd/system/gunicorn.service

echo "$USER"
echo "$PWD"



sudo systemctl daemon-reload
sudo systemctl start gunicorn.service
sudo systemctl enable gunicorn.service


echo "Gunicorn has started."

echo "Gunicorn has been enabled."


sudo systemctl restart gunicorn.service
sudo systemctl status gunicorn.service

