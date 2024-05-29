import psycopg2


# Connect to your postgres DB
conn=psycopg2.connect(
  database="books_demo",
  user="postgres",
#  host="/tmp/",
#  password="Spock"
)

# Open a cursor to perform database operations
cur = conn.cursor()

#cur.execute('INSERT INTO book VALUES ('Демиан', 9785, 'Герман Гессе')')
# Execute a query
cur.execute("SELECT * FROM book")

# Retrieve query results
records = cur.fetchall()

print(records)

# Зафиксировать изменения
conn.commit()
# Вывести число измененных или удаленных строк
print(cur.rowcount)
#Закрыть соединение
conn.close()