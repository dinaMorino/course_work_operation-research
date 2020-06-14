import networkx as nx
import matplotlib.pyplot as plt
from calculation import*

def print_graph():
	a, b, c = calc_ri()
	G = a
	nx.draw(G, with_labels=True, font_weight='bold')
	plt.show()