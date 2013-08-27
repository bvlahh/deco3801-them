#!/bin/bash

echo "insert into to_validate (select address, port from good_proxies where lastchecked < (unix_timestamp(now())-3600) ); delete from good_proxies where lastchecked < (unix_timestamp(now())-3600);" | mysql -t -D proxylist;

