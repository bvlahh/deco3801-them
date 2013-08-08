#!/bin/bash

# install ssh clients so we can scp our files across
yum -y install openssh-clients;

################################################################################
### scp supervisord init script, iptables rules, supervisor, nginx, and php  ###
### config files to working directory before this                            ###
################################################################################

# set the timezone as Brisbane with a symlink
ln -sf /usr/share/zoneinfo/Australia/Brisbane /etc/localtime;

# add the epel repository
rpm -Uvh ftp://mirror.optus.net/epel/6/x86_64/epel-release-6-8.noarch.rpm;

# update what's already installed
yum -y update;

# lightish php install for now - dependencies get installed too
yum -y install php-common php php-mbstring php-cli php-xml php-mysql;

# nginx web server
yum -y install nginx;

# we'll run nginx under supervisor along with php, so turn off auto start
chkconfig nginx off;

# no database yet

# install supervisor and init script, auto start it when the machine starts
yum -y install python-setuptools;
easy_install supervisor;
mv -f ./supervisord /etc/rc.d/init.d/supervisord;
chmod +x /etc/rc.d/init.d/supervisord;
chkconfig --add supervisord;
chkconfig --level 35 supervisord on;

# iptables firewall rule (allow http traffic inbound)
mv -f ./iptables /etc/sysconfig/iptables;
chcon --reference=/etc/sysconfig/syslog /etc/sysconfig/iptables;
service iptables restart;

# copy config files - we're not customising php.ini yet
mv -f ./supervisord.conf /usr/etc/supervisord.conf;
mv -f ./nginx.conf /etc/nginx/nginx.conf;
mv -f ./php.ini /etc/php.ini;

# start it all
service supervisord start;


