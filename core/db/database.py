import psycopg2
from core.db.postgres_config import conn

def sql_start():
  conn.autocommit = True
  cur = conn.cursor()

  try:
    if conn:
      print('Подключение в базе данных...')
      print('База данных подключена')
      
    else:
      print('Не удалось подключится к базе данных')

      # Создание БД
      cur.execute("""
      CREATE DATABASE voice_holiday
      WITH
      OWNER = "userAdministrator"
      ENCODING = 'UTF8'
      LC_COLLATE = 'Russian_Russia.utf8'
      LC_CTYPE = 'Russian_Russia.utf8'
      LOCALE_PROVIDER = 'libc'
      CONNECTION LIMIT = -1
      IS_TEMPLATE = False;""")

      cur.execute("""
      CREATE TABLE IF NOT EXISTS public.student_group
      (
        id integer NOT NULL,
        name character varying(50) COLLATE pg_catalog."default" NOT NULL,
        CONSTRAINT student_group_pkey PRIMARY KEY (id)
      )
      """)

      cur.execute("""
      CREATE TABLE IF NOT EXISTS public."user"
      (
        id bigint NOT NULL,
        firstname character varying(50) COLLATE pg_catalog."default" NOT NULL,
        lastname character varying(50) COLLATE pg_catalog."default" NOT NULL,
        datebirthday date,
        student_group_id integer,
        CONSTRAINT user_pkey PRIMARY KEY (id)
      )
      """)
      cur.connection.commit()
  except psycopg2.Error as error:
    print("Ошибка при работе с PostgreSQL", error)
  finally:
    if conn:
      print("Соединение с PostgreSQL открыто.")