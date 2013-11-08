#!/bin/bash

if [ $# -ne  2 ]; then
    echo "Usage: `basename $0` user server"
    exit
fi

scp -r ./config $1@$2:~

ssh $1@$2 '
cd config
./server_setup.sh
'

cd nginx
./load.sh $1 $2

cd ..

cd parser
./load.sh $1 $2

cd ..
