---
layout: post
title: "Serpent.io"
date: 2014-3-14 16:24:12 -0800
comments: false
categories: projects
---

When I first wrote this game I was still learning the "JavaScript way" of doing object-oriented programming with prototypical inheritance. I more or less succeeded in that aspect, but the code responsible for rendering the view and managing user interactions was a huge ball of mud. At that time I knew just enough jQuery to be dangerous, and while the basic mechanics seemed to work I had all my truth in the DOM and ran into a wall while trying to extend it to have more features. I wasn't unbinding events properly, so chaos ensued when I tried to reset the game for another play without a hard refresh. It was a mess, but I had other things I wanted to work on.

## Backbone reboot

I recently revisted the project for a couple of days to apply what I'd learned in the intervening months about keeping a clean separation between the `DOM` and my data with the help of a client-side framework called Backbone.js. I did an almost complete rewrite, and the game is now primarily driven by cascading events. The cell is the fundamental model of the game, which may belong to any of several different collections (`snakeSegments`, `apples`, `obstacles`) depending on the current state of that cell; these collections publish appropriate events when cells are added or removed, which trigger changes elsewhere in the game. For example, when an apple is eaten the game view hears the "appleEaten" event and knows to update the score and make a new apple.


Each square is a `div` with `display:inline-block` and special classes providing styles for each possible state. The squares each have an associated Backbone view that listens for change events on the cell data model. When the Backbone cell model changes, the cell view updates the CSS classes applied to its div element, creating the illusion of objects moving across the board. The game state is now maintained completely separate from the DOM's appearance thanks to views that listen only to data models.

## Rails backend

This was primarily a JavaScript project, but as a finishing touch I whipped up a simple Ruby on Rails backend to allow users to save scores to a scoreboard. A `HighScore` model is created when the Backbone app POSTs one to the `/high_scores` url. I originally fetched the scores with a GET request to `/high_scores`, but eventually moved to bootstrapping the high score data with the page delivering the Backbone app to avoid an unnecessary XHR request.


