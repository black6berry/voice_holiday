import sqlite3
con = sqlite3.connect("voice-holiday.db")
#------------------   Класс для работы с БД  ------------------
class ActionORM:
    """ Класс для работы ORM """
#------------------    CRUD Пользователей   -------------------
    def get_holidays() -> dict:
        """ Ф-я получения праздников """
        cur = con.cursor()
        try:
            query = """
                SELECT id, name
                FROM holiday;
            """
            cur.execute(query)
            holidays = cur.fetchall()
            holidays_list = []
            for holiday in holidays:
                holidays_dict = {
                    'ID': holiday[0],
                    'name': holiday[1],
                }
                holidays_list.append(holidays_dict)
            print(holidays_list)
    
            return holidays_list
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)


    def add_user(self, user_id, username, chat_id, is_admin) -> int:
        """ Ф-я создания пользователя """
        try:
            with con.cursor() as cur:
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
                con.commit()
                user_id = cur.lastrowid.__init__
            return user_id
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)


#------------------    CRUD Групп  -------------------
    def get_groups() -> list:
        """ Вывод групп """
        try:
            # cur = conn.cursor()
            with con.cursor() as cur:
                query = """
                    SELECT * FROM public.student_group
                    ORDER BY id ASC 
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
                print(group_list)

            return group_list
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)


#------------------    CRUD Текстов поздравлений   -------------------
    def get_congratulations() -> list:
        """ Получение текстов поздравлений """
        try:
            with con.cursor() as cur:
                query = """
                    SELECT id, "text"
                    FROM public.congratulation;
                """
                cur.execute(query)
                congratulation_template_text = cur.fetchall()
                congratulations_list = []
                for birthday_text in congratulation_template_text:
                    group_dict = {
                        'ID': birthday_text[0],
                        'Name': birthday_text[1],
                    }
                    congratulations_list.append(group_dict)
                print(congratulations_list)

            return congratulations_list
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)