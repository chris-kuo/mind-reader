from FuzzyTrie import FuzzyTrie
import math

class MindReader():
	def __init__(self):
		self.primary_fmap = dict() # primary frequency map
		self.secondary_fmap = dict() # secondary frequency map
		self.primary_total_count = 0
		self.secondary_total_count = 0
		self.primary_trie = FuzzyTrie()
		self.secondary_trie = FuzzyTrie()
		self.p_single_error = 0.1
		self.default_primary_file = 'count_1w.txt'


	########## Load Word Frequency ##########
	def load_primary_freq(self, f, max_num_words=float('inf')) -> int:
		# input format
		# on each line, <word> <count>
		# Returns number of word-count pair loaded
		num_words = 0
		for line in f:
			word, count = line.split()
			# word = word.decode('utf-8')
			count = int(count)
			if word in self.primary_fmap:
				print(f'WARNING: duplicate word `{word}` Primary Freq Map. Using latest count of f{count}')
				self.primary_total_count -= self.primary_fmap[word]
				num_words -= 1
			self.primary_fmap[word] = count
			self.primary_total_count += count
			self.primary_trie.add_word(word)
			num_words += 1
			if num_words > max_num_words:
				break
		return num_words

	def load_default_primary_freq(self):
		try:
			with open(self.default_primary_file) as infile:
				# load top 5000 words instead of entire word list
				self.primary_num_words_loaded = self.mind_reader.load_primary_freq(infile)
		except IOError as err:
		    print("I/O error: {0}".format(err))


	def load_secondary_freq(self, infile) -> int:
		# input format
		# on each line, <word> <count>
		# Returns number of word-count pair loaded
		line = f.readline()
		num_words = 0
		while line:
			word, count = line.strip().split()
			word = word.decode('utf-8')
			count = int(freq)
			if word in self.secondary_fmap:
				print(f'WARNING: duplicate word `{word}` in Secondary Freq Map. Using latest count of f{count}')
				self.secondary_total_count -= self.secondary_fmap[word]
				num_words -= 1
			self.secondary_fmap[word] = count
			self.secondary_total_count += count
			self.secondary_trie.add_word(word)
			num_words += 1
		return num_words


	########## Update Word Frequency Maps ##########
	def increment_primary(self, word: str):
		if word not in self.primary_fmap:
			self.primary_fmap[word] = 1
			self.primary_trie.add_word(word)
		else:
			self.primary_fmap[word] += 1
		self.primary_total_count += 1

	def increment_secondary(self, word: str):
		if word not in self.secondary_fmap:
			self.secondary_fmap[word] = 1
			self.secondary_trie.add_word(word)
		else:
			self.secondary_fmap[word] += 1
		self.secondary_total_count += 1

	def clear_primary_fmap(self):
		self.primary_fmap.clear()
		self.primary_trie.clear()

	def clear_secondary_fmap(self):
		self.secondary_fmap.clear()
		self.secondary_trie.clear()

	########## Auto Completion ##########
	def suggest(self, partial_input: str, allowed_errors: int=0, num_suggestions: int=6) -> [str]:
		# Given a partial input and acceptable number of input errors, return list
		# of ranked suggested words.
		
		# get list of candidates words grouped in number of errors in matching partial input
		candidates = self.primary_trie.match_prefix(partial_input, allowed_errors)
		for num_errors, words in self.secondary_trie.match_prefix(partial_input, allowed_errors).items():
			if num_errors not in candidates:
				candidates[num_errors] = words
			else:
				candidates[num_errors] |= words
		# score the candidates
		candidates = self.score(candidates)
		return candidates[:num_suggestions]

	def score(self, candidates: dict) -> [str]:
		# step 1: convert num_errors to probability
		weights = dict()
		for num_errors, words in candidates.items():
			for word in words:
				if word in weights:
					weights[word] = max(weights[word], math.pow(self.p_single_error, num_errors))
				else:
					weights[word] = math.pow(self.p_single_error, num_errors)

		# step 2: calculate a priori based on primary word freq table
		for word in weights:
			weights[word] *= self.primary_fmap[word] / self.primary_total_count if word in self.primary_fmap else \
					(len(self.primary_fmap) / self.primary_total_count if self.primary_total_count else 0.1)

		# step 3: calculate a priori based on secondary word freq table
		for word in weights:
			weights[word] *= self.secondary_fmap[word] / self.secondary_total_count if word in self.secondary_fmap else \
					(len(self.secondary_fmap) / self.secondary_total_count if self.secondary_total_count else 0.1)
		return sorted(list(weights), key=lambda s: weights[s], reverse=True)
		
if __name__ == '__main__':
	# Run unit test
	import unittest

	class MindReaderTest(unittest.TestCase):
		def setUp(self):
			# use the word frequency list from Mr. Norvig's Natural Language Corpus Data: Beautiful Data
			self.mind_reader = MindReader()

			default_primary_file = 'count_1w.txt'
			with open(default_primary_file) as infile:
				# load top 5000 words instead of entire word list
				self.primary_num_words_loaded = self.mind_reader.load_primary_freq(infile, 5000)
			self.assertEqual(self.primary_num_words_loaded, len(self.mind_reader.primary_trie))

		def test_increment_primary(self):
			# test existing word
			mind_reader = self.mind_reader
			word = 'the'
			previous = mind_reader.primary_fmap[word]
			mind_reader.increment_primary(word)
			self.assertEqual(mind_reader.primary_fmap[word], previous + 1)
			# test non-existing word
			word = 'not_exist'
			mind_reader.increment_primary(word)
			self.assertEqual(mind_reader.primary_fmap[word], 1)

		def test_playground(self):
			word = 'associate'
			self.mind_reader.increment_secondary('async')
			for i in range(1, len(word)):
				print(word[:i], '->', self.mind_reader.suggest(word[:i], 1))

	unittest.main()
