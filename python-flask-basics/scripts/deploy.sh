#!/usr/bin/env bash

echo $(date)

rm -r /opt/twitter/var/www/coin_toss
cp -r ../app /opt/twitter/var/www/coin_toss

/opt/twitter/var/www/coin_toss/coin_toss.fcgi &

sudo cp ../configs/*.conf /opt/twitter/etc/nginx/servers

sudo nginx -s stop
sudo nginx

