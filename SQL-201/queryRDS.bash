#!/usr/bin/env bash

#specify the file with the literal SQL in it
queryfile=sample-query.sql

# db params
username=<your username
pass=<your password>
host=<your rds hostname>



# query results ==>  stdout
mysql -u${username} -p${pass} -h${host} < $queryfile 

# query results ==> file
#mysql -u${username} -p${pass} -h${host} < $queryfile > output.tsv

# nb, can also run: $ echo "command" | mysql -uxxx -pxxx db
# or: $ cat queryfile | mysql -uxxx -pxxx db

