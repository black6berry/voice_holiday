import psycopg2
from core.db.postgres_config import conn

def sql_start():
    """Ф-я создания/подключения к БД"""
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
                    OWNER = "useradministrator"
                    ENCODING = 'UTF8'
                    LC_COLLATE = 'Russian_Russia.utf8'
                    LC_CTYPE = 'Russian_Russia.utf8'
                    LOCALE_PROVIDER = 'libc'
                    CONNECTION LIMIT = -1
                    IS_TEMPLATE = False;""")

            cur.execute("""
                CREATE TABLE public."user" (
                    id int8 GENERATED ALWAYS AS IDENTITY NOT NULL,
                    firstname varchar NOT NULL,
                    lastname varchar NOT NULL,
                    datebirthday date NOT NULL,
                    CONSTRAINT user_pk PRIMARY KEY (id)
                );
            """)

            cur.execute("""
                CREATE TABLE public.congratulation (
                    id int4 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1 NO CYCLE) NOT NULL,
                    "text" varchar NOT NULL,
                    CONSTRAINT congratulation_pk PRIMARY KEY (id)
                );
            """)
            cur.connection.commit()
    except psycopg2.Error as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if conn:
            print("Соединение с PostgreSQL открыто.")