# Beginner / Intermediate Programmatic MySQL 

2013-11-21, Josh Montague

An introduction to a command-line workflow using MySQL. The queries used here are relatively simple - mostly focused on illustrating the ability to load data into relational tables, and then form queries which ``JOIN`` across those tables. For an easier way to start learning about syntax and query-building, you can explore interactive links like [SQLfiddle](http://sqlfiddle.com/) or [SQLzoo](http://sqlzoo.net/wiki/SELECT_basics).

This session was built using:

- Ubuntu 12 with `mysql-server` (should be installed by default)
- AWS RDS with MySQL 5.5 
 
-------------------------------------

## Motivation 

This session was designed specifically for the workflow and infrastructure we were using at the time. That is, we wanted to maintain some modifiable ``.sql`` files for updating / reproducing behavior in the future, and we wanted to do all the work from a ``bash`` shell. Additionally, we knew about a particular remote database hostname and had control over the databases and tables therein. Where appropriate in these files, I'll indicate where you'll want to change the values being used. Unless you want to just copy our table structure, which is kind of weird. Not really creepy weird, because I understand that would require less work on your part. But still, a little weird.  


## Input Data 

In this session, we'll start with two tab-separated input data files; assume that we got them from some other process. Go ahead and ``cat`` the two data files in ``data/``. The important point is that the input files contain rows of data that represent measurements or observations of various features. And, as is indicated by the filenames, the two files are intended to represent different aspects of the same entities (people). An important feature of the data is that there exists a shared id - a number in this case, in the first column - that connects the entities (people) in the two files together. These individual files will soon become tables in our database. 

 
## Loading Tables 

Again, we're looking for an approach that is programmatic, so to load the tables we'll use the ``loadToRDS.bash`` script. In this file, we can see that there are a handful of variables to set up. The goal is to build up the command-line options used in the ``mysql`` command near the end. To actually log in and issue any commands, you'll need to know your username and password (in addition to the actual hostname, if it's a remote RDS instance). At the end of the command, you can see that we're going to redirect the ``.sql`` file to the ``mysql`` command. The result of this process is identitical to having manually typed all the lines of ``sample-load.sql`` on the interactive MySQL prompt.  

Having seen how the ``sample-load.sql`` file is going to be used, we can now look at the contents of that file to see what's happening. The first thing we have to do is select the right database; there could be many databases in our RDS instance. In this case, we're using the ``zzzRST`` database (so named in order to appear at the end of the list). For this example, we're assuming that each time we run this script we want to start over from scratch. Obviously that's a little harsh if you're maintaining a database for any useful application; but it shows how you'd go about building out tables the first time. We first ``DROP`` (delte) the table if it already exists (again, typically not how you'd start a more maintenance-oriented database interaction). Then, we create two tables, one for each of the two data files we have locally. We specify the column titles (which weren't in the data files, themselves), and set the column type, and an default behavior in the event of missing data. We assign the primary key to the id in the first column because we know that should be both unique, and present in the other table. In this example, I won't delve into the subtleties of syntax and data types, but note that the [MySQL documentation](http://dev.mysql.com/doc/refman/5.5/en/create-table.html) is actually quite well-written.

After creating the tables, we upload the data files (possible because we logged into the MySQL server with the ``--enable-local-infile`` option). Note that you'll have to modify the path to reflect your local file system. We describe the format of the data (delimiters, line breaks), and specify the column order. 

Finally, we build indexes on some of the table columns. Indexes are essentially the reason that database queries can happen quickly. If you're not already familiar with them (or even if you are, really), definitely have a read through [the index docs](http://dev.mysql.com/doc/refman/5.5/en/mysql-indexes.html). The primary keys will already have indexes on them, but if we want to ``SELECT`` on any other column, it's a good idea to build the indexes upfront. It only costs a little bit of time to do this, so I always try to make a guess about what to index at the start. It's possible to define the index columns in the ``CREATE TABLE`` command, but this will result in a slower load process. Though this small example won't illustrate the difference, the added time cost of building the index on load for each row adds up quickly. Note the last index is a compound index on a combination of column values.  

Now that we have a handle on what's going on during the load process, we can move the data to the RDS by simply running the ``loadToRDS.bash`` script. Though these small data files will only take seconds to load, large files can take some time, so you'll likely want to ``nohup`` and background the task.  

## Querying Tables 

The query script has a similar structure - we define some variables and construct the ``mysql`` command, then redirect another ``.sql`` file with commands to make queries. In this ``queryRDS.bash`` script, there are two examples of "what to do with the results". The first will return the results to ``stdout``, while the second writes the results to a file. Try the file output version once so you believe it, but use the ``stdout`` version for most of the examples so you can immediately see the results. 

*Note that it's definitely possible to manage the command line parameters in other ways; one could define e.g. a ``params.bash`` file that ``export``s the variables to your environment for the session and ``source`` that file. That approach would reduce duplicate code; I just didn't think of it until afterward :)* 


As before, the act of querying the db is managed by the ``queryRDS.bash`` script. At this point, I'd recommend opening ``sample-query.sql`` in one window and having a shell prompt in this project directory in another window. Start by editing ``sample-query.sql`` so that only the first ``SELECT`` statement will run. Then, progress through them commenting and uncommenting as you go. Below are short explanations of the concept introduced in each command: 

- The first query is about as simple as it gets: a basic ``SELECT``. This should simply return all the rows (``*`` wildcard) from the ``users_personal`` table. 
- The second query introduces a table alias (``users_work AS w``) and a ``JOIN`` across the two tables using the ``WHERE`` condition that the ids match. In the ``WHERE`` condition, we can use the previously-defined table aliases. Note that ``JOIN`` on its own is an implicit ``INNER JOIN``. For the other types of ``JOIN``s, see the visual reference below. 
- The third query introduces shorthand for aliasing (this time on rows and tables): when a new term immediately follows a column or table name, it is implicitly treated as an alias for the thing that preceeds it. In this case, ``SELECT first_name AS first, ...`` would be equivalent. You can see the resulting aliases in the output.
- The fourth query includes two additional ``WHERE`` clauses: a full string match (``w.department="data science"``), and a substring match (``LIKE``). The ``%``s are wildcard characters that allow any other characters to appear in those positions. 
- Finally, the fifth query introduces a built-in match command, ``COUNT``, which requires aggregates the result of the remainder of the query. In this case, we calculate the inner join of the two tables and group by ``department`` which allows us to ``COUNT`` the total number of rows in each ``department`` grouping. 






Finally, here are a couple of additional references that I find helpful to keep bookmarked:

- [visual reference for JOIN geometry](http://www.codinghorror.com/blog/2007/10/a-visual-explanation-of-sql-joins.html)
- [all the gory details on how SQL joins work]( http://en.wikipedia.org/wiki/Join_(SQL) )




