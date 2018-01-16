from data import Data
import numpy as np

#
# Deterministic finite automaton from wikipedia.org
#
# Q     : a finite set of states
# Sigma : a finite set of input symbols called the alphabet
# Delta : a transition function (Delta: Q*Sigma -> Q)
# Q_0   : an initial state
# F     : a set of accept states
#

class DFA:
	# Q     : integer 0 ~ self.state_size-1
	# Sigma : integer 0 ~ self.alpha_size-1
	# Delta : list of tuples (qi, sigma, qf) : self.transitions
	# Q_0   : integer 0
	# F     : ???
	def __init__(self, alpha_size):
		# some random initialization

		# always start at init
		self.state_size = 5
		self.alpha_size = alpha_size
		self.transitions = [(0, 0, 1), (0, 1, 4)]
		self.report = None

	def getReport(self, data):
		if self.report:
			return self.report
		report = dict()
		
		# assert isinstance(data, Data)

		# evaluate all of positive and negative strings
		posneg_stat = np.zeros((self.state_size, 2), dtype = np.int)
		for string in data.pos:
			state = self.getFinalState(string)
			posneg_stat[state, 1] += 1
		for string in data.pos:
			state = self.getFinalState(string)
			posneg_stat[state, 0] += 1

		report['posneg_stat'] = posneg_stat
		self.report = report
		return report

	def getNextState(self, i, symbol):
		for qi,sigma,qf in self.transitions:
			if qi == i and sigma == symbol:
				return qf
		return i

	def getFinalState(self, string):
		state = 0
		for s in string:
			state = self.getNextState(state, s)
		return state