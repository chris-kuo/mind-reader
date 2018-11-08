import curses
from curses import wrapper
import urllib.request
import sys

from AutocompletionSuggestor import WordSuggestor


def main(stdscr):
    # start color in curses
    curses.start_color()
    curses.noecho()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

    # Clear screen
    stdscr.clear()
    
    # Create word suggestor and load dictionary and word weight
    words_to_import = 10000
    url = 'http://norvig.com/ngrams/count_1w.txt'
    stdscr.addstr(0, 0, 'Downloading %s' % url)
    stdscr.refresh()
    freq_map = dict()
    with urllib.request.urlopen(url) as f:
        stdscr.addstr(1, 0, 'Processing frequency list file')
        stdscr.refresh()
        for line_number in range(words_to_import): # load top frequency words
            line = f.readline()
            word, freq = line.strip().split()
            word = word.decode('utf-8')
            freq = int(freq)
            freq_map[word] = freq
    stdscr.addstr(2, 0, 'First %d words loaded from %s' % (len(freq_map), url))
    stdscr.refresh()
    # build dictionary from frequency map
    stdscr.addstr(3, 0, 'Loading dictionary...')
    stdscr.refresh()
    dictionary = list(freq_map)

    # Instantiate Word Suggestor
    suggestor = WordSuggestor()

    # load dictionary
    suggestor.load_dictionary(dictionary)

    # load word weights
    stdscr.addstr(4, 0, 'Loading word weights...')
    stdscr.refresh()
    suggestor.load_word_weight(freq_map)

    # check number of words loaded
    stdscr.addstr(5, 0, 'Check suggestor dicationary contains %d words...' % words_to_import)
    stdscr.refresh()
    assert suggestor.total_number_of_words() == words_to_import
    stdscr.addstr('pass\n')
    stdscr.refresh()

    stdscr.addstr(6, 0, 'Press enter to begin.')
    c = stdscr.getch()
    while c != curses.KEY_ENTER and c != 10 and c != 13:
        c = stdscr.getch()
    stdscr.clear()

    # input buffer
    buf = []

    while True:
        # Get screen height
        height, width = stdscr.getmaxyx()

        # get keyboard input
        c = stdscr.getch()
        ch = chr(c)
        if (c == curses.KEY_BACKSPACE or c == curses.KEY_DC) and len(buf) > 1:
            buf.pop()
        elif ch.isalnum() or ch.isspace():
            buf.append(ch)

        partial_input = ''.join(buf).split()[-1]
        suggestion = ' '.join(suggestor.suggest(partial_input))

        stdscr.clear()
        # write suggestion to bottom of screen
        stdscr.attron(curses.color_pair(2))
        stdscr.addstr(height - 1, 0, suggestion[:width])
        stdscr.attroff(curses.color_pair(2))

        # write quit message
        stdscr.attron(curses.color_pair(1))
        stdscr.addstr(height - 2, 0, 'Press ctrl-c to quit')
        stdscr.attroff(curses.color_pair(1))

        # write input to screen
        stdscr.addstr(0, 0, ''.join(buf))
        stdscr.refresh()

try:
    wrapper(main)
except KeyboardInterrupt:
    sys.exit(0)
