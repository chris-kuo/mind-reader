from collections import namedtuple, defaultdict
import heapq
from functools import lru_cache


class TrieNode():
	def __init__(self, ch: str='', end_word: bool=False, parent=None):
		self.ch = ch
		self.end_word = end_word
		self.children = dict()
		self.parent = parent

	def __str__(self) -> str:
		return f"TrieNode('{self.ch}')"

	def __lt__(self, other) -> bool:
		return self.ch < other.ch

	def append_ch(self, ch: str, end_word: bool=False):
		if ch not in self.children:
			self.children[ch] = TrieNode(ch, end_word)
		else:
			self.children[ch].end_word = self.children[ch].end_word or end_word

	def gather(self) -> [str]:
		# Return all words in current and children TrieNodes
		words = [self.ch] if self.end_word else []
		# has children nodes
		words += [(self.ch + word) for child in self.children.values() for word in child.gather()]
		return words

	def prefix(self) -> str:
		# Return prefix to current TrieNode.
		pre = ''
		node = self
		while node.parent:
			pre = node.parent.ch + pre
			node = node.parent
		return pre

	def words(self) -> [str]:
		# Return all words in current and children TrieNodes
		words = [self.ch] if self.end_word else []
		# has children nodes
		words += [(self.ch + word) for child in self.children.values() for word in child.gather()]
		return words		

	def traverse(self, suffix):
		# traverse from current node through string s and return the node corresponding
		# to s[-1]. Return None if suffix doesn't result in valid path
		node = self
		for ch in suffix:
			if ch not in node.children:
				return None
			node = node.children[ch]
		return node

	def fuzzy_traverse(self, suffix: str, allowed_errors: int=0) -> dict():
		# Use a queue to hold nodes to be traversed
		# Each Queue Item need to hold the current number of errors,
		# the path it has taken, and the remaining suffix to be matched
		QItem = namedtuple('QItem', ['num_errors', 'node', 'i'])
		result = defaultdict(set) # stores the result based on number of errors
		# (node, current suffix index, num_errors) use a heap queue to 
		# process path with lower error count first.
		# TODO: break from searching when more than sufficient result are found
		queue = [QItem(num_errors=0, node=self, i=0)] 
		while queue:
			item = heapq.heappop(queue)
			num_errors, node, i = item
			# base case - too many errors
			if num_errors > allowed_errors:
				continue
			# base case - matched all suffix
			if i == len(suffix):
				# add current node to result. Group results by number of errors
				result[num_errors].add(node)
				continue
			# process current node
			for ch, child in node.children.items():
				if ch == suffix[i]: # found a matching child node
					heapq.heappush(queue, QItem(num_errors=num_errors, node=child, i=i+1))
				else: # no matching child node, try substituting (ie match any character)
					heapq.heappush(queue, QItem(num_errors=num_errors+1, node=child, i=i+1))
				# handle missing char in partial input -> match any char in trie and continue matching suffix @ i
				heapq.heappush(queue, QItem(num_errors=num_errors+1, node=child, i=i))
			# handle extra char in partial input -> skip char in suffix and try matching from current node
			heapq.heappush(queue, QItem(num_errors=num_errors+1, node=node, i=i+1))
		return result

class Trie():
	def __init__(self):
		self.head = TrieNode()
		self.num_words = 0

	def __len__(self) -> int:
		return self.num_words

	def __contains__(self, word: str) -> bool:
		node = self.head
		for ch in word:
			if ch not in node.children:
				return False
			node = node.children[ch]
		# make sure the ending node is end of word
		return node.end_word

	def add_word(self, word: str): # add word to trie
		node = self.head
		for ch in word:
			if ch not in node.children:
				node.children[ch] = TrieNode(ch, parent=node)
			node = node.children[ch]
		# mark last node as end of word
		node.end_word = True
		self.num_words += 1

	
	def add_words(self, words: [str]):
		for word in words:
			self.add_word(word)
	

	def remove_word(self, word: str) -> bool:
		'''
		Remove word from trie.
		Returns True if word was in Trie, else returns False
		'''
		node = self.head
		stack = []
		# propagate to end, and recursively remove unnecessary node
		for ch in word:
			if ch not in node.children:
				return False
			stack.append(node) # used to track traversal path
			node = node.children[ch]
		node.end_word = False
		stack.append(node)
		# remove unnecessary nodes
		while stack:
			node = stack.pop()
			if node is self.head: # removed all nodes
				break
			if len(node.parent.children) == 1:
				del node.parent.children[node.ch]
				node.parent = None
		self.num_words -= 1

	def remove_words(self, words: [str]):
		for word in words:
			self.remove_word(word)


	def words(self) -> [str]:
		# Return all words in trie
		return self.head.gather()

	def match_prefix(self, prefix) -> [str]:
		node = self.head.traverse(prefix)
		result = [] if not node else [prefix[:-1] + word for word in self.head.traverse(prefix).gather()]
		return result


	def clear(self):
		self.head = TrieNode()
		self.num_words = 0
		

# simple unit test
if __name__ == '__main__':
	trie = Trie()
	words = ['at', 'about', 'attack', 'art', 'bow', 'but', 'belief', 'try', 'trie', 'turning']
	for word in words:
		trie.add_word(word)

	assert set(words) == set(trie.words())
	assert 'at' in trie
	assert 'belief' in trie
	assert 'cat' not in trie
	assert len(trie) == len(words)
	assert set(trie.match_prefix('a')) == set([s for s in words if s.startswith('a')])
	assert set(trie.match_prefix('at')) == set([s for s in words if s.startswith('at')])
	assert set(trie.match_prefix('tru')) == set([s for s in words if s.startswith('tru')])
	assert set(trie.match_prefix('hello')) == set([s for s in words if s.startswith('hello')])
	assert 'about' in trie
	trie.remove_word('about')
	assert 'about' not in trie
	assert len(trie) == len(words) - 1
	trie.remove_word('but')
	assert len(trie) == len(words) - 2
	assert set(trie.words()) == (set(words) - set(['about', 'but']))
	trie.remove_words(['attack', 'belief', 'not'])
	assert set(trie.words()) == (set(words) - set(['about', 'but', 'attack', 'belief']))
	trie.add_words(['about', 'but', 'attack', 'belief'])
	assert set(words) == set(trie.words())

	word = 'attack'
	for i, c in enumerate(word):
		print(word[:i], '->', trie.match_prefix(word[:i]))

	print('\nTest fuzzy traverse')
	for i, c in enumerate(word):
		traversal_results = trie.head.fuzzy_traverse(words[:i], 1)
		print([str(node) for nodes in traversal_results.values() for node in nodes])
		results = dict()
		# for num_errors, nodes in traversal_results.items():
		# 	results[num_errors] = [node.prefix() + node.ch for node in nodes]
		# print(word[:i], '->', results)
