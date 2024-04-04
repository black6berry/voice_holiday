import psycopg2

conn = psycopg2.connect(
  host='127.0.0.1',
  port=5432,
  user='userAdministrator',
  password='adminMGOK11!',
  database='voice_holiday'
)