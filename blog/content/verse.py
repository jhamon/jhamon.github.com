#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import curses
from string import center
import sys

def ShowSyntax():
	print 'deadpoets requires you to specify one text file.'
	print 'Usage: deadpoets filename'

filename = sys.argv[-1]
try:
	poem = open(filename, 'r').readlines()
except: 
	print 'The text file you specified could not be opened.'
	ShowSyntax()

obscar = '.'
punct = '\'\"?!,'

# raven = open(FILENAME,'r').readlines()
# ozy = open('Ozymandias.txt').readlines()

def is_empty(line):
	return list(line).count(' ') == len(line)

def strip_newlines(poem):
	return [x.replace('\n','') for x in poem]


def obscure_word_interiors(line):
	if is_empty(line):
		return line
	else:
		words = line.split(' ')
		newwords = []
		for word in words:
			if len(word)>2:
				if word[0] in punct and word[-1] in punct:
					word = word[0:2] + obscar*(len(word)-4) + word[-2:]
				elif word[0] in punct:
					word = word[0:2] + obscar*(len(word)-3) + word[-1]
				elif word[-1] in punct:
					word = word[0] + obscar*(len(word)-3) + word[-2:]
				else:
					word = word[0] + obscar*(len(word)-2) + word[-1]

			else:
				word = obscar*len(word)
			newwords.append(word)
		line = ' '.join(newwords)
		return line

def obscure_all_but_first_letter_of_word(line):
	words = line.split(' ')
	newwords = []
	for word in words:
		if len(word) > 1:
			if word[0] in punct: #Begins with punctuation
				word = word[0:2] + obscar*(len(word)-2)
			else: # Doesn't begin with punctuation
				word = word[0] + obscar*(len(word)-1)
		else:
			word = obscar
		newwords.append(word)
	# words = [w[0]+obscar*(len(w)-1) for w in words]
	line = ' '.join(newwords)
	return line

def obscure_all_but_last_letter_of_word(line):
	words = line.split(' ')
	words = [obscar*(len(w)-1)+w[-1] for w in words]
	line = ' '.join(words)
	return line


screen = curses.initscr() 
curses.noecho() 
curses.curs_set(0) 
screen.keypad(1) 
# curses.start_color()

def print_title():
	maxY,maxX = screen.getmaxyx()
	screen.addstr(center('DeadPoets: poetry trainer',maxX),curses.A_REVERSE)

def main_menu(num_of_lines):
	def draw_start_menu():
		maxY,maxX = screen.getmaxyx()
		print_title()
		screen.addstr('\n')
		screen.addstr(center('because the only way to truly',maxX))
		screen.addstr(center('know a text is to memorize it.',maxX))
		# screen.addstr("\n That's how long I want to remember what I study.")
		pad1 = '\n\n      '
		pad2 = '\n           '
		screen.addstr(pad1+'What would you like to do?')
		screen.addstr(pad2 + '1) Read the whole poem.')
		screen.addstr(pad2 + '2) Read the poem with some letters obscured')

	# Get menu selection
	press = 0
	while press == 0:
		event = screen.getch() 
		if event == ord("q"): 
			break 
		elif event == ord("1"): 
			# screen.clear()
			screen.clear()
			print_poem()
		elif event == ord("2"):
			screen.clear()
			screen.addstr(obscure_word_interiors(ozy[b])+'\n')

	b = 0
	draw_start_menu()
			b = b + 1



ozy = strip_newlines(ozy)
raven = strip_newlines(raven)

main_menu(len(ozy))

# for line in raven:
# 	print obscure_all_but_first_letter_of_word(line)

# print
# for line in ozy:
# 	print obscure_word_interiors(line)

# print 
# for line in raven:
# 	print obscure_word_interiors(line)