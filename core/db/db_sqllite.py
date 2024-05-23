import sqlite3

def sql_start():
    """Ф-я создания/подключения к БД"""
    con = sqlite3.connect("voice-holiday.db")
    cur = con.cursor()

    try:
        if con:
            print('Подключение в базе данных...')

            # Создаем таблицу holiday
            cur.execute('''
            CREATE TABLE IF NOT EXISTS holiday (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
            ''')

            # Создаем таблицу pattern
            cur.execute('''
            CREATE TABLE IF NOT EXISTS pattern (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                "text" TEXT NOT NULL
            );
            ''')

            cur.execute('''
            CREATE TABLE IF NOT EXISTS pattern_holiday (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_id INTEGER NOT NULL,
                holiday_id INTEGER NOT NULL,
                FOREIGN KEY (pattern_id) REFERENCES pattern(id),
                FOREIGN KEY (holiday_id) REFERENCES holiday(id)
            )
            ''')

            # Сохраняем изменения
            con.commit()

            print('База данных подключена')

        else:
            print('Не удалось подключится к базе данных')

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLITE", error)
    finally:
        if con:
            print("Соединение с SQLITE открыто.")