"""в этом файле хранятся функции работающие с базой и команды к ним"""


import sqlite3 #импорт sqlite3 и исключений
from sqlite3 import Error


def create_connection(path): # создает соединение с базой
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def execute_query(connection, query): #добавляет значения
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

def execute_read_query(connection, query):#получает значения
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

def execute_сount_query(connection, query):#тоже получает  но вывод дает длину таблицы(int)
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return (len(result))
    except Error as e:
        print(f"The error '{e}' occurred")

create_data_table = """ 
CREATE TABLE IF NOT EXISTS data (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  i INTEGER,
  j INTEGER,
  tij INTEGER
);
"""
#создает таблицу data
create_calculation_table = """
CREATE TABLE IF NOT EXISTS calculation(
	id INTEGER PRIMARY KEY,
	i INTEGER,
	j INTEGER,
	tij INTEGER,
	Tri INTEGER,
	Tpi INTEGER,
	Ri INTEGER
);
"""
#создает таблицу calculation
delete_data = """
DROP TABLE IF EXISTS data;
"""
delete_calculation = """
DROP TABLE IF EXISTS calculation;
"""
#прям все удаляет насовсем но проверяет есть ли что удалять
select_data = "SELECT * from data" 
#выкладывает все данные из таблицы data
select_i = "SELECT id,i from data"
#выкладывает конкретно три столбца
connection = create_connection("C:\\IO\\sm_app.sqlite")
#создает соединение