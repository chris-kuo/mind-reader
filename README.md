# Autocompleter
Word completion from partial input implemented using trie and handles single input errors.

The same class can also be used as spell check by supplying complete word input rather than partial input, however the suggestion criteria would need to be updated to include length matching as one of the weights.

A simple demo is provided with the source code to demonstrate suggestions from incremental partial matching.

# Sample demo output
Note that the '--' in suggested word list seprates results with no input errors, 1 error, and 2 errors.

```
Downloading http://norvig.com/ngrams/count_1w.txt
Processing frequency list file
First 5000 words loaded from http://norvig.com/ngrams/count_1w.txt

----- start demo -----
Check partial_input without errors:

Word 0: november
	n-> ['not', 'new', 'no', 'news', 'now', 'name']
	no-> ['not', 'no', 'now', 'north', 'non', 'note']
	nov-> ['november', 'nov', 'novel', 'nova', '--', 'not']
	nove-> ['november', 'novel', '--', 'note', 'never', 'nov']
	novem-> ['november', '--', 'novel', '--', 'note', 'never']
	novemb-> ['november', '--', '--', 'notebook', 'novel', 'notebooks']
	novembe-> ['november', '--', '--']

Word 1: produce
	p-> ['page', 'pm', 'price', 'people', 'products', 'product']
	pr-> ['price', 'products', 'product', 'privacy', 'program', 'prices']
	pro-> ['products', 'product', 'program', 'project', 'profile', 'property']
	prod-> ['products', 'product', 'production', 'produced', 'produce', 'productions']
	produ-> ['products', 'product', 'production', 'produced', 'produce', 'productions']
	produc-> ['products', 'product', 'production', 'produced', 'produce', 'productions']

Word 2: lot
	l-> ['like', 'list', 'last', 'links', 'life', 'line']
	lo-> ['local', 'long', 'location', 'love', 'low', 'look']

Word 3: neither
	n-> ['not', 'new', 'no', 'news', 'now', 'name']
	ne-> ['new', 'news', 'next', 'need', 'network', 'never']
	nei-> ['neighborhood', 'neither', '--', 'new', 'news', 'next']
	neit-> ['neither', '--', 'next', 'network', 'net', 'networks']
	neith-> ['neither', '--', 'netherlands', 'neighborhood', '--', 'next']
	neithe-> ['neither', '--', 'netherlands', '--', 'northern', 'neighborhood']

Word 4: employees
	e-> ['e', 'email', 'each', 'ebay', 'education', 'even']
	em-> ['email', 'employment', 'employees', 'employee', 'emergency', 'em']
	emp-> ['employment', 'employees', 'employee', 'empty', 'employer', 'empire']
	empl-> ['employment', 'employees', 'employee', 'employer', 'employed', 'employers']
	emplo-> ['employment', 'employees', 'employee', 'employer', 'employed', 'employers']
	employ-> ['employment', 'employees', 'employee', 'employer', 'employed', 'employers']
	employe-> ['employees', 'employee', 'employer', 'employed', 'employers', '--']
	employee-> ['employees', 'employee', '--', 'employment', 'employer', 'employed']

Word 5: scenes
	s-> ['search', 'site', 'see', 'so', 's', 'services']
	sc-> ['school', 'science', 'schools', 'screen', 'score', 'schedule']
	sce-> ['scene', 'scenes', '--', 'search', 'see', 'services']
	scen-> ['scene', 'scenes', '--', 'send', 'science', 'seen']
	scene-> ['scene', 'scenes', '--', '--', 'see', 'send']

Word 6: snow
	s-> ['search', 'site', 'see', 'so', 's', 'services']
	sn-> ['snow', '--', 'search', 'site', 'see', 'so']
	sno-> ['snow', '--', 'so', 'some', 'should', 'software']

Word 7: capital
	c-> ['can', 'contact', 'c', 'click', 'city', 'copyright']
	ca-> ['can', 'car', 'case', 'care', 'call', 'card']
	cap-> ['capital', 'capacity', 'cape', 'cap', 'capabilities', 'capture']
	capi-> ['capital', '--', 'california', 'casino', 'capacity', 'cape']
	capit-> ['capital', '--', 'capture', 'captain', '--', 'city']
	capita-> ['capital', '--', 'captain', '--', 'catalog', 'capacity']

Check partial_input with one deletion:

Word 0: regulations
	r-> ['re', 'rights', 'review', 'r', 'read', 'research']
	re-> ['re', 'review', 'read', 'research', 'reviews', 'real']
	reg-> ['register', 'region', 'registered', 'regional', 'registration', 'regular']
	regu-> ['regular', 'regulations', 'regulation', 'regulatory', 'regularly', '--']
	regua-> ['--', 'regular', 'regarding', 'regulations', 'regulation', 'regulatory']
	reguat-> ['--', 'regulations', 'regulation', 'regulatory', '--', 'results']
	reguati-> ['--', 'regulations', 'regulation', '--', 'relations', 'relationship']
	reguatio-> ['--', 'regulations', 'regulation', '--', 'relations', 'relationship']
	reguation-> ['--', 'regulations', 'regulation', '--', 'relations', 'relationship']
	reguations-> ['--', 'regulations', '--', 'relations', 'relationship', 'relationships']

Word 1: exciting
	e-> ['e', 'email', 'each', 'ebay', 'education', 'even']
	ex-> ['experience', 'example', 'exchange', 'executive', 'excellent', 'express']
	exc-> ['exchange', 'excellent', 'except', 'exclusive', 'exception', 'excess']
	exci-> ['exciting', '--', 'exchange', 'excellent', 'existing', 'except']
	excit-> ['exciting', '--', 'exit', '--', 'edition', 'either']
	exciti-> ['exciting', '--', '--', 'edition', 'executive', 'existing']
	excitig-> ['--', 'exciting', '--']

Word 2: fri
	f-> ['for', 'from', 'free', 'first', 'find', 'full']
	fi-> ['first', 'find', 'file', 'financial', 'field', 'files']

Word 3: authors
	a-> ['and', 'a', 'are', 'at', 'as', 'all']
	at-> ['at', 'attention', 'attorney', 'attack', 'atom', 'atlanta']
	ath-> ['athletic', '--', 'at', 'author', 'although', 'authority']
	atho-> ['--', 'author', 'although', 'authority', 'authors', 'attorney']
	athor-> ['--', 'author', 'authority', 'authors', 'attorney', 'authorities']
	athors-> ['--', 'authors', '--', 'author', 'authority', 'attorney']

Word 4: platform
	p-> ['page', 'pm', 'price', 'people', 'products', 'product']
	pa-> ['page', 'part', 'pages', 'party', 'payment', 'park']
	pat-> ['patients', 'path', 'patient', 'patch', 'pattern', 'patterns']
	patf-> ['--', 'patients', 'path', 'patient', 'patch', 'platform']
	patfo-> ['--', 'platform', '--', 'performance', 'patients', 'path']
	patfor-> ['--', 'platform', '--', 'performance', 'pattern', 'perform']
	patform-> ['--', 'platform', '--', 'performance', 'perform', 'performed']

Word 5: still
	s-> ['search', 'site', 'see', 'so', 's', 'services']
	st-> ['state', 'store', 'states', 'students', 'still', 'stock']
	sti-> ['still', 'stick', '--', 'site', 'state', 'said']
	stil-> ['still', '--', 'style', 'silver', 'skills', 'soil']

Word 6: summer
	s-> ['search', 'site', 'see', 'so', 's', 'services']
	sm-> ['small', 'smith', 'smart', 'smoking', 'smaller', 'smooth']
	smm-> ['--', 'some', 'same', 'small', 'something', 'similar']
	smme-> ['--', 'some', 'same', 'something', 'someone', 'summer']
	smmer-> ['--', 'summer', '--', 'services', 'some', 'service']

Word 7: spanking
	s-> ['search', 'site', 'see', 'so', 's', 'services']
	sp-> ['special', 'sports', 'space', 'specific', 'speed', 'sponsored']
	spa-> ['space', 'spain', 'spanish', 'spa', 'spam', 'spaces']
	span-> ['spanish', 'spanking', '--', 'san', 'standard', 'space']
	spank-> ['spanking', '--', 'spanish', '--', 'san', 'standard']
	spankn-> ['--', 'spanking', '--', 'spain', 'spanish']
	spankng-> ['--', 'spanking', '--']

Check partial_input with one substitution:

Word 0: magazines
	m-> ['more', 'my', 'may', 'me', 'most', 'music']
	mw-> ['--', 'more', 'my', 'may', 'me', 'most']
	mwg-> ['--', 'might', 'magazine', 'magazines', 'magic', 'mg']
	mwga-> ['--', 'magazine', 'magazines', '--', 'may', 'make']
	mwgaz-> ['--', 'magazine', 'magazines', '--']
	mwgazi-> ['--', 'magazine', 'magazines', '--']
	mwgazin-> ['--', 'magazine', 'magazines', '--']
	mwgazine-> ['--', 'magazine', 'magazines', '--']
	mwgazines-> ['--', 'magazines', '--', 'magazine']

Word 1: pension
	p-> ['page', 'pm', 'price', 'people', 'products', 'product']
	pe-> ['people', 'per', 'personal', 'person', 'performance', 'period']
	pen-> ['pennsylvania', 'penis', 'pen', 'penalty', 'pension', '--']
	pens-> ['pension', '--', 'personal', 'person', 'persons', 'pennsylvania']
	pensi-> ['pension', '--', 'penis', '--', 'personal', 'person']
	pensin-> ['--', 'pension', '--', 'personal', 'person', 'persons']
	pensinn-> ['--', 'pension', '--', 'personnel']

Word 2: across
	a-> ['and', 'a', 'are', 'at', 'as', 'all']
	aa-> ['aa', '--', 'and', 'a', 'are', 'at']
	aar-> ['--', 'are', 'area', 'art', 'article', 'around']
	aaro-> ['--', 'around', 'across', 'abroad', 'acrobat', '--']
	aaros-> ['--', 'across', '--', 'around', 'arts', 'almost']
	aaross-> ['--', 'across', '--']

Word 3: hate
	h-> ['have', 'home', 'has', 'he', 'his', 'here']
	hn-> ['--', 'have', 'home', 'has', 'he', 'his']
	hnt-> ['--', 'hotel', 'hotels', 'hot', 'html', 'hit']
	hnte-> ['--', 'hotel', 'hotels', 'hunter', 'hate', '--']

Word 4: alex
	a-> ['and', 'a', 'are', 'at', 'as', 'all']
	ap-> ['application', 'april', 'applications', 'apr', 'apply', 'appropriate']
	ape-> ['--', 'are', 'area', 'american', 'application', 'april']
	apex-> ['--', 'alexander', 'alex', '--', 'are', 'area']

Word 5: kids
	k-> ['know', 'k', 'key', 'keep', 'kids', 'knowledge']
	kq-> ['--', 'know', 'k', 'key', 'keep', 'kids']
	kqd-> ['--', 'kids', 'kid', '--', 'know', 'k']
	kqds-> ['--', 'kids', '--', 'kansas', 'kinds', 'kits']

Word 6: useful
	u-> ['us', 'up', 'use', 'used', 'user', 'under']
	us-> ['us', 'use', 'used', 'user', 'using', 'usa']
	use-> ['use', 'used', 'user', 'users', 'useful', 'uses']
	usef-> ['useful', '--', 'use', 'used', 'user', 'users']
	usefo-> ['--', 'useful', '--', 'use', 'used', 'user']
	usefol-> ['--', 'useful', '--']

Word 7: exception
	e-> ['e', 'email', 'each', 'ebay', 'education', 'even']
	ex-> ['experience', 'example', 'exchange', 'executive', 'excellent', 'express']
	exz-> ['--', 'experience', 'example', 'exchange', 'executive', 'excellent']
	exze-> ['--', 'experience', 'executive', 'excellent', 'expected', 'except']
	exzep-> ['--', 'except', 'exception', '--', 'experience', 'example']
	exzept-> ['--', 'except', 'exception', '--', 'expected', 'expert']
	exzepti-> ['--', 'exception', '--', 'except', 'expertise']
	exzeptio-> ['--', 'exception', '--']
	exzeption-> ['--', 'exception', '--']

Check partial_input with two substitution:

Word 0: digital
	d-> ['do', 'date', 'day', 'data', 'd', 'de']
	di-> ['did', 'directory', 'digital', 'different', 'discussion', 'display']
	dig-> ['digital', 'digest', '--', 'did', 'directory', 'different']
	digs-> ['--', 'digital', 'discussion', 'display', 'district', 'discount']
	digsl-> ['--', '--', 'digital', 'discussion', 'display', 'district']
	digsla-> ['--', '--', 'digital', 'display', 'disease', 'distance']
	digslal-> ['--', '--', 'digital']

Word 1: anyone
	a-> ['and', 'a', 'are', 'at', 'as', 'all']
	an-> ['and', 'an', 'any', 'another', 'analysis', 'annual']
	ant-> ['anti', 'antonio', 'antique', 'antiques', 'anthony', '--']
	anto-> ['antonio', '--', 'another', 'auto', 'anyone', 'anti']
	antoa-> ['--', 'antonio', '--', 'another', 'analysis', 'auto']
	antoae-> ['--', '--', 'another', 'anyone', 'antonio']

Word 2: nobody
	n-> ['not', 'new', 'no', 'news', 'now', 'name']
	no-> ['not', 'no', 'now', 'north', 'non', 'note']
	nok-> ['nokia', '--', 'not', 'no', 'now', 'north']
	nokl-> ['--', 'nokia', '--', 'not', 'no', 'now']
	nokld-> ['--', '--', 'nokia', 'naked', 'noted', 'node']
	nokldy-> ['--', '--', 'nobody']

Word 3: recognized
	r-> ['re', 'rights', 'review', 'r', 'read', 'research']
	re-> ['re', 'review', 'read', 'research', 'reviews', 'real']
	rec-> ['recent', 'record', 'records', 'received', 'receive', 'recently']
	reco-> ['record', 'records', 'recommended', 'recommend', 'recovery', 'recommendations']
	recoi-> ['--', 'record', 'records', 'received', 'receive', 'recommended']
	recoin-> ['--', 'recognition', 'recognized', 'recognize', '--', 'recent']
	recoini-> ['--', 'recognition', 'recognized', 'recognize', '--', 'recording']
	recoinih-> ['--', '--', 'recognition', 'recognized', 'recognize']
	recoinihe-> ['--', '--', 'recognized', 'recognize']
	recoinihed-> ['--', '--', 'recognized']

Word 4: champion
	c-> ['can', 'contact', 'c', 'click', 'city', 'copyright']
	ch-> ['check', 'change', 'children', 'changes', 'china', 'child']
	cha-> ['change', 'changes', 'chapter', 'chat', 'channel', 'charge']
	chag-> ['--', 'change', 'changes', 'chapter', 'chat', 'channel']
	chagp-> ['--', 'chapter', 'championship', 'champion', '--', 'change']
	chagpi-> ['--', 'championship', 'champion', '--', 'chapter', 'capital']
	chagpic-> ['--', '--', 'championship', 'champion']
	chagpicn-> ['--', '--', 'championship', 'champion']

Word 5: camping
	c-> ['can', 'contact', 'c', 'click', 'city', 'copyright']
	cu-> ['current', 'customer', 'currently', 'customers', 'culture', 'custom']
	cum-> ['cum', 'cumshot', 'cumshots', '--', 'company', 'comments']
	cumz-> ['--', 'cum', 'cumshot', 'cumshots', '--', 'company']
	cumzi-> ['--', '--', 'committee', 'commission', 'coming', 'cum']
	cumzin-> ['--', '--', 'coming', 'combined', 'combination', 'cutting']
	cumzing-> ['--', '--', 'coming', 'cutting', 'camping']

Word 6: identify
	i-> ['in', 'is', 'i', 'it', 'if', 'information']
	ij-> ['--', 'in', 'is', 'i', 'it', 'if']
	ijd-> ['--', 'index', 'industry', 'id', 'individual', 'india']
	ijdn-> ['--', '--', 'in', 'information', 'into', 'info']
	ijdnt-> ['--', '--', 'into', 'international', 'internet', 'interest']
	ijdnti-> ['--', '--', 'identify', 'identified', 'identity', 'identification']
	ijdntif-> ['--', '--', 'identify', 'identified', 'identification']
	ijdntify-> ['--', '--', 'identify']

Word 7: confidence
	c-> ['can', 'contact', 'c', 'click', 'city', 'copyright']
	co-> ['contact', 'copyright', 'company', 'could', 'comments', 'community']
	cor-> ['corporate', 'corporation', 'core', 'correct', 'corner', 'corresponding']
	corf-> ['--', 'conference', 'corporate', 'corporation', 'core', 'correct']
	corfi-> ['--', 'configuration', 'confidence', 'confirm', 'confirmed', 'configure']
	corfiu-> ['--', '--', 'configuration', 'confidence', 'confirm', 'confirmed']
	corfiue-> ['--', '--', 'confidence']
	corfiuen-> ['--', '--', 'confidence']
	corfiuenc-> ['--', '--', 'confidence']
	corfiuence-> ['--', '--', 'confidence']

[Finished in 1.2s]
```
