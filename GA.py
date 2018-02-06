from dfa import DFA
from data import PTA, Individual
from config import CONFIG
from disjoint_set import DisjointSet
from copy import copy
from merge import PTADisjointSet
import random
import os


def fitness(pta_nodes, p):
	return (fitness1, fitness2)

# https://math.stackexchange.com/questions/101125/how-to-compute-the-pareto-frontier-intuitively-speaking/101141
def getParetoIndexes(fitness_list):
	l = len(fitness_list)
	sorted_idx_0 = sorted(range(l), key=lambda t:fitness_list[t][0])

	pareto_frontier = []
	i = 0
	while True:
		pareto_frontier.append(sorted_idx_0[i])

		j = i+1
		while j < l:
			if fitness_list[sorted_idx_0[i]][1] > fitness_list[sorted_idx_0[j]][1]:
				break
			j = j+1
		if j >= l:
			break
		else:
			i = j
	
	return pareto_frontier

def crossover(p, q):
	plen = len(p.merge_basis)
	qlen = len(q.merge_basis)

	alpha = random.random()
	p_left_off = random.sample(range(plen), int(alpha*plen))
	q_left_off = random.sample(range(qlen), int(alpha*qlen))

	p_right_off = [i for i in range(plen) if i not in p_left_off]
	q_right_off = [i for i in range(qlen) if i not in q_left_off]

	new_basis1 = list(map(p.merge_basis.__getitem__, p_left_off)) + \
		list(map(q.merge_basis.__getitem__, q_right_off))
	new_basis2 = list(map(p.merge_basis.__getitem__, p_right_off)) + \
		list(map(q.merge_basis.__getitem__, q_left_off))

	return Individual(new_basis1), Individual(new_basis2)

def mutation(node_len, p):
	alpha = random.randint(0, 99)
	orig_basis = copy(p.merge_basis)
	additional_merge_set = []
	if alpha < CONFIG['GA_mutation_percentage']:
		for i in range(max(node_len//100, 10)):
			r = random.randint(0, 5)
			if r == 5:
				break
			elif r > 0:
				# add merge set
				additional_merge_set.append(random.sample(range(node_len), 2))
			else:
				# remove merge set
				if orig_basis:
					del orig_basis[random.randint(0, len(orig_basis)-1)]
	
	return Individual(orig_basis + additional_merge_set)

def GA_loop_pareto(fname, output_folder):
	pta = PTA.fromTXT(fname)

	if not os.path.exists(output_folder):
		os.makedirs(output_folder)

	# enumerate all nodes, by BFS
	pta_nodes = []
	bfsq = [pta]
	while bfsq:
		node = bfsq.pop(0)
		pta_nodes.append(node)

		for c in node.dict:
			bfsq.append(node.dict[c])

	# Initial population
	node_len = len(pta_nodes)
	population = []
	for i in range(CONFIG['GA_population_size']):
		basis = []
		for t in range(random.randint(int(node_len/3), int(node_len*2/3))):
			basis.append(random.sample(range(node_len), 2))
		population.append(Individual(basis))

	# generation
	for gen in range(CONFIG['GA_generation_cnt']):
		logfilename = os.path.join(output_folder, 'gen_%03d.log' % gen)
		with open(logfilename, 'wt') as logfile:
			# choosing elite
			# evaluate fitness
			# @TODO library. no duplicating evaluation
			fitnesses = []
			unions_list = []
			ds_list = []
			for individual in population:
				ds = PTADisjointSet(pta_nodes)
				i = 0
				while i < len(individual.merge_basis):
					s1, s2 = individual.merge_basis[i]

					# remove redundancy
					if ds.find(s1) == ds.find(s2):
						del individual.merge_basis[i]
						continue
					
					ds.union(s1, s2)
					i += 1

				unions = ds.get()
				fitness1 = len(unions)
				fitness2 = 0
				for union in unions:
					pos_cnt = 0
					neg_cnt = 0

					for c in union:
						b = pta_nodes[c].acceptance
						if b == None:
							continue
						if b == True:
							pos_cnt += 1
						else:
							neg_cnt += 1

					fitness2 += pos_cnt * neg_cnt # MY CHOICE
				fitnesses.append((fitness1, fitness2))
				unions_list.append(unions)
				ds_list.append(ds)
				logfile.write('fitness %d %d\n' % (fitness1, fitness2))
				print('fitness %d %d' % (fitness1, fitness2))

			# elites
			pareto_indexes = getParetoIndexes(fitnesses)
			elite_indexes = pareto_indexes if len(pareto_indexes) < CONFIG['GA_elite_size'] \
				else random.sample(pareto_indexes, CONFIG['GA_elite_size'])
			next_population = list(map(population.__getitem__, elite_indexes))
			logfile.write('PARETO count=%d\n' % len(elite_indexes))
			print('PARETO count=%d' % len(elite_indexes))
			for e in elite_indexes:
				logfile.write('id %d fitness %d %d\n' % (e, fitnesses[e][0], fitnesses[e][1]))
				logfile.write(' - merge_basis %s\n' % population[e].merge_basis)
				# logfile.write(' - union_set %s\n' % unions_list[e])
				# write fsm graphviz code
				vizcode = 'digraph fsm {\n\tnode [style=filled];\n'
				ds = ds_list[e]
				for union in unions_list[e]:
					rootstate = ds.find(union[0]) # representation of state
					for i, c in enumerate(ds.trans[rootstate.value]):
						if c != -1:
							vizcode += '\t%d -> %d [ label = "%s" ];\n' % (rootstate.value, c, i)

					
					# for state in positiveStates:
					# 	vizcode += '\t%d [ color="%s" ];\n' % (state, posColor)

					# for state in negativeStates:
					# 	vizcode += '\t%d [ color="%s" ];\n' % (state, negColor)

				vizcode += '}\n'
				logfile.write(vizcode)
				print('id %d fitness %d %d' % (e, fitnesses[e][0], fitnesses[e][1]))
				print(' - merge_basis %s' % population[e].merge_basis)
				# print(' - union_set %s' % unions_list[e])

			# crossover and mutation
			while len(next_population) < CONFIG['GA_population_size']:
				left, right = random.sample(population, 2)
				lo, ro = crossover(left, right)

				l = mutation(node_len, lo)
				r = mutation(node_len, ro)
				next_population += [l, r]

			population = next_population


def unittest_getParetoIndexes():
	t = getParetoIndexes([(1, 0), (4, 2), (-1, 3), (-5, 0)])
	print(t)

	indexes = []
	for i in range(5):
		indexes += [(-t, -i+t) for t in range(i)]
	print(getParetoIndexes(indexes))

if __name__ == "__main__":
	# unittest_getParetoIndexes()
	# GA_loop_pareto('../grid/1_training.txt', '1_training')
	GA_loop_pareto('test_training.txt', 'test_training')
