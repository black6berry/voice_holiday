import psycopg2
from core.db.postgres_config import conn

#----------------------------------------------------
#           CRUD Пользователей                      |
#----------------------------------------------------
""" Ф-я получения пользователей """
def get_users() -> list:
  cur = conn.cursor()
  try:
    query = """
      SELECT id, firstname, lastname, datebirthday, student_group_id
      FROM public."user";
    """
    cur.execute(query)
    users = cur.fetchone()
    user_list = []
    for user in users:
      group_dict = {
        'ID': user[0],
        'Name': user[1],
      }
      user_list.append(group_dict)
    
    return users
  except psycopg2.Error as error:
    print("Ошибка при работе с SQLite", error)
  finally:
    if conn:
      conn.close()
      print("Соединение с SQLite закрыто")


""" Ф-я создания пользователя """
def add_user(user_id, username, chat_id, is_admin) -> int:
  cur = conn.cursor()
  try:
    query = """ INSERT INTO user 
              (user_id, 
              username, 
              chat_id, 
              is_admin) 

              VALUES (?, ?, ?, ?)
              """
  
    cur.execute(query,(
      user_id, 
      username, 
      chat_id, 
      is_admin, 
    ))
    print("ПОЛЬЗОВАТЕЛЬ СОЗДАН")
    conn.commit()
    user_id = cur.lastrowid.__init__
    return user_id
  except psycopg2.Error as error:
    print("Ошибка при работе с SQLite", error)
  finally:
    if conn:
      conn.close()
      print("Соединение с SQLite закрыто")


#----------------------------------------------------
#                   CRUD Групп                      |
#----------------------------------------------------
""" Вывод групп """
def get_groups() -> list:
  cur = conn.cursor()
  try:
    query = """ 
      SELECT * FROM public.student_group
      ORDER BY id ASC 
      LIMIT 50
    """
    cur.execute(query)
    groups = cur.fetchall()
    group_list = []
    for group in groups:
      group_dict = {
        'ID': group[0],
        'Name': group[1],
      }
      group_list.append(group_dict)

    return group_list
  except psycopg2.Error as error:
    print("Ошибка при работе с SQLite", error)
  finally:
    if conn:
      conn.close()
      print("Соединение с SQLite закрыто")


def get_birthday_text() -> str:
  pass
