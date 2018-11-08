from collections import deque, namedtuple, OrderedDict
import json
import urllib.request
import random
from functools import lru_cache


# Trie that supports suggestion from partial inputs
class TrieNode():
    def __init__(self, ch, prefix='', end_word=False):
        self.ch = ch
        self.prefix = prefix
        self.end_word = end_word
        self.children = dict()
        self.cache = None

    
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

    def clear_cache(self):
        self.cache = None

    def add(self, word):
        '''
        Append word to this trie node
        '''
        self.clear_cache()
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
        if not self.cache:
            q = [self]
            result = []
            while q:
                node = q.pop()
                if node.end_word:
                    result.append(node.word())
                q.extend(node.children.values())
            self.cache = result
        return self.cache

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
    
    def suggest(self, prefix):
        '''
        Return list of suggested words based on lower case partial input.
        ''' 
        prefix = prefix.lower()
        node = None
        i = 0
        allowed_errors = 2
        results = [set() for _ in range(allowed_errors + 1)]
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
                results[errors] |= set(node.words())
        temp = set()
        for result in results:
            result -= temp
            temp |= result
        return results

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


# Word suggester class using a Trie
class WordSuggestor():
    def __init__(self):
        self._trie = TrieNode('')
        self._word_weight = dict()
        self._cache = OrderedDict()

    def load_word_weight(self, word_weight_dict):
        '''
        Load the word weights from word weight dictionary.
        Higher preference is given to word with higher weight.
        '''
        for word, weight in word_weight_dict.items():
            self._word_weight[word] = weight
        self._cache.clear()

    def load_dictionary(self, dictionary):
        '''
        Load the word from dictionary. Dictionary is an interable of strings
        that represents each word
        '''
        for word in dictionary:
            self._trie.add(word)
        self._cache.clear()

    def lookup_word(self, word):
        '''
        Look up word in the word suggestor dictionary.
        Returns True if word is in dciationry, else False
        '''
        return self._trie.lookup(word)

    def total_number_of_words(self):
        '''
        Return the total number of words in the dictionary of
        word suggestor.
        '''
        return len(self._trie.words())

    def suggest(self, partial_input, num_suggestions=8):
        '''
        Suggest word based on partial_input string.
        '''
        if partial_input not in self._cache:
            results = self._trie.suggest(partial_input)
            results = list(map(list, results))
            for result in results:
                result.sort(key=lambda w: self._word_weight[w], reverse=True)
            i = 1
            suggestions = results[0]
            while len(suggestions) < num_suggestions and i < len(results):
                suggestions.extend(results[i])
                i += 1
            # trim result
            suggestions = suggestions[:num_suggestions]
            self._cache[partial_input] = suggestions
        return self._cache[partial_input]


if __name__=='__main__':
    # import Novrig's word frequency list as dictionary
    words_to_import = 10000
    url = 'http://norvig.com/ngrams/count_1w.txt'
    print('Downloading %s' % url)
    freq_map = dict()
    with urllib.request.urlopen(url) as f:
        print('Processing frequency list file')
        for line_number in range(words_to_import): # load top frequency words
            line = f.readline()
            word, freq = line.strip().split()
            word = word.decode('utf-8')
            freq = int(freq)
            freq_map[word] = freq
    print('First %d words loaded from %s' % (len(freq_map), url))

    # build dictionary from frequency map
    dictionary = list(freq_map)

    # Instantiate Word Suggestor
    suggestor = WordSuggestor()

    # load dictionary
    suggestor.load_dictionary(dictionary)

    # load word weights
    suggestor.load_word_weight(freq_map)

    # Try searching 
    assert suggestor.lookup_word('search') == True
    assert suggestor.lookup_word('collection') == True

    print('Check suggestor dicationary contains %d words...' % words_to_import, end='')
    assert suggestor.total_number_of_words() == words_to_import
    print('pass')

    # Demo Code
    random_seed = 20181105
    verbose = True
    num_words_per_testcase = 5

    random.seed(random_seed) # seed random number generator
    word_list = [word for word in dictionary if len(word) >= 3] # test words of at least 3 letters

    print()
    print('----- start demo -----')
    # perfect prefixes
    print('Check partial_input without errors:')
    print()
    for n, word in enumerate(random.sample(word_list, num_words_per_testcase)):
        print('Word %d: %s' % (n, word))
        for i in range(1, len(word)):
            partial = word[:i]
            if verbose:
                print('\t%s->' % partial, suggestor.suggest(partial))
        print()

    # skip one letter
    print('Check partial_input with one deletion:')
    print()
    for n, word in enumerate(random.sample(word_list, num_words_per_testcase)):
        print('Word %d: %s' % (n, word))
        i = random.randint(1, max(len(word) - 2, 1))
        temp = word[:i] + word[i+1:]
        for i in range(1, len(temp) + 1):
            partial = temp[:i]
            if verbose:
                print('\t%s->' % partial, suggestor.suggest(partial))
        print()

    # mistype one letter
    print('Check partial_input with one substitution:')
    print()
    for n, word in enumerate(random.sample(word_list, num_words_per_testcase)):
        print('Word %d: %s' % (n, word))
        i = random.randint(1, max(len(word) - 2, 1))
        temp = list(word)
        temp[i] = random.choice([c for c in 'abcdefghijklmnopqrstuvwxyz' if c != word[i]])
        temp = ''.join(temp)
        for i in range(1, len(temp) + 1):
            partial = temp[:i]
            if verbose:
                print('\t%s->' % partial, suggestor.suggest(partial))
        print()

    # mistype two letters
    print('Check partial_input with two substitution:')
    print()
    for n, word in enumerate(random.sample([word for word in dictionary if len(word) > 5]
                , num_words_per_testcase)):
        print('Word %d: %s' % (n, word))
        i, j = random.sample(range(1, len(word)), 2)
        temp = list(word)
        temp[i] = random.choice([c for c in 'abcdefghijklmnopqrstuvwxyz' if c != word[i]])
        temp[j] = random.choice([c for c in 'abcdefghijklmnopqrstuvwxyz' if c != word[j]])
        temp = ''.join(temp)
        for i in range(1, len(temp) + 1):
            partial = temp[:i]
            if verbose:
                print('\t%s->' % partial, suggestor.suggest(partial))
        print()