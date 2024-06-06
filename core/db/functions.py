import sqlite3
con = sqlite3.connect("voice-holiday.db")
#------------------   Класс для работы с БД  ------------------
class ActionORM:
    """ Класс для работы ORM """
#------------------    CRUD Праздников   -------------------
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
                    'id': holiday[0],
                    'name': holiday[1],
                }
                holidays_list.append(holidays_dict)
            # print(holidays_list)
    
            return holidays_list
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)

#------------------    CRUD шаблонов   -------------------
    def get_templates(id) -> dict:
        """ Ф-я получения праздников """
        cur = con.cursor()
        try:
            query = """
                SELECT ph.id, p."text" 
                FROM pattern_holiday ph
                JOIN pattern p 
                ON ph.pattern_id = p.id 
                WHERE ph.holiday_id == ?
            """
            cur.execute(query, (id,))
            templates = cur.fetchall()
            templates_list = []
            for template in templates:
                templates_dict = {
                    'id': template[0],
                    'text': template[1],
                }
                templates_list.append(templates_dict)
            # print(templates_dict)
    
            return templates_list
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)


    def get_template(id) -> str:
        """ Ф-я  Получение шаблона """
        cur = con.cursor()
        try:
            query = """
                SELECT "text" FROM pattern
                WHERE id == ?
            """
            cur.execute(query, (id,))
            template_text = cur.fetchall()
            # print(template_text)

            return template_text
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)


    def add_template(template_text):
        """ Ф-я добавления шаблона """
        cur = con.cursor()
        try:
            query = """
                INSERT INTO pattern
                (id, "text")
                VALUES(None, ?);
            """
            cur.execute(query, (template_text,))
            result = cur.fetchone()
            return result
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)


    def delete_template(id):
        """ Ф-я удаления шаблона """
        cur = con.cursor()
        try:
            query = """
                DELETE FROM pattern
                WHERE id=?;
            """
            cur.execute(query, (id,))
            result = cur.fetchone()
            return result
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)