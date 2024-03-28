import psycopg2

def sql_start():

  global conn, cur
  conn = psycopg2.connect('voice_holiday_db')
  cur = conn.cursor()
  if conn:
    print('Подключение в базе данных...')
    print('База данных подключена')
  else:
    print('Не удалось подключится к базе данных')
  try:
    cur.execute(
    """CREATE TABLE IF NOT EXISTS user( 
      user_id INTEGER NOT NULL,
      username TEXT NOT NULL,
      chat_id INTEGER NOT NULL,
      is_admin INTEGER DEFAULT (0) NOT NULL,
      application_form_id INTEGER,
      CONSTRAINT user_pk PRIMARY KEY (username),
      CONSTRAINT user_application_form_FK FOREIGN KEY (application_form_id) REFERENCES application_form(id) ON DELETE SET NULL
    );
    """)

  except psycopg2.Error as error:
    print("Ошибка при работе с SQLite", error)
  finally:
    if conn:
      conn.close()
      print("Соединение с SQLite закрыто.\nБАЗА ДАННЫХ СОЗДАНА")