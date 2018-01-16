# NFA 
# NFA to DFA

EPSILON = None

# fails for matching character which is not registered with transition
class NFA:
	# 0 : initial state
	def __init__(self, state_cnt=5, finals=[4]):
		self.state_cnt = state_cnt
		self.finals = set(finals)

		self.transitions = []

	# i to finals
	# return None for fail
	def addTransition(self, i, fs, char=EPSILON):
		self.transitions.append((i, set(fs), char))

	# checked: already checked states on searching
	# BFS strategy
	def getEpsilons(self, states):
		results = set()
		gonna_check = states

		while gonna_check:
			new_gonna_check = set()

			for i, fs, char in self.transitions:
				if i in gonna_check and char == EPSILON:
					new_gonna_check |= fs - results

			results |= gonna_check
			gonna_check = new_gonna_check

		return results

	def verifyString(self, string):
		print("Testing string:%s" % string)

		states = set()
		states.add(0)
		for c in string:
			# epsilon expansion
			states = self.getEpsilons(states)

			new_states = set()
			for i, fs, char in self.transitions:
				if i in states and char == c:
					new_states |= fs

			states = new_states
			if len(states) == 0:
				break


			states = new_states

		if states & self.finals: # intersection of sets
			print("ACCEPTED")
		else:
			print("NOT ACCEPTED")

# fails for matching character which is not registered with transition
class DFA:
	def __init__(self, state_cnt=5, finals=[4]):
		self.state_cnt = state_cnt
		self.finals = finals

		self.transitions = []

	def addTransition(self, i, f, char):
		self.transitions.append((i, f, char))

	def verifyString(self, string):
		print("Testing string:%s" % string)

		state = 0
		accepted = True
		for c in string:
			met = False
			for i, f, char in self.transitions:
				if i == state and char == c:
					state = f
					met = True
					break
			if not met:
				accepted = False
				break

		if accepted and state in self.finals:
			print("ACCEPTED")
		else:
			print("NOT ACCEPTED")

def NFA2DFA(nfa):
	assert isinstance(nfa, NFA)

	dfa_states = [] # list of set of states
	dfa_transitions = []

	inits = nfa.getEpsilons(set([0]))
	dfa_states.append(inits)
	gonna_check_nums = [0] # number(index) of dfa_states

	# BFS strategy
	while gonna_check_nums:
		cur_state_num = gonna_check_nums.pop(0) 
		cur_state = dfa_states[cur_state_num]
		cur_transitions = dict()

		# search transitions
		for i, fs, char in nfa.transitions:
			if i in cur_state and char != EPSILON:
				try:
					cur_transitions[char] |= fs
				except:
					cur_transitions[char] = fs

		# add transitions
		for char, state in cur_transitions.items():
			state = nfa.getEpsilons(state)
			if cur_transitions[char] in dfa_states:
				idx = dfa_states.index(cur_transitions[char])
			else:
				idx = len(dfa_states)
				dfa_states.append(cur_transitions[char])
				gonna_check_nums.append(idx)
			dfa_transitions.append((cur_state_num, idx, char))

	# finals
	dfa_finals = []
	for i, state in enumerate(dfa_states):
		if state.intersection(nfa.finals):
			dfa_finals.append(i)

	dfa = DFA(finals = dfa_finals)
	for i, f, c in dfa_transitions:
		dfa.addTransition(i, f, c)
	print(dfa_states)
	print(dfa_transitions)
	print(dfa_finals)
	return dfa


def main():
	def test1():
		# (B+|AB+)
		# init  0
		# i     1
		# iB    2
		# j     3
		# jA    4
		# jAB   5
		nfa = NFA(6, [2, 5])
		nfa.addTransition(0, [1, 3])

		nfa.addTransition(1, [2], 'B')
		nfa.addTransition(2, [2], 'B')
		nfa.addTransition(3, [4], 'A')
		nfa.addTransition(4, [5], 'B')
		nfa.addTransition(5, [5], 'B')
		dfa = NFA2DFA(nfa)

		nfa.verifyString('AB')
		dfa.verifyString('AB')
		nfa.verifyString('ABBB')
		dfa.verifyString('ABBB')
		nfa.verifyString('BAB')
		dfa.verifyString('BAB')
		nfa.verifyString('ABA')
		dfa.verifyString('ABA')
		nfa.verifyString('')
		dfa.verifyString('')
		nfa.verifyString('BB')
		dfa.verifyString('BB')
		nfa.verifyString('B')
		dfa.verifyString('B')
		nfa.verifyString('C')
		dfa.verifyString('C')
		nfa.verifyString('BAB')
		dfa.verifyString('BAB')

	def randomTest():
		pass

	test1()





if __name__ == "__main__":
	main()