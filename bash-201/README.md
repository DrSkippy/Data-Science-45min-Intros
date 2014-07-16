#BASH Data Structures
------------
------------
This tutorial intends for you to run the code blocks directly in the command line.

## List
 
*  Create:
<pre>
declare -a pub_list=(twitter tumblr disqus fsq wp-com wp-org)
</pre>

*  Assign:
<pre>
list_items=$(echo ${pub_list[@]})
my_item=${pub_list[5]}
</pre>

*  Reference:
<pre>
echo ${pub_list[@]}
echo ${pub_list[5]}
</pre>

*  Loop:
<pre>
for pub in "${pub_list[@]}"; do
    echo "---------------------------------"
    echo "$pub"
done
</pre>

## Dictionary

*  Create:
<pre>
declare -A twitter_handle
</pre>

*  Assign:
<pre>
twitter_handle["jrmontague"]=jrmontag
twitter_handle["jkobl"]=JeffAKolb
twitter_handle["shendrickson"]=DrSkippay
twitter_handle["blehman"]=BrianLehman
</pre>

*  Reference:
<pre>
echo ${twitter_handle["jrmontague"]}
echo ${!twitter_handle[@]}
echo ${twitter_handle[@]}
</pre>

*  Loop:
<pre>
for i in "${!twitter_handle[@]}"; do
    echo "key: $i"
    echo "value: ${twitter_handle[$i]}"
done
</pre>

## Date Object

*  Create range:
<pre>
start_date="2014-01-09 22:00:00";  
end_date="2014-01-10 22:00:00";  
</pre>

*  Create date objects:
<pre>
current=$(date -d "${start_date:0:4}${start_date:5:2}${start_date:8:2} ${start_date:11:2}")
end=$(date -d "${end_date:0:4}${end_date:5:2}${end_date:8:2} ${end_date:11:2}")
</pre>

*  Loop:
<pre>
while [ "$end" != "$current" ];do
    path=$(date -d "$current" +%Y%m%d.%H)
    year="${path:0:4}"
    mnth="${path:4:2}"
    day="${path:6:2}"
    hour="${path:9:2}"
    echo $path
    current=$(date -d "$current +1 hours")
done
</pre>

## Strings  (quote hell) 

*  Hard vs soft quote
<pre>
var='$USER'
echo $var
</pre>
<pre>
var="$USER"
echo $var
</pre>

*  Combine quotes
<pre>
var='$USER='"$USER"
</pre>

## Examples
*  Create globals
<pre>
grep_cmd1='grep -i -E "cat|bull dog"'       # cat
grep_cmd2='grep -i -E "cat'"'"'s|bull dog"'  # cat's
cmd1="cat prac | ${grep_cmd1}"
cmd2="cat prac | ${grep_cmd2}"
</pre>

*  Eval
<pre>
eval $cmd1
eval $cmd2
</pre>

*  Back tic 
<pre>
echo `eval $cmd1` # be careful with back tics 
</pre>

*  Back tic vs eval

<pre>
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
</pre>

## Quizes
*  Quiz #1
Given a set of tweets and grep statemnts, create files appropriately named based on the grep rules. Only change the indicated line.
<pre>
tmp=twitter.agg.piped
if [ -f grep_rules.txt ]; then
    while read line; do                    
        echo "file: $tmp for rule: $line"
        eval "$line"
        # --------------------
        # -- run script and debug line below -- 

        rname="${grep_stmt} | rules_to_file_name.py"
        
        # -- run script and debug line above --
        # --------------------


        cmd="cat $tmp | $grep_stmt > twitter.agg.piped.${rname}.filter.piped &"
        eval "$cmd"
    done < grep_rules.txt
else
    echo "   No grep_rules.txt found."
fi 
</pre>

*  Quiz #2 
Try to spot the problem with the quotes.
<pre>
# The following string resulted in a rule with value: "from:$USER" ; instead of value: "from:compston"
curl -v -X POST -ustephen@gnip.com "https://api.gnip.com/replay/rules.json" -d '{"rules":[{"value":"from:$USER"}]}'
</pre>



## Quiz Solutions

*  Quiz #1 solution
<pre>
rname=$(echo "${grep_stmt}" |./rules_to_file_name.py)
</pre>

* Quiz #2 solution
<pre>
curl -v -X POST -ustephen@gnip.com "https://api.gnip.comreplay/rules.json" -d '{"rules":[{"value":"from:'"$USER"'"}]}'
</pre>

