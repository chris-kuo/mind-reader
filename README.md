# Mind Reader
A word completion module. Suggest words from partial inputs. Implemented using trie and handles single and double (optional) input errors.

A simple demo is provided with the source code to demonstrate suggestions from incremental partial matching.

# Usage

First clone the mind-reader repository

```
git clone https://github.com/chris-kuo/mind-reader.git
```

Clone the MinderReader module and copy the files to the source file directory. For autocompletion of English words, the repo comes with the default word frequency data based on Mr. Norvig's word frequency table at [https://norvig.com/ngrams/].

_Example: use as autocompletor for English words_

```Python
from MindReader import MindReader

def main():
	suggestor = MindReader()
	suggestor.load_default_primary_freq()
	...
	partial_input = read_user_input()
	suggestions = suggestor.suggest(partial_input, allowed_errors=1, num_suggestions=8)
	...
```

_Example: use as autocompletor for Python IDE_

```Python
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
	...
	partial_input = read_user_input()
	suggestions = mind_reader.suggest(partial_input, allowed_errors=1, num_suggestions=6)
	...
	# after user completes input (such as insertion of space or new line)
	# use secondary for variable/user defined names
	mind_reader.increment_secondary(user_input)
	# for example, if user entered 'count' as variable name:
	# 	mind_reader.increment_secondary('count')
	...
```


# Sample demo output
Note that the '--' in suggested word list seprates results with no input errors, 1 error, and 2 errors.

