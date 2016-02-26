#!/usr/bin/env bash
# Scott Hendrickson
# @drskippy
# 2016-02-26

app_name=coin_toss
app_path=/opt/twitter/var/www
echo "Deploying $app_name: $(date)"

# remove the older version of the app if it exists
# note: add old application back up here?
if [ -d $app_path/$app_name ]; then
    rm -r $app_path/$app_name
fi

# copy the latest version of the application to the
# deploy directory
cp -r ../app $app_path/$app_name

# run the fastcgi container. 
# CONVENTION: name the fcgi file the same base name as
#             the application
# note: can set this to be started on boot
#       if you are building an app that should restart.
#       see you OS's facilities for launching on boot
$app_path/$app_name/$app_name.fcgi &

# deploy the latest web server plug in configuration
sudo cp ../configs/*.conf /opt/twitter/etc/nginx/servers

# stop the server, then restart it to load the latest
# application configuration
sudo nginx -s stop
sudo nginx

echo "Done."
