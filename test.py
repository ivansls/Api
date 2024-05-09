import psycopg2

conn = psycopg2.connect(dbname="Magazine", user="root", password="NasSidAdmin789", host="109.238.83.39", port="5665")
print("Подключение установлено")
conn.close()