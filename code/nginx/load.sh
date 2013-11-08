#!/bin/bash

# this copies ./html to the server

if [ $# -ne  2 ]; then
    echo "Usage: `basename $0` username serveraddress"
    exit
fi

server_user=$1;
server_address=$2;

app_dir='/usr/share/nginx/html/';

srv_user='nginx';

mkdir ./temp;

cp -r ./html ./temp;

cd ./temp;

cd ../;

tar -cf temp.tar temp/;

rm -rf ./temp;

scp ./temp.tar $server_user@$server_address:~;

rm -f ./temp.tar;

ssh $server_user@$server_address "

rm -rf $app_dir;

tar -xmf temp.tar;
mv -f ./temp/html $app_dir;

chown -R $srv_user $app_dir;

rm -rf ./temp;
rm -f ./temp.tar;

";

