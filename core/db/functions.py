import sqlite3
import aiosqlite
con = sqlite3.connect("voice-holiday.db")
#------------------   Класс для работы с БД  ------------------
class ActionORM:
    """ Класс для работы ORM """
#------------------    CRUD Праздников   -------------------
    async def get_holidays() -> dict:
        """ Ф-я получения праздников """
        async with aiosqlite.connect('voice-holiday.db') as con:
            async with con.cursor() as cur:
                try:
                    await cur.execute("SELECT id, name FROM holiday;")
                    holidays = await cur.fetchall()
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
                    print("Ошибка в добавлении шаблона", error)
                    result = f"Ошибка в добавлении шаблона, {error}"
                    return result


    async def add_holiday(name_holiday: str) -> str:
        """ Ф-я добавления праздников """
        async with aiosqlite.connect('voice-holiday.db') as con:
            async with con.cursor() as cur:
                try:
                    query = """
                        INSERT INTO holiday
                        (name)
                        VALUES(?);
                    """
                    await cur.execute(query, (name_holiday,))
                    await con.commit()
                    holiday_id = cur.lastrowid
                    result = f"Паздник c id {holiday_id} добавлен"
                    print(result)
                    return result
                except aiosqlite.Error as error:
                    await con.rollback()
                    print("Ошибка при работе с SQLite", error)
                    return f"Ошибка в добавлении праздника {error}"


    async def delete_holiday(holiday_id: int) -> str:
        """ Ф-я удвления праздников """
        cur = con.cursor()
        try:
            query = """
                DELETE FROM holiday
                WHERE id=?;
            """
            cur.execute(query, (holiday_id,))
            con.commit()
            result = f"Праздник удален"
            print(result)
            return result
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)
        finally:
            cur.close()

#------------------    CRUD шаблонов   -------------------
    async def get_templates(holiday_id: int) -> list:
        """ Функция получения шаблонов для праздников """
        async with aiosqlite.connect('voice-holiday.db') as con:
            async with con.cursor() as cur:
                try:
                    query = """
                        SELECT ph.id, p."text"
                        FROM pattern_holiday ph
                        JOIN pattern p
                        ON ph.pattern_id = p.id
                        WHERE ph.holiday_id == ?
                        LIMIT 50;
                    """
                    await cur.execute(query, (holiday_id,))
                    templates = await cur.fetchall()
                    templates_list = [
                        {
                            'id': template[0], 
                            'text': template[1]
                        } for template in templates
                    ]
                    return templates_list
                except aiosqlite.Error as error:
                    print("Ошибка при работе с SQLite", error)
                    return []


    async def get_template(pattern_id: int) -> str:
        """ Функция получения шаблона """
        async with aiosqlite.connect('voice-holiday.db') as con:
            async with con.cursor() as cur:
                try:
                    query = """
                        SELECT "text" FROM pattern
                        WHERE id == ?
                    """
                    await cur.execute(query, (pattern_id,))
                    template_text = await cur.fetchone()
                    return template_text[0] if template_text else ""
                except aiosqlite.Error as error:
                    print("Ошибка при работе с SQLite", error)
                    return f"Ошибка в работе {error}"


    async def add_template_for_holiday(holiday_id: int, pattern_text: str) -> str:
        """ Функция добавления шаблона для праздника """
        async with aiosqlite.connect('voice-holiday.db') as con:
            async with con.cursor() as cur:
                try:
                    # Вставка нового шаблона в таблицу pattern
                    await cur.execute("INSERT INTO pattern (text) VALUES (?)", (pattern_text,))
                    # Получение id вставленного шаблона
                    pattern_id = cur.lastrowid

                    # Вставка записи в таблицу pattern_holiday
                    await cur.execute("INSERT INTO pattern_holiday (pattern_id, holiday_id) VALUES (?, ?)", (pattern_id, holiday_id))

                    # Сохранение изменений
                    await con.commit()
                    result = f"Шаблон с id {pattern_id} добавлен для праздника с id {holiday_id}"
                    return result
                except aiosqlite.Error as error:
                    await con.rollback()
                    print("Ошибка в добавлении шаблона", error)
                    return f"Ошибка в добавлении шаблона, {error}"


    async def delete_template(pattern_id: int) -> str:
        """ Функция удаления шаблона """
        async with aiosqlite.connect('voice-holiday.db') as con:
            async with con.cursor() as cur:
                try:
                    await cur.execute("DELETE FROM pattern_holiday WHERE pattern_id=?;", (pattern_id,))
                    # Удаление из таблицы pattern
                    await cur.execute("DELETE FROM pattern WHERE id=?;", (pattern_id,))
                    await con.commit()
                    result = "Удаление завершено успешно"
                    return result
                except aiosqlite.Error as error:
                    await con.rollback()
                    print("Ошибка при работе с SQLite", error)
                    return f"Ошибка в удалении шаблона, {error}"