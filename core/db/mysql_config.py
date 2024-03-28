import psycopg2

connection = psycopg2.connect(
  host='127.0.0.1',
  port=3306,
  user='userAdministrator',
  password='adminMGOK11!',
  database='voice_holiday_db'
)