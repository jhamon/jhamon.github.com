---
layout: post
title: "Building Elementary Cellular Automata in Ruby"
date: 2014-10-09 01:31:32 -0700
comments: true
categories: ruby projects design-patterns
---

Cellular automata are simulations where each location in a space can have a finite number of states (usually `on` or `off`, or `0` and `1`). The state at a particular location can change through time according to specific rules. Most such systems are fairly boring, but some sets of rules can give rise to surprisingly complex behavior.  Whole branches of math and computer science are devoted to the study of these simulations.

There's a good chance you've seen an implementation of *Conway's Game of Life*, which is the most well-known example of cellular automation. *Life* is set on a two-dimensional grid, and self-replicating [patterns](http://en.wikipedia.org/wiki/Conway%27s_Game_of_Life#Examples_of_patterns) called *gliders* are a common occurance. 

<img src="http://upload.wikimedia.org/wikipedia/commons/e/e5/Gospers_glider_gun.gif" style="float: right">


I am not a computer scientist, but I find the dancing patterns mesmerizing.  As a fun exercise, I decided to take my layman's knowledge of cellular automation and build my own implementation of the 256 different Elementary Cellular Automata. These are also very beautiful, but have so far made a much smaller pop culture splash than their cousin *Life*.

## Elementary Cellular Automata

The *Elementary* in *Elementary Cellular Automata* comes from the fact that the model space is restricted to only one dimension.  The grid in this case is a single row of pixels.  Rather than animating a one-pixel row, most representations of ECAs show time on the vertical axis by printing a new row for each timestep.

From one time-step to the next, a pixel will live or die according to rules that examine the state of a pixel and the state of its two neighboring pixels.
For convenience, we might represent the pattern in a particular location as the a three-digit string like `101` or `001`.  Since a particular pixel and its two neighbors can each be either a `1` or a `0`, there are `2*2*2 = 8` different possible patterns at a particular location.  The [Wikipedia article](http://en.wikipedia.org/wiki/Elementary_cellular_automaton) goes into a lot of detail about how these rules are derived.

## Program organization

A principal in good object-oriented design is to separate things that change from things that don't change.  With that in mind, I decided to use the composite pattern for the main `ElementaryCellularAutomata` class and abstract the changeable portions of the simulation logic their own classes. 

The 256 different kinds of rules into a `Rule` class.  A factory method configures the rule class to have a different behavior depending on the rule number.

I also handle print functions in a `Printer` class following a template pattern.  This is so I can easily print output to the console with one class, or save to png image with anohter.  And I could easily extend it to other types of printers in the future (PDF, jpg, etc) as long as those classes provide a `print` method.

You can check out the finished code and a gallery of the output [on github](https://github.com/jhamon/elementary_cellular_automata).

## JavaScript reboot

Just for fun, I decided to build an animated JavaScript version of this code.

<p data-height="463" data-theme-id="9963" data-slug-hash="ogvpxQ" data-default-tab="result" data-user="jhamon" class='codepen'>See the Pen <a href='http://codepen.io/jhamon/pen/ogvpxQ/'>Elementary Cellular Automata</a> by Jennifer Hamon (<a href='http://codepen.io/jhamon'>@jhamon</a>) on <a href='http://codepen.io'>CodePen</a>.</p>
<script async src="//assets.codepen.io/assets/embed/ei.js"></script>

