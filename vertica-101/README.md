#Vertica
This quick introduction to using Vertica inside IPython starts with a [datarama blog post](https://sites.google.com/a/twitter.com/gnip-data-rama/2015-q1-data-blog/2015-02-19twitterdataresourcespart5vertica). We'll set up an SSH tunnel and get things moving along.  

#IPython
We use the `vertica_python` package. We will open a connection, create a
database, add a record, print items as `list` or as `dict` and then
learn to iterate through results.  

#R
Setting up our ~/.Rprofile, we can easily access our database from
inside Rstudio. Example:  
<pre>
users = v("SELECT a._id, count(a._id)
FROM someplace.user_megastore_2 a, test.ddis_blehman_users b
          WHERE a.user_id=b.userID
          group by a._id
        ;")
</pre>
#HDFS
We can run map reduce jobs and then quickly place data into vertica using commands like `COPY test.ddis_blehman_test FROM LOCAL 'userID_unique_2012-2015.csv'`.  
