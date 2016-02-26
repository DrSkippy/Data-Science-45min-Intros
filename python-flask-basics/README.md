# Simple Flask Application

##Steps:

###(1) Install a web server

This is the application that runs in the background and processes HTTP protocol requests.  For
this demonstration, we will use the NGINX web server on our OSX laptops.

    brew update
    brew install nginx

Now that the web server is installed, we are ready to test it.  Later, you may want to start
the server on machine start up. Today, we will start it manually. Be sure to start it again
when you need it after you have restarted your computer.

To start the server

    sudo nginx

Now visit http://localhost:8080. You should get "Welcome to nginx!" message if everything went
well.

###(2) Install a gateway module for communication between our application and the web server
For this example, we will use fastcgi.  To install this module,

    brew install fastcgi

###(3) Install the application requirements
    
    pip install numpy matplotlib
    pip install flask flup

###(4) We need to set a user for the web server
The web server will run as a specified user. When the web server was installed, the default
behavior is to run as "nobody". This won't work for us because "nobody" has the wrong permissions.
(But that doesn't mean everybody has the right permissions!).

Edit the file /opt/twitter/etc/nginx/nginx.conf.  Add the single line immediately after then line 
that starts "#user..." (line 3):
    
    user <your user name> staff;

###(5) Move into the Scripts directory and deploy the application

    cd scripts
    ./deploy.sh

###(6) Rejoice!
To understand the workings of the code, follow along as we explore the application tree.  The gist of
the structure is to keep everthing in an orderly github repository that includes scripts
for rapidly deploying the code, configs and restarting the web server with the new configs.

    |____app
    | |____coin_toss.fcgi
    | |____coin_toss.py
    | |____templates
    | | |____info.html
    | | |____table.html
    |____configs
    | |____coin_toss.conf
    |____README.md
    |____scripts
    | |____deploy.sh


Let's start with the deploy scrip:

    #!/usr/bin/env bash

    echo $(date)

    rm -r /opt/twitter/var/www/coin_toss
    cp -r ../app /opt/twitter/var/www/coin_toss

    /opt/twitter/var/www/coin_toss/coin_toss.fcgi &

    sudo cp ../configs/*.conf /opt/twitter/etc/nginx/servers

    sudo nginx -s stop
    sudo nginx

###(7) Open coin_toss.conf

###(8) Open coin_toss.fcgi

###(9) open coin_toss.py

###(10) Try the APIs

    http://localhost:8090/coin_toss/info
    http://localhost:8090/coin_toss/ensemble
    http://localhost:8090/coin_toss/ensemble/summary
    http://localhost:8090/coin_toss/plot/demo.png
    http://localhost:8090/coin_toss/hist/100_100_500.png
    http://localhost:8090/coin_toss/ensemble/table
    http://localhost:8090/coin_toss/ensemble/csv



