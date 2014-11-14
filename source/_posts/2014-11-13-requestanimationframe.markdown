---
layout: post
title: "Improve your animation performance with requestAnimationFrame"
date: 2014-05-03 06:09:19 -0800
comments: true
categories: javascript
---

At their most basic core, browser animations have the following structure:


  1. Make some calculations
  2. Update the plot
  3. Goto 1.

A not-great way of doing this is with the timer functions provided by the browser:

```javascript
function animate() {
  makeCalculations();
  updatePlot();
}
var timestep = 50 // 50 ms, e.g. 20 fps;
window.setInterval(animate, timestep);
```

## When timers aren't on time

This will get the job done, but the results often leave much to be desired.  The animation may be choppy and uneven because timers are handled [in the same thread of execution as other asynchronous browser events](http://ejohn.org/blog/how-javascript-timers-work/), and may not fire precisely when you'd like.

For the smoothest animations, we'd like to use a very small timestep between frames.  This is a bit of a conundrum because decreasing the size of the timestep makes deviations from perfect timing the most noticeable.  This is because the same amount of absolute error in our timing function will represent a larger precentage of a smaller interval.

## Monitor refresh effect

Crazy things can happen when the rate of change in a phenomenon (in the browser, or in life) is happening at a different rate than we can percieve it.  In the study of optical illusions, the [wagon-wheel effect](http://en.wikipedia.org/wiki/Wagon-wheel_effect) is when we percieve motion to be slowed or even reversed from the true direction of motion. This occurs because of "temporal aliasing" by the recording medium into discrete frames.

For browser animations, the lesson to take from this is that the difference between our animation's fps and the monitor's refresh fps can have a big impact on the percieved smoothness of our animation.  Nat Duca and Tom Wilzius discussed this form of "jank" in their Google I/O presentation [Jank Free: Chrome Rendering Performance](http://www.youtube.com/watch?v=n8ep4leoN9A).

## Render performance with requestAnimationFrame

Browser developers have given us a better alternative for animations called `requestAnimationFrame`.  rAF should get called when you are ready to draw another frame, and the browser will know to update before it's next repaint to give you the best possible render performance.

Our simple example above becomes

```javascript

function animate() {
  makeCalculations();
  updatePlot();
  requestAnimationFrame(animate);
}

requestAnimationFrame(animate);
```

Browser support is getting [pretty good](http://caniuse.com/#feat=requestanimationframe), and there are [polyfills available](https://gist.github.com/paulirish/1579671) that will fall back to `setInterval` where it's unsupported.

Now go forth and `requestAnimationFrame`!