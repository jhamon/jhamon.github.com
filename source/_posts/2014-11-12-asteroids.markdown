---
layout: post
title: "Learning prototypical inheritance with Asteroids"
date: 2013-10-12 16:28:49 -0800
comments: false
categories: javascript projects
---

Asteroids is more experiment than finished game since there are no win conditions. It's one of the first things I made using JavaScript, and it was a great way to wrap my head around JavaScript's prototypical inheritance. The game has several different types of objects (the spaceship, bullets, asteroids) that have specific behaviors but have a common need to know where they are, move around, etc. This is easily accomplished by having a base object, MovingObject.prototype, that all other objects delegate to (a.k.a. "inherit from").

Here's a simplified snippet showing the inheritance pattern:

```javascript
(function () {
    var Asteroids = window.Asteroids = (window.Asteroids || {});

    var MovingObject = Asteroids.MovingObject = function (options) {
      // initialization code to set up position, speed, etc.
    }
    MovingObject.prototype.move = function () {
      // complex logic to update object's position
      // based on position, speed, angular velocity, 
      // direction, acceleration, etc.
    }

    var Ship = Asteroids.Ship = function (options) {
      // Ship-specific initialization would go here
      Asteroids.MovingObject.call(this, options)
    };
    Ship.prototype = new MovingObject();
    Ship.prototype.constructor = Ship;

    // Repeat a similar procedure for Asteroid and Bullet constructors.
})();
```

To understand what's happening here, you have to know that every object has a hidden `[[Prototype]]` property that is set by the constructor function at creation time to whatever is at the constructor's `.prototype` property. Whenever we try to access a property that an object doesn't have, it defers to its prototype. So when we try to access a property on an object, the interpreter will check that object, then the object's prototype, then the prototype's prototype, etc until it finds a defined property with that name or reaches the end of the prototype chain and returns undefined. This is exactly what people are talking about when they refer to the "prototype chain".  

As a more concrete example, let's say I want to call ship.move() on a Ship instance that I create with `var ship = new Asteroids.Ship()`. Well, ship doesn't have a property called move and neither does the prototype of ship (e.g. `Ship.prototype`) which was an instance of `MovingObject`. But the prototype's prototype, e.g. `MovingObject.prototype` will have a function under the move property name.

I want to give a shoutout to Kyle Simpson for explaining prototypical inheritance (better known as "behavior delegation") in a way that actually makes sense.