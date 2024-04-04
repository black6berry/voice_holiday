import psycopg2
from core.db.postgres_config import conn


""" Ф-я получения пользователя """
def get_user(username) -> bool:
  cur = conn.cursor()
  try:
    query = """ SELECT username
              FROM user 
              WHERE username=?
              """
    cur.execute(query,( username, ))
    result = cur.fetchone()
    if result:
      return True
    else:
      return False
    
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



""" Создаем новую заявку """
def add_application_form(
    datetime_create,
    user_FIO="", 
    phone_number="", 
    INN="", 
    monthly_revenue_company="", 
    monthly_loan_payments="", 
    desired_loan_amount="", 
    loan_term="") -> int:

  cur = conn.cursor()
  try:
    query = """ INSERT INTO application_form
                                          (user_FIO, 
                                          phone_number, 
                                          INN, 
                                          monthly_revenue_company, 
                                          monthly_loan_payments, 
                                          desired_loan_amount, 
                                          loan_term, 
                                          datetime_create)

                                          VALUES(?, ?, ?, ?, ?, ?, ?, ?)
                                          """
    cur.execute(query, (
      user_FIO, 
      phone_number, 
      INN, 
      monthly_revenue_company, 
      monthly_loan_payments, 
      desired_loan_amount, 
      loan_term,
      datetime_create))
    conn.commit()
    application_id = cur.lastrowid
    return application_id
  except psycopg2.Error as error:
    print("Ошибка при работе с SQLite", error)
  finally:
    if conn:
      conn.close()
      print("Соединение с SQLite закрыто")


""" Обновление данных заявки """
def update_application_form(
    datetime_create,
    application_form_id,
    user_FIO="", 
    phone_number="", 
    INN="", 
    monthly_revenue_company="", 
    monthly_loan_payments="", 
    desired_loan_amount="", 
    loan_term="") -> int:

  cur = conn.cursor()
  
  try: 
    query = """ UPDATE application_form
                SET
                user_FIO=?, 
                phone_number=?, 
                INN=?, 
                monthly_revenue_company=?, 
                monthly_loan_payments=?, 
                desired_loan_amount=?, 
                loan_term=?, 
                datetime_create=?

                WHERE id=?
              """
  
    cur.execute(query, (
      user_FIO, 
      phone_number, 
      INN, 
      monthly_revenue_company, 
      monthly_loan_payments, 
      desired_loan_amount, 
      loan_term,
      datetime_create,
      application_form_id))
    conn.commit()
    application_id = cur.lastrowid
    print(application_id)
    return application_id
  except psycopg2.Error as error:
    print("Ошибка при работе с SQLite", error)
  finally:
    if conn:
      conn.close()
      print("Соединение с SQLite закрыто")


""" Ф-я обновления id заявки пользователя """
def update_user_application_form_id(new_application_form_id, username):
  cur = conn.cursor()
  try: 
    query = """ 
      UPDATE user 
      SET application_form_id=?
      WHERE username=? 
    """
    cur.execute(query, (new_application_form_id, username))
    conn.commit()
  except psycopg2.Error as error:
    print("Ошибка при работе с SQLite", error)
  finally:
    if conn:
      conn.close()
      print("Соединение с SQLite закрыто")



""" Получить id заявки """
def get_application_form_id(username) -> int:
  cur = conn.cursor()
  try:
    query = """
      SELECT application_form_id
      FROM "user"
      WHERE username=?
    """
    cur.execute(query, (username,))
    result = cur.fetchone()
    print(result[0])
    return result[0]
  except psycopg2.Error as error:
    print("Ошибка при работе с SQLite", error)
  finally:
    if conn:
      conn.close()
      print("Соединение с SQLite закрыто")