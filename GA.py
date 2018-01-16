from dfa import DFA
from data import Data
from config import CONFIG
from random import choice

def fitness(p):
	return -1

def crossover(p, q):
	return p, q

def mutation(p):
	return p


def main():
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
	main()
