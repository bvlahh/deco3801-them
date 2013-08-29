#!/bin/bash

# this copies ./src to the server

server_user='root';
server_address='vmx14562.hosting24.com.au';

app_dir='~/parser';

srv_user='root';

mkdir ./temp1;

cp -r ./src ./temp1

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

supervisorctl restart parser
";

