from MindReader import MindReader
import keyword
import curses
from curses import wrapper
import urllib.request
import sys
import keyword


def main(stdscr):
	# start color in curses
	curses.start_color()
	curses.noecho()
	curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
	curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

	# Clear screen
	stdscr.clear()
	
	# create MindReader instance
	suggestor = MindReader()

	# Create word suggestor and load dictionary and word weight
	words_to_import = 10000
	filename = 'count_1w.txt'
	with open(filename, 'r') as f:
		stdscr.addstr(1, 0, 'Loading python keyword and build-in words')
		with open('python_builtin_functions.txt') as f:
			for line in f:
				word = line.split()[0]
				suggestor.increment_primary(word)
		# load keyword
		for word in keyword.kwlist:
			suggestor.increment_primary(word)

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
		if (c == curses.KEY_BACKSPACE or c == curses.KEY_DC or c == 127) and len(buf) > 1:
			buf.pop()
		elif ch.isalnum() or ch.isspace():
			buf.append(ch)
			if ch.isspace():
				suggestor.increment_secondary(''.join(buf).split()[-1])

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
