#!/bin/bash

if [ -d "env" ] 
then
    echo "Python virtual environment exists." 
else
    python3 -m venv env
fi

echo $PWD
source /var/www/spira_backend/env/bin/activate  #this is not building here /var/lib/jenkins/workspace/Backend


pip3 install -r requirements.txt

if [ -d "logs" ]
then
    echo "Log folder exists." 
else
    mkdir logs
    touch logs/error.log logs/access.log
fi

sudo chmod -R 777 logs

echo "env setup finished"