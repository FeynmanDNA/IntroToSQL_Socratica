## from Socratica 2019 SQL tutorials

### postgreSQL for debian
install postgreSQL client and pgadmin4 for debian

**IMPORTANT**: set up postgres user and password for pgadmin4
```
sudo su postgres
postgres@debian:psql
postgres=# \password postgres (password = xxx)
```

in pgadmin4, create new server: name = localhost, connection/hostname = localhost

databases can have many many tables

SELECT can retrieve data from one table or multiple tables with a technique called JOINS

the earthquake csv is from US Geological Science Survey

earthquake_id is the primary key of the table, primary key is a value that uniquely identifies each row in the table

how to import the 'earthquake' table:

1. in pgAdmin: Tools - Query Tool
2. input this in the Query Editor:

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

3. now execute (F5)
4. right-click the 'earthquake' table
5. use Import (make sure the 'Header' switch is set to 'Yes')


Q: How to see the whole table?
SELECT * FROM earthquake

Q: How many rows are there in this table?
SELECT COUNT(*) from earthquake
to see the count, Count is the name of the function, not the name of any column in our table

some other common SQL functions are COUNT, MIN, MAX, AVG, SUM

SELECT MIN(occurred_on), MAX(occurred_on) FROM earthquake

Q: What magnitude range is covered by the table?
SELECT MIN(magnitude), MAX(magnitude) FROM earthquake

SELECT magnitude, place, occurred_on FROM earthquake to see the specific columns

Q: What was the largest earthquake in 2016?
SELECT *
FROM earthquake
WHERE occurred_on >= '2016-01-01' AND occurred_on <= '2016-12-31'
ORDER BY magnitude DESC
LIMIT 1;

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
