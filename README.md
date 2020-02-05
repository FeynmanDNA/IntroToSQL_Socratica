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
- ORDER BY: asc/desc
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

Q: how to see the columns of a database?

we only need to select 1 row to see all the columns `SELECT * FROM earthquake LIMIT 1;`

Q: SQL functions:

some other common SQL functions are COUNT, MIN, MAX, AVG, SUM

```sql
SELECT MIN(occurred_on), MAX(occurred_on) FROM earthquake;
```

Q: What magnitude range is covered by the table?

```sql
SELECT MIN(magnitude), MAX(magnitude) FROM earthquake;
```

Q: what are the causes for earthquake? DISTINCT

many earthquakes have the same cause, so a lot of duplicates

SELECT DISTINCT will make sure we do not see duplicate rows

```sql
SELECT DISTINCT cause FROM earthquake;
```

Q: how many earthquakes are caused by nuclear explosion?

```sql
SELECT COUNT(*) FROM earthquake WHERE cause='nuclear explosion';
```

**NOTE: SQL `'` and `"` are different! you should use SINGLE QUOTE: `'`**

Q: Find the most recent earthquake caused by a nuclear explosion?

```sql
SELECT magnitude, place, occurred_on
FROM earthquake
WHERE cause = 'nuclear explosion'
ORDER BY occurred_on DESC
LIMIT 5;
```

Q: How can we count the number of aftershocks?

Idea; find quakes with "Honshu" and "Japan" in the 'place' text and occurred within a week of the March 11th quake

```sql
SELECT * FROM earthquake WHERE place LIKE '%Honshu%Japan%'
AND occurred_on BETWEEN '2011-03-11' AND '2011-3-18';
```

`'%x'` is a string pattern, the `%` symbol matches zero or more characters

`BETWEEN...AND` is another operator

## INSERT

The sample database will consist of several tables:
- `chitter_user` table
    - columns: `user_id`, `username`, `encrypted_password`, `email`, and `date_joined`
    - `user_id` will be the auto-generated primary key
- `post` table
    - columns: `post_id`, `user_id`, `post_text`, and `posted_on`
    - `post_id` will be the auto-generated primary key
- `follower` table
    - columns: `user_id` and `follower_id`

for `chitter_user` table:

```sql
CREATE TABLE public.chitter_user
(
    username text,
    user_id serial NOT NULL,
    encrypted_password text,
    email text,
    date_joined timestamp without time zone,
    PRIMARY KEY (user_id)
)
WITH (
    OIDS = FALSE
);

ALTER TABLE public.chitter_user
    OWNER to postgres;
```

for `post` table:

```sql
CREATE TABLE public.post
(
    post_id serial NOT NULL,
    user_id integer,
    post_text text,
    posted_on timestamp without time zone DEFAULT current_timestamp,
    PRIMARY KEY (post_id),
    CONSTRAINT user_id_constraint FOREIGN KEY (user_id)
        REFERENCES public.chitter_user (user_id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
)
WITH (
    OIDS = FALSE
);

ALTER TABLE public.post
    OWNER to postgres;
```

for `follower` table:

```sql
CREATE TABLE public.follower
(
    user_id integer NOT NULL,
    follower_id integer NOT NULL,
    PRIMARY KEY (user_id, follower_id),
    CONSTRAINT user_id_constraint FOREIGN KEY (user_id)
        REFERENCES public.chitter_user (user_id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT follower_id_constraint FOREIGN KEY (follower_id)
        REFERENCES public.chitter_user (user_id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
)
WITH (
    OIDS = FALSE
);

ALTER TABLE public.follower
    OWNER to postgres;
```

the listed columns for which you have data and the VALUES must be in the same order, the order of the data must match the order of the columns

user `DEFAULT` keyword as the user_id, this is because our database will generate this value for us

```sql
INSERT INTO chitter_user
	(user_id, username, encrypted_password, email, date_joined)
VALUES
	(DEFAULT, 'firstuser', 'd3dasdfi3', '1@1.com', '2019-02-21');
```

now try add user without specifying all fields, only insert for username and encrypted password

```sql
INSERT INTO chitter_user
    (username, encrypted_password)
VALUES
    ('seconduser', '878732ddui');
```

the user_id is generated for us, but other columns are NULL because we did not provide the values

insert into post table, using comma `,` to insert multiple entries

```sql
INSERT INTO post
    (user_id, post_text)
VALUES
    (1, 'hi, first post!'),
    (1, 'second post!!');
```

**speed:** measure speed of `INSERT` queries
**TEST:** insert 10,000 rows in two different ways, using Python with a Postgres database

**in order to talk to the database, we will use the popular 'psyco PG2' module** `import psycopg2`

NOTE: in order for psycopg2 to work, you need to change `pg_hba.conf` file (/etc/postgresql/9.1/main/pg_hba.conf*).

This line:
```
local   all             postgres                                peer
```
Should be:
```
local   all             postgres                                md5
```

so the login by password can be done via psycopg2

then restart postgresql `sudo service postgresql restart`

```
single query method took: 1.3434667587280273 seconds

big query method took: 0.11228609085083008 seconds
```

BUT NOTE: when inserting large volumes of data, the way you word your queries can make a big impact on how quickly they will run.

## UPDATE statement

a sample `secret_user` database, with the following schema:
columns: `user_id`, `first_name`, `last_name`, `code_name`, `country`, `organization`, `salary`, and `knows_kung_fu`

to update, use `UPDATE tablename SET clause`, and **specify the ROWS to make this change**. Use "WHERE" clause to specify rows to update

```sql
UPDATE secret_user
SET first_name = 'James'
WHERE user_id = 1;
```

like insert, you can make changes to multiple columns with one query using comma

```sql
UPDATE secret_user
SET code_name = 'Neo 2.0', salary = 115000
WHERE first_name = 'Jack' AND last_name = 'Ryan;
```

```sql
UPDATE table_name
SET column1 = value1, column2 = value2, column3 = value3, ...
WHERE conditions for rows;
```

**if you do not include a WHERE clause, the change will apply to EVERY ROW in the table!!!**

New operator: `IN`

```sql
UPDATE secret_user
SET knows_kung_fu = TRUE
WHERE user_id IN (5,7,8);
```

You can do calculations in the query!

```sql
UPDATE secret_user
SET salary = 1.1*salary;
```

Calculate the sum of the salaries:

```sql
SELECT SUM(salary)
FROM secret_user;
```