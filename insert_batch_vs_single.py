import psycopg2
import time

# N = number of rows to add in each batch
N = 10000

# the user_id, post_text value to insert
each_insert_value = "(1, 'ice mountain?')"

# Generate single INSERT INTO query
single_query = """INSERT INTO post (user_id, post_text)
  VALUES {};""".format(each_insert_value)

# print("single_query: ", single_query)

# Generate a single big INSERT INTO query
big_query = "INSERT INTO post (user_id, post_text) VALUES "
# print("big_query: ", big_query)

# insert N rows separately by commas
big_query += (each_insert_value + ', ') * (N-1)
# end with a semi-colon
big_query += (each_insert_value + ';')
# print("big_query: ", big_query)

# Connect to database
conn = psycopg2.connect(
  "dbname=socratica user=postgres password=5421"
)
# print("conn: ", conn)

# Create a cursor
cur = conn.cursor()
# print("cur:", cur)

# Time the two methods
start_time = time.time()
for i in range(N):
  cur.execute(single_query)
conn.commit()
stop_time = time.time()

print("single query method took: {} seconds".format(stop_time-start_time))

start_time = time.time()
cur.execute(big_query)
conn.commit()
stop_time = time.time()

print("\nbig query method took: {} seconds".format(stop_time-start_time))

# Close both cursor and database connection
cur.close()
conn.close()
