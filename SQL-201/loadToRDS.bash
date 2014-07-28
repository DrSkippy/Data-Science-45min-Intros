#!/usr/bin/env bash
echo $(date)

# load script 
sql=sample-load.sql

# rds creds
user=<your username>
pass=<your password>
host=<your rds hostname>


# launch mysql server and input commands from SQL script above
mysql --enable-local-infile -u${user} -p${pass} -h${host} < $sql


echo $(date)
