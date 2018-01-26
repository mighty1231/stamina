from dfa import DFA
from data import PTA
from config import CONFIG
from random import choice
import os


def fitness(p):
	return -1

def crossover(p, q):
	return p, q

def mutation(p):
	return p

def merge(pta, prev, new_pair):
	# mergedSet = [(1, 2, 3), (4, 5)]
	# removal = [6, 7, 8]
	return mergedSet, removal


def GA_loop_pareto(fname, output_folder):
	pta = PTA.fromTXT(fname)

	if not os.path.exists(output_folder):
		os.makedirs(output_folder)

	# enumerate all nodes, by BFS
	nodes = []
	bfsq = [pta]
	while bfsq:
		node = bfsq.pop(0)
		nodes.append(node)

		for c in node.dict:
			bfsq.append(node.dict[c])





	population = [DFA() for i in range(CONFIG['GA_population_size'])]

	for gen in range(CONFIG['GA_generation_cnt']):
		# choosing elite
		sorted_population = sorted(population, key=fitness)
		next_population = sorted_population[:CONFIG['GA_elite_size']] # or reverse? CONFIG[]:

		while len(next_population) != CONFIG['GA_population_size']:
			left, right = choice(population), choice(population)
			lo, ro = crossover(left, right)

			l = mutation(lo)
			r = mutation(ro)
			next_population += [l, r]

		population = next_population



if __name__ == "__main__":
	GA_loop_pareto('../grid/1_training.txt', '1_training')
