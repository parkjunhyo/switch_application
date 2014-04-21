#! /bin/env bash

## download and installation
yum install -y httpd

## boot start up
chkconfig httpd on

## web folder generation
web_dir='/var/www/html/config'
chmod 777 /var/www/html
chmod 777 /var/www
if [[ ! -d $web_dir ]]
then
 mkdir -p $web_dir
 chmod 777 $web_dir
fi

## copy the upgrade file
cp ./upgrade_os.py /var/www/html/upgrade_os.py
chmod 777 /var/www/html/upgrade_os.py

## os folder
os_dir='/var/www/html/os'
if [[ ! -d $os_dir ]]
then
 mkdir -p $os_dir
 chmod 777 $os_dir
fi

## service restart
/etc/init.d/httpd restart

