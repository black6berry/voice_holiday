import psycopg2
from core.db.postgres_config import conn

#------------------   Класс для работы с БД  ------------------
class ActionORM:
    """ Класс для работы ORM """
#------------------    CRUD Пользователей   -------------------
    def get_users() -> list:
        """ Ф-я получения пользователей """
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


    def add_user(user_id, username, chat_id, is_admin) -> int:
        """ Ф-я создания пользователя """
        try:
            with conn.cursor() as cur:
                query = """ 
                    INSERT INTO user 
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


#------------------    CRUD Групп  -------------------
    def get_groups() -> list:
        """ Вывод групп """
        try:
            # cur = conn.cursor()
            with conn.cursor() as cur:
                query = """ 
                    SELECT * FROM public.student_group
                    ORDER BY id ASC 
                    LIMIT 24
                """
                cur.execute(query)
                groups = cur.fetchall()
                group_list = []
                print(group_list)
                for group in groups:
                    group_dict = {
                        'ID': group[0],
                        'Name': group[1],
                    }
                    group_list.append(group_dict)

            return group_list
        except psycopg2.Error as error:
            print("Ошибка при работе с SQLite", error)


#------------------    CRUD Текстов поздравлений   -------------------
    def get_congratulations() -> str:
        """ Получение текстов поздравлений """
        try:
            with conn.cursor() as cur:
                query = """
                    SELECT id, "text"
                    FROM public.congratulation;
                """
            cur.execute(query)
            birthday_text = cur.fetchall()
            congratulations_list = []
            print(congratulations_list)
            for birthday_text in congratulations_list:
                group_dict = {
                    'ID': birthday_text[0],
                    'Name': birthday_text[1],
                }
                congratulations_list.append(group_dict)

            return congratulations_list
        except psycopg2.Error as error:
            print("Ошибка при работе с SQLite", error)