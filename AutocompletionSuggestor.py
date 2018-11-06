from collections import deque
from collections import namedtuple
import json
import urllib.request
import random

# import Novrig's word frequency list as dictionary
url = 'http://norvig.com/ngrams/count_1w.txt'
print('Downloading %s' % url)
freq_map = dict()
with urllib.request.urlopen(url) as f:
	print('Processing frequency list file')
	for line_number in range(8000): # load top frequency words
		line = f.readline()
		word, freq = line.strip().split()
		word = word.decode('utf-8')
		freq = int(freq)
		freq_map[word] = freq
print('First %d words loaded from %s' % (len(freq_map), url))

# build dictionary from frequency map
dictionary = list(freq_map)

# Trie that supports suggestion from partial inputs
class TrieNode():
	def __init__(self, ch, prefix='', end_word=False):
		self.ch = ch
		self.prefix = prefix
		self.end_word = end_word
		self.children = dict()

	
	def word(self):
		'''
		Return the word if this trie node is end of word, else returns None
		'''
		if self.end_word:
			return self.prefix + self.ch
		else:
			None
	def __str__(self):
		return "TrieNode('%s, %s')" % (self.prefix, self.ch)

	def add(self, word):
		'''
		Append word to this trie node
		'''
		node = self
		prefix = self.prefix + self.ch
		i = 0
		while i < len(word):
			ch = word[i]
			if ch not in node.children:
				node.children[ch] = TrieNode(ch, prefix)
			node = node.children[ch]
			i += 1
			prefix += ch
		node.end_word = True

	def words(self):
		'''
		Enumerate all words starting from this trie node
		'''
		q = [self]
		result = []
		while q:
			node = q.pop()
			if node.end_word:
				result.append(node.word())
			q.extend(node.children.values())
		return result

	def print(self):
		'''
		Print trie
		'''
		offset = len(self.prefix) + 1
		bullet = '+' if offset // 2 else ''
		if bullet:
			print(bullet + '-' * offset + self.ch)
		else:
			print(self.ch)
		for child in self.children.values():
			child.print()
	
	def suggest(self, prefix, num_suggestions=5):
		'''
		Return list of suggested words based on lower case partial input.
		''' 
		prefix = prefix.lower()
		node = None
		i = 0
		allowed_errors = 1
		result = [set() for _ in range(allowed_errors + 1)]
		NodeAndPrefix = namedtuple('NodeAndPrefix', ('node', 'prefix', 'errors'))
		q = deque([NodeAndPrefix(self, prefix, 0)])
		is_first_letter = True # only allow input errors after first letter
		while q:
			node, prefix, errors = q.popleft()
			if errors > allowed_errors:
				continue
			if prefix:
				ch = prefix[0]
				if ch in node.children:
					# correct input
					q.append(NodeAndPrefix(node.children[ch], prefix[1:], errors))
				if not is_first_letter:
					# extraneous input
					q.append(NodeAndPrefix(node, prefix[1:], errors + 1))
					# wrong input and missed input
					for child in node.children.values():
						q.append(NodeAndPrefix(child, prefix[1:], errors + 1))
						q.append(NodeAndPrefix(child, prefix, errors + 1))
					# swapped input
					if len(prefix) > 1:
						q.append(NodeAndPrefix(node, prefix[1] + prefix[0] + prefix[2:], errors + 1))
				is_first_letter = False
			else:
				result[errors] |= set(node.words())
		temp = sorted(list(result[0]), key=lambda w: freq_map[w], reverse=True)
		if len(temp) <= num_suggestions: # include suggestions from errorous inputs if necessary
			# '--' marks results from assuming no input errors to assuming 1 input error
			temp  += ['--'] + sorted(list(result[1] - result[0]), key=lambda w: freq_map[w], reverse=True)
		return temp[:num_suggestions + 1]

	def lookup(self, word):
		node = self
		i = 0
		while i < len(word):
			if word[i] in node.children:
				node = node.children[word[i]]
				i += 1
			else:
				return False
		return True if node.end_word else False

# create trie
trie = TrieNode('')
# add words
for word in dictionary:
	trie.add(word)

assert trie.lookup('search') == True
assert trie.lookup('collection') == True

print()
print('----- start demo -----')
num_tries = 8
# perfect prefixes
print('Check partial_input without errors:')
print()
for n, word in enumerate(random.sample(dictionary, num_tries)):
	print('Word %d: %s' % (n, word))
	for i in range(1, len(word)):
		partial = word[:i]
		print('\t%s->' % partial, trie.suggest(partial))
	print()

# skip one letter
print('Check partial_input with one deletion:')
print()
for n, word in enumerate(random.sample(dictionary, num_tries)):
	print('Word %d: %s' % (n, word))
	i = random.randint(1, max(len(word) - 2, 1))
	temp = word[:i] + word[i+1:]
	for i in range(1, len(temp) + 1):
		partial = temp[:i]
		print('\t%s->' % partial, trie.suggest(partial))
	print()

