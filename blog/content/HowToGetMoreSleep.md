Title: Turn my mac into HAL 
Date: 12/2/2013 
Slug: sleep-schedule
Author: Jennifer Hamon 
Category: Productivity
Summary: In the past I have had some problems going to bed at a reasonable hour.  Now my computer tells me when I should.

In the past I have had some problems going to bed at a regular time.  When I get interested in something on the computer late at night, I often end up staying up well past the time when I should have gone to sleep.  This is bad because it affects my happiness and productivity significantly the following day.

This has happened to me a lot recently, so I decided to write a little script to nag me about the benefits of regular sleep if I'm on the computer in the wee hours of the morning.

### 1. Finding things for my computer to tell me

I started with a quick google search about healthy sleep to find things for my script to say.  I did a copy/paste on the first couple articles that looked good and edited them into a text file with one fact-filled sentence per line.  I deleted any lines that wouldn't stand on their own as a statement of fact, and gave it a descriptive name: `SleepFacts.txt`.

### 2. Writing the script

Next I need a small script to print a random line from my text file of sleep facts.  Much as I wish there were a `sort --random` type of command available, I couldn't find one so decided to write my own in python.  I saved the following into `~/scripts/print_random_line.py`:

	::python
	#!/usr/bin/env python
	# Prints one random line from a text file, e.g. SleepFacts.txt
	# usage: print_random_line.py ~/path/to/file

	from sys import argv
	import random

	try:
		filename = argv[1]
		file = open(filename,'r')
	except:
		print 'File not found.'
		sys.exit(1)
	lines = file.readlines()
	print lines[random.randrange(0,len(lines))]
	file.close()

Next I made the file executable and make it available from the command line by symlinking it to `/usr/bin`:

	::bash
	$ sudo chmod +x ~/scripts/print_random_line.py
	$ ln -s ~/scripts/print_random_line.py /usr/bin/printrl

Now I'm ready to make the computer say a random line in a text file using the builtin text-to-speech capability.  On a mac:
	
	::bash
	$ printrl SleepFacts.txt | say
	$ echo Jen: `printrl ~/txt/SleepFacts.txt` | say # Personalize it!

or on most linux systems

	::bash
	$ printrl SleepFacts.txt | espeak


### 3. Automating the process

Awesome.  Now I have something that performs the action I'm after, I just need to schedule it to execute and nudge me toward healthier sleep habits anytime I'm on the computer late at night.  `cron` is the perfect tool for this.

	::bash
     $ crontab -e 

And put this on a new line:

	::bash
     */10 0,1,2,3,4,5,6 * * * /usr/bin/printrl ~/txt/SleepFacts.txt | /usr/bin/say


### PROFIT! 

Now anytime I'm on the computer after midnight, my computer helpfully nags me every 10 minutes about the benefits of regular sleep.  Was this kind of silly?  Definitely.  But I think it will help me improve my habits.

> *"Without adequate sleep and rest, over-worked neurons can no longer function to coordinate information properly, and we lose our ability to access previously learned information."*
>
> *"A sleep-deprived person cannot focus attention optimally and therefore cannot learn efficiently."*
>
> *"Although chronic sleep deprivation affects different individuals in a variety of ways, it is clear that a good night’s rest has a strong impact on learning and memory."*
>
> **//powers off computer and goes to bed//**