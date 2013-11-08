#!/bin/bash

# this copies ./rpc-server to the server

server_user=$1;
server_address=$2;

app_dir='~/parser';

mkdir ./temp1;

cp -r ./rpc-server ./temp1

cp -r ./html5-python ./temp1

tar -cf temp1.tar temp1/;

rm -rf ./temp1;

scp ./temp1.tar $server_user@$server_address:~;

rm -f ./temp1.tar;

ssh $server_user@$server_address "

rm -rf $app_dir;

tar -xmf temp1.tar;
mv -f ./temp1/ $app_dir;

rm -rf ./temp1;
rm -f ./temp1.tar;

cd /root/parser/html5-python;
python setup.py install;

supervisorctl restart parser"
