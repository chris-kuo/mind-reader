from MindReader import MindReader
import keyword

if __name__ == '__main__':
	mind_reader = MindReader()
	# load built in function names
	with open('python_builtin_functions.txt') as f:
		for line in f:
			word = line.split()[0]
			mind_reader.increment_primary(word)
	# load keyword
	for word in keyword.kwlist:
		mind_reader.increment_primary(word)
	# use secondary for variable names
	mind_reader.increment_secondary('num_errors')
	word = 'num_errors'
	# word = 'enumeration'
	for i in range(1, len(word)):
		partial_input = word[:i]
		print(f'{partial_input} -> {mind_reader.suggest(partial_input, 1)}')