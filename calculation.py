"""!!! Данный файл реализует графы и расчеты в программе!!!"""

import networkx as nx #импорт библиотеки для графов, ниже импорт файла с командами базы
from db import* 

def add_edge_graph():# создает граф
	G = nx.DiGraph()#инициализация графа
	i = 1
	len_table = execute_сount_query(connection, select_data)#узнает длину таблицы для цикла
	reed_data = 'SELECT i,j, Tij from data WHERE id = (?);'

	while i <= len_table:#
		turple_i = (i,)
		def execute_read_id_query(connection, query):
		#^ функция общается с базой, она тут(а не в db) потому что участвует в цикле итерации, а аккуратнее я не умею сделать
			cursor = connection.cursor()
			result = None
			try:
				cursor.execute(query,turple_i)
				result = cursor.fetchall()
				return result
			except Error as e:
				print(f"The error '{e}' occurred")

		list_turple_id = execute_read_id_query(connection,reed_data)#получаем список кортежей одной строчки
		turple_id = list_turple_id[0]#тут и везде где ниже, присваиваются значения переменным
		i_graph = turple_id[0]#
		j_graph = turple_id[1]#
		t_ij_graph = turple_id[2]#
		G.add_edge(i_graph, j_graph, weight=t_ij_graph)
		"""^ тут в пустой объект графа добавляется два нода и вес"""
		i += 1
	n = list(G.nodes())
	g = 0
	while g < len(n):#здесь добавляются атрибуты к каждому ноду
		jj = n[g]
		G.nodes[jj]['Tri'] = 0
		#G.nodes[jj]['Trj'] = 0
		G.nodes[jj]['Tpi'] = 0
		#G.nodes[jj]['Tpj'] = 0
		G.nodes[jj]['Ri'] = 0
		#G.nodes[jj]['rji'] = 0
		g += 1
	return G
def calc_ir():#данная функция считает наступление раннего события i и присвает значения нодам
	G = add_edge_graph()
	v = 0
	list_nodes = sorted(list(G.nodes()))
	while v < len(list_nodes):
		g = list_nodes[v]
		if len(G.in_edges(g)) == 0:
			G.nodes[g]['Tri'] = 0
		elif len(G.in_edges(g)) == 1:
			tuple_id = tuple(list(G.in_edges(g))[0])
			G.nodes[g]['Tri'] = G.nodes[(tuple_id[0])]['Tri'] + G.edges[(tuple_id[0]),(tuple_id[1])]['weight']
		else:
			list_max = []
			k = 0 
			tuple_list = list(G.in_edges(g))
			while k < len(tuple_list):
				list_t = tuple(tuple_list[k])
				aa = G.nodes[(list_t[0])]['Tri'] + G.edges[(list_t[0]),(list_t[1])]['weight']
				list_max.append(aa)
				k += 1
			G.nodes[g]['Tri'] = max(list_max)
		v += 1
	return G
def calc_ip():#данная функция считает наступление позднего события i и присвает значения нодам
	G = calc_ir()
	v = 0
	list_nodes = sorted(list(G.nodes()), reverse=True)
	while v < len(list_nodes):
		g = list_nodes[v]
		if len(G.out_edges(g)) == 0:
			G.nodes[g]['Tpi'] = G.nodes[g]['Tri']

		elif len(G.out_edges(g)) == 1:
			tuple_id = tuple(list(G.out_edges(g))[0])
			G.nodes[g]['Tpi'] = G.nodes[(tuple_id[1])]['Tpi'] - G.edges[(tuple_id[0]),(tuple_id[1])]['weight']
		else:
			list_min = []
			k = 0
			tuple_list = list(G.out_edges(g))
			while k < len(tuple_list):
				list_t = tuple(tuple_list[k])
				aa = G.nodes[(list_t[1])]['Tpi'] - G.edges[(list_t[0]),(list_t[1])]['weight']
				list_min.append(aa)
				k += 1
			G.nodes[g]['Tpi'] = min(list_min)
		v += 1
	return G
def calc_ri():# данная функция считает резервы времени(и добавляет их к нодам графа), а так же список нодов критического пути и критический путь
	G = calc_ip()
	v = 0
	list_g = []
	list_nodes = sorted(list(G.nodes()))
	while v < len(list_nodes):
		g = list_nodes[v]
		a_r = G.nodes[g]['Tpi'] - G.nodes[g]['Tri']
		G.nodes[g]['Ri'] = a_r
		if a_r == 0:
			list_g.append(g)
		else:
			pass
		v += 1
	summ = []
	count = 0
	while count < (len(list_g)-1):
		g_c = list_g[count]
		a = G.edges[(list_g[count]),(list_g[count + 1])]['weight']
		summ.append(a)
		count += 1
	summ = sum(summ)
	return G,list_g,summ




