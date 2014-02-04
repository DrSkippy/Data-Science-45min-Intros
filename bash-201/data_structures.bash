#!/usr/bin/env bash
#################
echo $(date)
dt=$(date +%Y%m%d_%H%M)

#################
# list
#################
 
#--create:
declare -a pub_list=(twitter tumblr disqus fsq wp-com wp-org)

#--assign:
list_items=$(echo ${pub_list[@]})
my_item=${pub_list[5]}

#--reference:
echo ${pub_list[@]}
echo ${pub_list[5]}

#--loop:
for pub in "${pub_list[@]}"; do
    echo "---------------------------------"
    echo "$pub"
done

#################
# dictionary
#################

#--create:
declare -A twitter_handle

#--assign:
twitter_handle["jrmontague"]=jrmontag
twitter_handle["jkobl"]=JeffAKolb
twitter_handle["shendrickson"]=DrSkippy27
twitter_handle["blehman"]=WordCrank

#--reference:
echo ${twitter_handle["jrmontague"]}
echo ${!twitter_handle[@]}
echo ${twitter_handle[@]}

#--loop:
for i in "${!twitter_handle[@]}"; do
    echo "key: $i"
    echo "value: ${twitter_handle[$i]}"
done

#################
# date object
#################

#--create range:
start_date="2014-01-09 22:00:00";  
end_date="2014-01-10 22:00:00";  

#--create date objects:
current=$(date -d "${start_date:0:4}${start_date:5:2}${start_date:8:2} ${start_date:11:2}")
end=$(date -d "${end_date:0:4}${end_date:5:2}${end_date:8:2} ${end_date:11:2}")

#--loop:
while [ "$end" != "$current" ];do
    path=$(date -d "$current" +%Y%m%d.%H)
    year="${path:0:4}"
    mnth="${path:4:2}"
    day="${path:6:2}"
    hour="${path:9:2}"
    echo $path
    current=$(date -d "$current +1 hours")
done

#################
# strings  (quote hell) 
#################

#--hard vs soft quote
var='$USER'
echo $var

var="$USER"
echo $var

#--combine quotes
var='$USER='"$USER"

#--Example:
#--create globals
grep_cmd1='grep -i -E "cat|bull dog"'       # cat
grep_cmd2='grep -i -E "cat'"'"'s|bull dog"'  # cat's
cmd1="cat prac | ${grep_cmd1}"
cmd2="cat prac | ${grep_cmd2}"

#--eval
eval $cmd1
eval $cmd2

#--back tic 
echo `eval $cmd1` # be careful with back tics 

#--back tic vs eval
pwd
eval pwd
echo `pwd`
`pwd`           #notice error

echo $USER
eval "$USER"    #notice error
echo `$USER`    #notice error
`$USER`         #notice error
$USER           #notice error

var=`echo $USER`
echo $var

var=$USER
echo $var

#-- quiz #1 
tmp=twitter.agg.piped
if [ -f grep_rules.txt ]; then
    while read line; do                    
        echo "file: $tmp for rule: $line"
        eval "$line"

        # -- fix line below -- 
        rname="${grep_stmt} | rules_to_file_name.py"
        # -- fix line above --        

        cmd="cat $tmp | $grep_stmt > twitter.agg.piped.${rname}.filter.piped &"
        eval "$cmd"
    done < grep_rules.txt
else
    echo "   No grep_rules.txt found."
fi 

#-- quiz #2 
# The following string resulted in a rule with value: "from:$USER" ; instead of value: "from:compston"
curl -v -X POST -ustephen@gnip.com "https://api.gnip.com/replay/rules.json" -d '{"rules":[{"value":"from:$USER"}]}'














#---------------------------------------------------------------
#---------------------------------------------------------------

#-- quiz #1 solution
rname=$(echo "${grep_stmt}" |./rules_to_file_name.py)

#-- quiz #2 solution
curl -v -X POST -ustephen@gnip.com "https://api.gnip.comreplay/rules.json" -d '{"rules":[{"value":"from:'"$USER"'"}]}'

#---------------------------------------------------------------
#---------------------------------------------------------------



