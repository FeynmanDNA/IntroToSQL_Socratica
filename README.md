## from Socratica 2019 SQL tutorials

SQL generally ends with semi-colons.

In tables, there are columns with names ending in ID, these are numbers that uniquely identify each row of data. Such values are called "primary keys".

Generally you will use software to insert data.

The SELECT statement gives you the ability to choose data from multiple tables in a process called "JOINs".

A related solution would be to create a virtual table called a "View". This virtual table or table-like object collects matching data from multiple tables and make it easily accessible as if you are working with a single table.

**Speed**: when you execute a SELECT statement with a WHERE clause, the database may have to look at every single record in the table to find matching data. An Index can be created to ensure your queries are fast and efficient.

Transactions provide you the ability to make several changes and ensure that your data is safe if there is a problem part-way along the process.

So main features: **Joins, Views, Indexes, Transactions**

### postgreSQL for linux

We need a relational database, because we use SQL to talk to such systems.

Transferrable Skills:
- SQL
- Schema Design
- Database Optimization

Postgres mascot is elephant, because "elephants never forget"

install postgreSQL client and pgadmin4 for debian

**IMPORTANT**: set up postgres user and password for pgadmin4
```
sudo su postgres
postgres@debian:psql
postgres=# \password postgres (password = xxx)
```

### using pgadmin4

in pgadmin4, create new server: name = localhost, connection/hostname = localhost

Postgres GUI tool is pgadmin

pgAdmin sidebar shows "server group", a server group is a container for organizing your servers.

whenever you make changes in the pgadmin, look at the SQL tab.

To see how many tables there are, open the "schemas" folder. By default database has a public schema.

## SELECT

databases can have many many tables

SELECT can retrieve data from one table or multiple tables with a technique called JOINS

the earthquake csv is from US Geological Science Survey, it contains:
- Event Type: Earthquake
- Magnitude Range: 5.5+
- Date Range: 1969 - 2018

This table contains 10 columns: `earthquake_id`, `occurred_on`, `latitude`, `longitude`, `depth`, `magnitude`, `calculation_method`, `network_id`, `place`, and `cause`

`earthquake_id` is the primary key of the table, primary key is a value that uniquely identifies each row in the table

how to import the 'earthquake' table:

1. in pgAdmin: Tools - Query Tool
2. input this in the Query Editor:

    ```sql
    CREATE TABLE public.earthquake
    (
        earthquake_id integer NOT NULL,
        occurred_on timestamp without time zone,
        latitude numeric,
        longitude numeric,
        depth numeric,
        magnitude numeric,
        calculation_method character varying,
        network_id character varying,
        place character varying,
        cause character varying,
        CONSTRAINT earthquake_pkey PRIMARY KEY (earthquake_id)
    )
    WITH (
        OIDS = FALSE
    )
    ```

3. now execute (F5)
4. right-click the 'earthquake' table
5. use Import (make sure the 'Header' switch is set to 'Yes')

```sh
 "/usr/bin/psql" --command " "\\copy public.earthquake (earthquake_id, occurred_on, latitude, longitude, depth, magnitude, calculation_method, network_id, place, cause) FROM '/home/svd/Documents/Learn/SQL/earthquake.csv' CSV HEADER QUOTE '\"' ESCAPE '''';""
```

Q: How to see the whole table? *

```sql
SELECT * FROM earthquake;
```

this has two parts, Select xxx lists the **columns** you want data for, the FROM xxx specifies which **tables** to select data from.

Q: How many rows are there in this table? COUNT

there are functions you can use in your queries~

```sql
SELECT COUNT(*) FROM earthquake;
```

for this query, we select a `COUNT` rather than the data itself.

Notice that the name of the columnin the rowset is "count", this is the **name of the function**, not the name of any column in our table

**speed**:
- SELECT *: 279 msec
- SELECT COUNT(*): 104 msec

Q: specific select with WHERE

```sql
SELECT magnitude, place, occurred_on FROM earthquake;
```

to see the specific columns (the column order does not matter in the query)

In addition to the SELECT and FROM keywords, there is a third valuable part of queries: **WHERE**
- SELECT: columns
- FROM: table
- WHERE: rows condition AND condition OR condition
- ORDER BY: asec/desc
- LIMIT: restrict returned rows

Q: all earthquakes that occurred on or after jan 1 2000:

```sql
SELECT *
FROM earthquake
WHERE occurred_on >= '2000-01-01';
```

Q: What was the largest earthquake in 2010?

```sql
SELECT *
FROM earthquake
WHERE occurred_on >= '2010-01-01' AND occurred_on <= '2010-12-31'
ORDER BY magnitude DESC
LIMIT 1;
```

To restrict the number of rows returned, use `LIMIT` keyword


some other common SQL functions are COUNT, MIN, MAX, AVG, SUM

SELECT MIN(occurred_on), MAX(occurred_on) FROM earthquake

Q: What magnitude range is covered by the table?
SELECT MIN(magnitude), MAX(magnitude) FROM earthquake


we only need to select 1 row to see all the columns
SELECT * FROM earthquake LIMIT 1;

SELECT DISTINCT will make sure we do not see duplicate rows

SELECT COUNT(*) FROM earthquake WHERE cause='nuclear explosion'

**NOTE: SQL ' and " are different! you should use '**

Q: Find the most recent earthquake caused by a nuclear explosion?
SELECT * FROM earthquake WHERE cause = 'nuclear explosion' ORDER BY occurred_on DESC LIMIT 5

Q: How can we count the number of aftershocks?
Idea; find quakes with "Honshu" and "Japan" in the 'place' text and occurred within a week of the March 11th quake
SELECT * FROM earthquake WHERE place LIKE '%Honshu%Japan%'
AND occurred_on BETWEEN '2011-03-11' AND '2011-3-18'

'%x' is a string pattern, the % symbol matches zero or more characters
BETWEEN...AND is another operator
