from Trie import Trie, TrieNode
import heapq
from collections import defaultdict, namedtuple

class FuzzyTrie(Trie):
	'''
	Implements fuzzy matching that allows for single/multiple errors (insertion, deletion, substitution)
	Default is 0 allowed errors, which behaves the same as the regular Trie.traverse, except it returns
	[TrieNode] instead of single instance of TrieNode
	'''
	def __init__(self):
		super().__init__()
		self.head = TrieNode()

	def match_prefix(self, prefix, allowed_errors: int=0) -> dict:
		# First must match first char
		node = self.head.traverse(prefix[0])
		if node is None:
			return dict()
		# first prefix matched, now fuzzy traverse remaining prefix
		traverse_results = node.fuzzy_traverse(prefix[1:], allowed_errors)

		# for each node in traverse results, generate resulting words and store
		# in dictionary with num_errors as key
		result = dict()
		seen = set()
		for num_errors, nodes in traverse_results.items():
			if num_errors not in result:
				result[num_errors] = set()
			for node in nodes:
				words = [node.prefix() + partial for partial in node.words()]
				words = set(word for word in words if word not in seen)
				result[num_errors] |= words
				seen |= words
		return result

		# must match at the first ch in prefix
		if not prefix:
			return self.words()
		if prefix[0] not in self.head.children:
			return dict()
		traverse_results = self.traverse(prefix, allowed_errors)
		result = self.head
		result = {}
		for (num_errors, prefix, node) in traverse_results:
			for suffix in node.words():
				word = prefix + suffix
				if word not in result:
					result[word] = num_errors
				else:
					result[word] = min(result[word], num_errors)
		return result

# simple unit test
if __name__ == '__main__':
	fuzzy_trie = FuzzyTrie()
	words = ['at', 'about', 'attack', 'art', 'fresh', 'church', 'allow', 'ace', 'audio', 'bow', 'but', 'belief', 'try', 'trie', 'turning']
	for word in words:
		fuzzy_trie.add_word(word)

	assert set(words) == set(fuzzy_trie.words())
	assert 'at' in fuzzy_trie
	assert 'belief' in fuzzy_trie
	assert 'cat' not in fuzzy_trie
	assert len(fuzzy_trie) == len(words)

	print(fuzzy_trie.match_prefix('aut', 1).items())



	# assert set(trie.match_prefix('a')) == set([s for s in words if s.startswith('a')])
	# assert set(trie.match_prefix('at')) == set([s for s in words if s.startswith('at')])
	# assert set(trie.match_prefix('tru')) == set([s for s in words if s.startswith('tru')])
	# assert set(trie.match_prefix('hello')) == set([s for s in words if s.startswith('hello')])
	# assert 'about' in trie
	# trie.remove_word('about')
	# assert 'about' not in trie
	# assert len(trie) == len(words) - 1
	# trie.remove_word('but')
	# assert len(trie) == len(words) - 2
	# assert set(trie.words()) == (set(words) - set(['about', 'but']))
	# trie.remove_words(['attack', 'belief', 'not'])
	# assert set(trie.words()) == (set(words) - set(['about', 'but', 'attack', 'belief']))
	# trie.add_words(['about', 'but', 'attack', 'belief'])
	# assert set(words) == set(trie.words())

