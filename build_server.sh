#!/bin/bash

if [ $# -ne  2 ]; then
    echo "Usage: `basename $0` user server"
    exit
fi

scp -r ./config $1@$2:~

ssh $1@$2 '
cd config
./server_setup.sh
';

#scp -r ./nginx $USER@$SERVER:/
#scp -r ./parser $USER@$SERVER:/
#scp -r ./config $USER@$SERVER:/