```
Downloading http://norvig.com/ngrams/count_1w.txt
Processing frequency list file
First 10000 words loaded from http://norvig.com/ngrams/count_1w.txt

----- start demo -----
Check partial_input without errors:

Word 0: thumbnail
	t-> ['the', 'to', 'that', 'this', 'time', 'they']
	th-> ['the', 'that', 'this', 'they', 'their', 'there']
	thu-> ['thursday', 'thu', 'thus', 'thumbnail', 'thumbs', 'thumbnails']
	thum-> ['thumbnail', 'thumbs', 'thumbnails', 'thumbzilla', 'thumb', '--']
	thumb-> ['thumbnail', 'thumbs', 'thumbnails', 'thumbzilla', 'thumb', '--']
	thumbn-> ['thumbnail', 'thumbnails', '--', 'thumbs', 'thumbzilla', 'thumb']
	thumbna-> ['thumbnail', 'thumbnails', '--', '--', 'thumbs', 'thumbzilla']
	thumbnai-> ['thumbnail', 'thumbnails', '--', '--', 'thumbzilla']

Word 1: exciting
	e-> ['e', 'email', 'each', 'ebay', 'education', 'even']
	ex-> ['experience', 'example', 'exchange', 'executive', 'excellent', 'express']
	exc-> ['exchange', 'excellent', 'except', 'exclusive', 'exception', 'excess']
	exci-> ['exciting', 'excited', 'excitement', '--', 'exchange', 'excellent']
	excit-> ['exciting', 'excited', 'excitement', '--', 'exit', '--']
	exciti-> ['exciting', '--', 'excited', 'excitement', '--', 'edition']
	excitin-> ['exciting', '--', '--', 'existing', 'editing', 'excited']

Word 2: schemes
	s-> ['search', 'site', 'see', 'so', 's', 'services']
	sc-> ['school', 'science', 'schools', 'screen', 'score', 'schedule']
	sch-> ['school', 'schools', 'schedule', 'scheme', 'scheduled', 'scholarship']
	sche-> ['schedule', 'scheme', 'scheduled', 'schedules', 'schemes', 'scheduling']
	schem-> ['scheme', 'schemes', 'schema', '--', 'schedule', 'shemale']
	scheme-> ['scheme', 'schemes', '--', 'schema', '--', 'screen']

Word 3: flags
	f-> ['for', 'from', 'free', 'first', 'find', 'full']
	fl-> ['florida', 'flash', 'flowers', 'fl', 'floor', 'flat']
	fla-> ['flash', 'flat', 'flag', 'flashing', 'flags', 'flame']
	flag-> ['flag', 'flags', '--', 'flash', 'flat', 'flight']

Word 4: modem
	m-> ['more', 'my', 'may', 'me', 'most', 'music']
	mo-> ['more', 'most', 'money', 'movies', 'model', 'movie']
	mod-> ['model', 'models', 'mode', 'modern', 'modified', 'module']
	mode-> ['model', 'models', 'mode', 'modern', 'moderator', 'modem']

Word 5: rpm
	r-> ['re', 'rights', 'review', 'r', 'read', 'research']
	rp-> ['rpm', 'rpg', 'rp', '--', 're', 'rights']

Word 6: der
	d-> ['do', 'date', 'day', 'data', 'd', 'de']
	de-> ['de', 'development', 'details', 'design', 'department', 'description']

Word 7: depth
	d-> ['do', 'date', 'day', 'data', 'd', 'de']
	de-> ['de', 'development', 'details', 'design', 'department', 'description']
	dep-> ['department', 'depth', 'departments', 'depending', 'dependent', 'deposit']
	dept-> ['depth', 'dept', '--', 'details', 'department', 'death']

Check partial_input with one deletion:

Word 0: boss
	b-> ['by', 'be', 'but', 'business', 'been', 'back']
	bs-> ['bs', '--', 'by', 'be', 'but', 'business']
	bss-> ['--', 'business', 'best', 'based', 'basic', 'base']

Word 1: structure
	s-> ['search', 'site', 'see', 'so', 's', 'services']
	st-> ['state', 'store', 'states', 'students', 'still', 'stock']
	str-> ['street', 'structure', 'strong', 'strategy', 'string', 'stream']
	stru-> ['structure', 'structures', 'structural', 'struct', 'struggle', 'structured']
	struc-> ['structure', 'structures', 'structural', 'struct', 'structured', 'struck']
	strucu-> ['--', 'structure', 'structures', 'structural', 'struct', 'structured']
	strucur-> ['--', 'structure', 'structures', 'structural', 'structured', '--']
	strucure-> ['--', 'structure', 'structures', 'structured', '--', 'structural']

Word 2: attributes
	a-> ['and', 'a', 'are', 'at', 'as', 'all']
	at-> ['at', 'attention', 'attorney', 'attack', 'atom', 'atlanta']
	att-> ['attention', 'attorney', 'attack', 'attempt', 'attractions', 'attached']
	attr-> ['attractions', 'attribute', 'attributes', 'attraction', 'attractive', 'attract']
	attri-> ['attribute', 'attributes', '--', 'attractions', 'attitude', 'attraction']
	attrib-> ['attribute', 'attributes', '--', '--', 'attractions', 'attitude']
	attribt-> ['--', 'attribute', 'attributes', '--', 'attractions', 'attitude']
	attribte-> ['--', 'attribute', 'attributes', '--']
	attribtes-> ['--', 'attributes', '--', 'attribute']

Word 3: defines
	d-> ['do', 'date', 'day', 'data', 'd', 'de']
	df-> ['df', '--', 'do', 'date', 'day', 'data']
	dfi-> ['--', 'did', 'directory', 'digital', 'different', 'discussion']
	dfin-> ['--', 'doing', 'defined', 'definition', 'define', 'dining']
	dfine-> ['--', 'defined', 'define', 'defines', '--', 'directory']
	dfines-> ['--', 'defines', '--', 'defined', 'define', 'drives']

Word 4: itunes
	i-> ['in', 'is', 'i', 'it', 'if', 'information']
	iu-> ['--', 'in', 'is', 'i', 'it', 'if']
	iun-> ['--', 'in', 'information', 'into', 'info', 'international']
	iune-> ['--', 'inner', 'itunes', 'inexpensive', '--', 'in']
	iunes-> ['--', 'itunes', '--', 'insurance', 'institute', 'inside']

Word 5: ratios
	r-> ['re', 'rights', 'review', 'r', 'read', 'research']
	ra-> ['rating', 'rate', 'rates', 'range', 'radio', 'rather']
	rat-> ['rating', 'rate', 'rates', 'rather', 'ratings', 'rated']
	rato-> ['--', 'rating', 'rate', 'rates', 'rather', 'ratings']
	ratos-> ['--', 'rates', 'rats', 'ratios', '--', 'rating']

Word 6: oman
	o-> ['of', 'on', 'or', 'our', 'one', 'other']
	om-> ['omega', 'omaha', 'om', 'oman', 'omissions', '--']
	omn-> ['--', 'on', 'one', 'only', 'online', 'own']

Word 7: determination
	d-> ['do', 'date', 'day', 'data', 'd', 'de']
	de-> ['de', 'development', 'details', 'design', 'department', 'description']
	det-> ['details', 'detailed', 'detail', 'determine', 'determined', 'detroit']
	detr-> ['detroit', '--', 'details', 'degree', 'detailed', 'detail']
	detrm-> ['--', 'determine', 'determined', 'detroit', 'determination', 'determining']
	detrmi-> ['--', 'determine', 'determined', 'detroit', 'determination', 'determining']
	detrmin-> ['--', 'determine', 'determined', 'determination', 'determining', 'determines']
	detrmina-> ['--', 'determination', '--', 'determine', 'determined', 'determining']
	detrminat-> ['--', 'determination', '--']
	detrminati-> ['--', 'determination', '--']
	detrminatio-> ['--', 'determination', '--']
	detrmination-> ['--', 'determination', '--']

Check partial_input with one substitution:

Word 0: basic
	b-> ['by', 'be', 'but', 'business', 'been', 'back']
	ba-> ['back', 'based', 'baby', 'bad', 'bank', 'basic']
	bag-> ['bag', 'bags', 'baghdad', '--', 'back', 'based']
	bagi-> ['--', 'basic', 'basis', 'beginning', 'begin', 'bag']
	bagic-> ['--', 'basic', 'basically', 'basics', '--', 'back']

Word 1: throwing
	t-> ['the', 'to', 'that', 'this', 'time', 'they']
	tg-> ['tgp', '--', 'the', 'to', 'that', 'this']
	tgr-> ['--', 'through', 'travel', 'terms', 'three', 'training']
	tgro-> ['--', 'through', 'throughout', 'toronto', 'trouble', 'tropical']
	tgrow-> ['--', 'throw', 'throws', 'thrown', 'throwing', '--']
	tgrowi-> ['--', 'throwing', '--', 'tropical', 'throw', 'throws']
	tgrowin-> ['--', 'throwing', '--', 'thrown']
	tgrowing-> ['--', 'throwing', '--']

Word 2: situations
	s-> ['search', 'site', 'see', 'so', 's', 'services']
	si-> ['site', 'sign', 'size', 'since', 'sites', 'side']
	sit-> ['site', 'sites', 'situation', 'sitemap', 'sit', 'sitting']
	situ-> ['situation', 'situations', 'situated', '--', 'site', 'students']
	situa-> ['situation', 'situations', 'situated', '--', 'stuart', '--']
	situat-> ['situation', 'situations', 'situated', '--', '--', 'state']
	situati-> ['situation', 'situations', '--', 'situated', '--', 'statistics']
	situatio-> ['situation', 'situations', '--', '--', 'station', 'stations']
	situatios-> ['--', 'situation', 'situations', '--']
	situatioss-> ['--', 'situations', '--', 'situation']

Word 3: hopefully
	h-> ['have', 'home', 'has', 'he', 'his', 'here']
	ho-> ['home', 'how', 'hotel', 'hotels', 'house', 'hours']
	hop-> ['hope', 'hop', 'hopefully', 'hopes', 'hoping', 'hopkins']
	hope-> ['hope', 'hopefully', 'hopes', 'hoped', '--', 'home']
	hopef-> ['hopefully', '--', 'hope', 'hopes', 'hoped', '--']
	hopefu-> ['hopefully', '--', '--', 'hope', 'hopes', 'hoped']
	hopefub-> ['--', 'hopefully', '--']
	hopefubl-> ['--', 'hopefully', '--']
	hopefubly-> ['--', 'hopefully', '--']

Word 4: artist
	a-> ['and', 'a', 'are', 'at', 'as', 'all']
	ab-> ['about', 'above', 'able', 'abstract', 'ability', 'abuse']
	abt-> ['--', 'at', 'about', 'after', 'art', 'article']
	abti-> ['--', 'article', 'action', 'articles', 'activities', 'active']
	abtis-> ['--', 'artist', 'artists', 'artistic', '--', 'article']
	abtist-> ['--', 'artist', 'artists', 'artistic', '--', 'abstract']

Word 5: attraction
	a-> ['and', 'a', 'are', 'at', 'as', 'all']
	at-> ['at', 'attention', 'attorney', 'attack', 'atom', 'atlanta']
	att-> ['attention', 'attorney', 'attack', 'attempt', 'attractions', 'attached']
	attr-> ['attractions', 'attribute', 'attributes', 'attraction', 'attractive', 'attract']
	attra-> ['attractions', 'attraction', 'attractive', 'attract', '--', 'attack']
	attrac-> ['attractions', 'attraction', 'attractive', 'attract', '--', 'attack']
	attracw-> ['--', 'attractions', 'attraction', 'attractive', 'attract', '--']
	attracwi-> ['--', 'attractions', 'attraction', 'attractive', '--', 'attract']
	attracwio-> ['--', 'attractions', 'attraction', '--', 'attractive']
	attracwion-> ['--', 'attractions', 'attraction', '--']

Word 6: watson
	w-> ['with', 'was', 'we', 'will', 'what', 'which']
	wa-> ['was', 'way', 'want', 'water', 'war', 'washington']
	wat-> ['water', 'watch', 'watches', 'watching', 'waters', 'watched']
	watu-> ['--', 'water', 'watch', 'watches', 'watching', 'waters']
	watuo-> ['--', 'watson', '--', 'without', 'water', 'watch']
	watuon-> ['--', 'watson', '--', 'wagon']

Word 7: sticks
	s-> ['search', 'site', 'see', 'so', 's', 'services']
	sl-> ['slightly', 'sleep', 'slow', 'slide', 'slot', 'slowly']
	sli-> ['slightly', 'slide', 'slip', 'slideshow', 'slim', 'slight']
	slic-> ['--', 'slightly', 'stick', 'slide', 'sick', 'slip']
	slick-> ['--', 'stick', 'sick', 'stickers', 'sticker', 'sticks']
	slicks-> ['--', 'sticks', '--', 'stick', 'stocks', 'sick']

Check partial_input with two substitution:

Word 0: thriller
	t-> ['the', 'to', 'that', 'this', 'time', 'they']
	ta-> ['take', 'table', 'tax', 'talk', 'taken', 'taking']
	tar-> ['target', 'targets', 'targeted', 'tar', 'tariff', '--']
	taru-> ['--', 'true', 'trust', 'target', 'truth', 'truck']
	tarul-> ['--', 'truly', '--', 'table', 'talk', 'true']
	tarull-> ['--', '--', 'truly', 'tall', 'thriller']
	tarulle-> ['--', '--', 'thriller']
	taruller-> ['--', '--', 'thriller']

Word 1: projector
	p-> ['page', 'pm', 'price', 'people', 'products', 'product']
	pr-> ['price', 'products', 'product', 'privacy', 'program', 'prices']
	prf-> ['--', 'price', 'products', 'product', 'privacy', 'program']
	prfj-> ['--', 'project', 'projects', 'projection', 'projector', 'projectors']
	prfje-> ['--', 'project', 'projects', 'projection', 'projector', 'projectors']
	prfjec-> ['--', 'project', 'projects', 'projection', 'projector', 'projectors']
	prfjecs-> ['--', '--', 'project', 'projects', 'projection', 'projector']
	prfjecso-> ['--', '--', 'projector', 'projectors']
	prfjecsor-> ['--', '--', 'projector', 'projectors']

Word 2: officially
	o-> ['of', 'on', 'or', 'our', 'one', 'other']
	of-> ['of', 'off', 'office', 'offers', 'offer', 'official']
	off-> ['off', 'office', 'offers', 'offer', 'official', 'offered']
	offi-> ['office', 'official', 'officer', 'offices', 'officials', 'officers']
	offic-> ['office', 'official', 'officer', 'offices', 'officials', 'officers']
	offici-> ['official', 'officials', 'officially', '--', 'office', 'officer']
	officia-> ['official', 'officials', 'officially', '--', '--', 'office']
	officiai-> ['--', 'official', 'officials', 'officially', '--']
	officiail-> ['--', 'official', 'officials', 'officially', '--']
	officiailk-> ['--', '--', 'official', 'officials', 'officially']

Word 3: reproduced
	r-> ['re', 'rights', 'review', 'r', 'read', 'research']
	re-> ['re', 'review', 'read', 'research', 'reviews', 'real']
	rep-> ['report', 'reply', 'reports', 'republic', 'reported', 'repair']
	repr-> ['representative', 'represent', 'representatives', 'represents', 'representation', 'represented']
	repro-> ['reproduction', 'reproduced', 'reproductive', 'reproduce', '--', 'report']
	reprov-> ['--', 'reproduction', 'reproduced', 'reproductive', 'reproduce', '--']
	reprovu-> ['--', 'reproduction', 'reproduced', 'reproductive', 'reproduce', '--']
	reprovux-> ['--', '--', 'reproduction', 'reproduced', 'reproductive', 'reproduce']
	reprovuxe-> ['--', '--', 'reproduced', 'reproduce']
	reprovuxed-> ['--', '--', 'reproduced']

Word 4: attended
	a-> ['and', 'a', 'are', 'at', 'as', 'all']
	aj-> ['aj', '--', 'and', 'a', 'are', 'at']
	ajp-> ['--', 'application', 'april', 'applications', 'apr', 'apply']
	ajpe-> ['--', 'appear', 'appears', 'aspects', 'appeal', 'appendix']
	ajpen-> ['--', 'appendix', '--', 'agency', 'agent', 'agents']
	ajpend-> ['--', 'appendix', '--', 'amendment', 'agenda', 'attend']
	ajpende-> ['--', '--', 'appendix', 'amended', 'attended']
	ajpended-> ['--', '--', 'amended', 'attended']

Word 5: coaches
	c-> ['can', 'contact', 'c', 'click', 'city', 'copyright']
	cs-> ['cs', 'css', 'cst', '--', 'can', 'contact']
	csa-> ['--', 'can', 'car', 'case', 'care', 'change']
	csac-> ['--', 'coach', 'cache', 'crack', 'cached', 'coaching']
	csach-> ['--', 'coach', 'cache', 'cached', 'coaching', 'coaches']
	csachk-> ['--', '--', 'coach', 'cache', 'crack', 'cached']
	csachks-> ['--', '--', 'coaches']

Word 6: athens
	a-> ['and', 'a', 'are', 'at', 'as', 'all']
	au-> ['author', 'august', 'audio', 'australia', 'aug', 'auto']
	aul-> ['--', 'all', 'also', 'author', 'august', 'always']
	aule-> ['--', 'able', 'alert', 'alerts', 'allen', 'alexander']
	aulen-> ['--', 'allen', '--', 'able', 'along', 'agency']
	aulens-> ['--', '--', 'allen', 'athens']

Word 7: scotland
	s-> ['search', 'site', 'see', 'so', 's', 'services']
	sc-> ['school', 'science', 'schools', 'screen', 'score', 'schedule']
	sco-> ['score', 'scott', 'scotland', 'scope', 'scores', 'scottish']
	scot-> ['scott', 'scotland', 'scottish', 'scotia', '--', 'score']
	scotx-> ['--', 'scott', 'scotland', 'scottish', 'scotia', '--']
	scotxa-> ['--', 'scotland', 'scotia', '--', 'scott', 'scottish']
	scotxan-> ['--', 'scotland', '--', 'scotia']
	scotxant-> ['--', '--', 'scotland']

[Finished in 2.2s]
```
