import sys
import sqlite3
import networkx as nx
from PyQt5 import QtCore, QtGui, QtWidgets, QtSql
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery 
from name import Ui_MainWindow
from PyQt5.QtGui import QIcon, QKeySequence,QIntValidator
from db import*
from name import*
from calculation import*#импорт всего чтобы все друг друга видели в данном документе
from draw import*

"""!!!логика приложения, вывод данных и запуск непосредственно!!!"""

execute_query(connection, create_data_table)
execute_query(connection, create_calculation_table)#создает таблицу если ее нет
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    QtWidgets.QApplication.setWindowIcon(QtGui.QIcon("web.png"))
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    def val_box():#берет из пин бокс данные , присваивает их переменным
    	tab_1 = ui.pin_box.value()
    	tab_2 = ui.pin_box_2.value()
    	tab_3 = ui.pin_box_3.value()
    	return [(tab_1,tab_2,tab_3)]# формат вывода нужен для запроса sql

    def db_add():# добавляет данные
    	parameters = val_box()
    	create_data = """
    	INSERT INTO
    	data (i,j,tij) VALUES (?,?,?);"""
    	create_calculation = """
    	INSERT INTO
    	calculation (i,j,tij) VALUES (?,?,?);"""
    	def execute_query_add(connection, query):#обращение к базе для добавления значений; здесь находится так как для запроса нужны переменные
    		cursor = connection.cursor()
    		try:
    			cursor.executemany(query,parameters)
    			connection.commit()
    			print("Query executed successfully")
    		except Error as e:
    			print(f"The error '{e}' occurred")
    	execute_query_add(connection, create_data)
    	execute_query_add(connection, create_calculation)

    def val_tri_tpi():
    	a, b, c = calc_ri()
    	G = a
    	count = 0
    	tuple_read = execute_read_query(connection,select_i)
    	while count < len(tuple_read):
    		fk_i = tuple_read[count]
    		v = fk_i[1]
    		id_s = fk_i[0]
    		if v in list(G.nodes()):
    			tri = G.nodes[v]['Tri']
    			tpi = G.nodes[v]['Tpi']
    			ri = G.nodes[v]['Ri']
    			parameters = tuple((tri,tpi,ri,id_s))
    			reate_calculation = "UPDATE calculation SET Tri =(?),Tpi =(?),Ri =(?) where id=(?)"
    			def execute_query_add(connection, query):
    				cursor = connection.cursor()
    				try:
    					cursor.execute(query,parameters)
    					connection.commit()
    					print("Query executed successfully")
    				except Error as e:
    					print(f"The error '{e}' occurred")
    			execute_query_add(connection,reate_calculation)
    		else:
    			pass
    		count += 1
    
    def db_delete():#удаляет данные. вообще все
    	execute_query(connection, delete_data)
    	execute_query(connection, delete_calculation)
    	execute_query(connection, create_calculation_table)
    	execute_query(connection, create_data_table)
    	ui.plainTextEdit.clear()

    def db_output():#выводит данные в форму на экране приложения
    	connect_qsql = QtSql.QSqlDatabase.addDatabase('QSQLITE')#драйвер к базе, обращается по имени и открывает
    	connect_qsql.setDatabaseName('sm_app.sqlite')
    	connect_qsql.open()

    	sql_table_data = QtSql.QSqlTableModel()#создает модель
    	sql_table_data.setTable("data")
    	sql_table_data.setEditStrategy(QSqlTableModel.OnFieldChange)
    	sql_table_data.select()

    	table_view = ui.tableView#связь модель с таблицей и немного поправляет вид до нормального. Левая таблица
    	table_view.setModel(sql_table_data)
    	table_view.setColumnWidth(1,10)
    	table_view.setColumnWidth(2,10)
    	table_view.setColumnWidth(3,10)
    	table_view.setColumnHidden(0, True)

    	sql_table_calculation = QtSql.QSqlTableModel()
    	sql_table_calculation.setTable("calculation")
    	sql_table_calculation.setEditStrategy(QSqlTableModel.OnFieldChange)
    	sql_table_calculation.select()

    	table_view_2 = ui.tableView_2#связь модель с таблицей и немного поправляет вид до нормального. Правая соответственно
    	table_view_2.setModel(sql_table_calculation)
    	table_view_2.setColumnWidth(1,2)# выглядит криво, я не нашла в документации как применить данное свойство разом ко всем столбикам
    	table_view_2.setColumnWidth(2,2)
    	table_view_2.setColumnWidth(3,2)
    	table_view_2.setColumnWidth(4,2)
    	table_view_2.setColumnWidth(5,2)
    	table_view_2.setColumnWidth(6,2)
    	table_view_2.setColumnWidth(7,2)
    	table_view_2.setColumnWidth(8,2)
    	table_view_2.setColumnWidth(9,2)
    	table_view_2.setColumnWidth(10,2)
    	table_view_2.setColumnHidden(0, True)

    	print_graph()
    def show():#вывод итога
    	a, b, c = calc_ri()
    	z = "Критический путь проходит по точкам: "+(str(b))+" "+"Длина критического пути равна: "+" "+(str(c))+" "+ "пункт(а,ов)"
    	plain_text = ui.plainTextEdit.setPlainText(z)

    ui.pushButton_2.clicked.connect(db_delete)#обработка нажатий
    ui.pushButton_2.clicked.connect(db_output)
    ui.pushButton_5.clicked.connect(db_add)
    ui.pushButton_5.clicked.connect(db_output)
    ui.pushButton_3.clicked.connect(val_tri_tpi)
    ui.pushButton_3.clicked.connect(show)
    ui.pushButton_8.clicked.connect(db_output)
    MainWindow.show()
    sys.exit(app.exec_())
