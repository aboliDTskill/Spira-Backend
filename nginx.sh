#!/bin/bash

sudo cp -rf app.conf /etc/nginx/sites-available/app.conf
sudo chmod -R 777  /var/www/spira_backend

sudo ln -s /etc/nginx/sites-available/app.conf /etc/nginx/sites-enabled
sudo systemctl restart nginx
sudo nginx -t

sudo systemctl start nginx
sudo systemctl enable nginx

echo "Nginx has been started"

sudo systemctl status nginx

