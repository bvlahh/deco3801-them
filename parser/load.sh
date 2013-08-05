#!/bin/bash

# this copies ./html to the server

server_user='root';
server_address='vmx14562.hosting24.com.au';

app_dir='~/parser';

srv_user='root';

mkdir ./temp;

cp -r ./src ./temp

tar -cf temp.tar temp/;

rm -rf ./temp;

scp ./temp.tar $server_user@$server_address:~;

rm -f ./temp.tar;

ssh $server_user@$server_address "

rm -rf $app_dir;

tar -xmf temp.tar;
mv -f ./temp/ $app_dir;

rm -rf ./temp;
rm -f ./temp.tar;

supervisorctl restart parser
";

