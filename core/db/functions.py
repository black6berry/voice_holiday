import sqlite3
con = sqlite3.connect("voice-holiday.db")
#------------------   Класс для работы с БД  ------------------
class ActionORM:
    """ Класс для работы ORM """
#------------------    CRUD Праздников   -------------------
    async def get_holidays() -> dict:
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
        finally:
            cur.close()

#------------------    CRUD шаблонов   -------------------
    async def get_templates(holiday_id: int) -> dict:
        """ Ф-я получения праздников """
        cur = con.cursor()
        try:
            query = """
                SELECT ph.id, p."text" 
                FROM pattern_holiday ph
                JOIN pattern p 
                ON ph.pattern_id = p.id 
                WHERE ph.holiday_id == ?
                LIMIT 50;
            """
            cur.execute(query, (holiday_id,))
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
        finally:
            cur.close()


    async def get_template(pattern_id) -> str:
        """ Ф-я  Получение шаблона """
        cur = con.cursor()
        try:
            query = """
                SELECT "text" FROM pattern
                WHERE id == ?
            """
            cur.execute(query, (pattern_id,))
            template_text = cur.fetchall()
            # print(template_text)

            return template_text
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)
        finally:
            cur.close()


    async def add_template_for_holiday(holiday_id: int, pattern_text: str) -> str:
        """ Ф-я добавления шаблона """
        cur = con.cursor()
        try:
            # Вставка нового шаблона в таблицу pattern
            cur.execute("INSERT INTO pattern (text) VALUES (?)", (pattern_text,))
            # Получение id вставленного шаблона
            pattern_id = cur.lastrowid

            # Вставка записи в таблицу pattern_holiday
            cur.execute("INSERT INTO pattern_holiday (pattern_id, holiday_id) VALUES (?, ?)", (pattern_id, holiday_id))

            # Сохранение изменений
            con.commit()
            result = f"Шаблон с id {pattern_id} добавлен для праздника с id {holiday_id}"
            return result
        except sqlite3.Error as error:
            print("Ошибка в добавлении шаблона", error)
            result = f"Ошибка в добавлении шаблона, {error}"
            return result
        finally:
            cur.close()


    async def delete_template(pattern_id: int) -> str:
        """ Ф-я удаления шаблона """
        cur = con.cursor()
        try:
            cur.execute("DELETE FROM pattern_holiday WHERE pattern_id=?;", (pattern_id,))
            # Удаление из таблицы pattern
            cur.execute("DELETE FROM pattern WHERE id=?;", (pattern_id,))
            # Завершение транзакции
            con.commit()
            result = "Удаление завершено успешно"
            return result
        except sqlite3.Error as error:
            # Откат транзакции в случае ошибки
            # con.rollback()
            print("Ошибка при работе с SQLite", error)
            result = f"Ошибка в удалении шаблона, {error}"
            return result
        finally:
            cur.close()