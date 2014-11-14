---
layout: post
title: "Using JavaScript animation to communicate IFTTT at a glance"
date: 2014-08-11 16:11:20 -0700
comments: true
categories: javascript projects
---

<p data-height="268" data-theme-id="0" data-slug-hash="GhrjF" data-default-tab="result" data-user="jhamon" class='codepen'>See the Pen <a href='http://codepen.io/jhamon/pen/GhrjF/'>IFTTT Slottt Machine</a> by Jennifer Hamon (<a href='http://codepen.io/jhamon'>@jhamon</a>) on <a href='http://codepen.io'>CodePen</a>.</p>
<script async src="//codepen.io/assets/embed/ei.js"></script>

At IFTTT we're always looking for better ways to communicate what our service is and how people can use us to connect the services they love together in powerful ways.  One idea I had for this was to create an animation based on the if-logo-then-logo style presentation of recipes used on the [WTF page](http://www.ifttt.com/wtf) and elsewhere throughout the site.  With 442 triggers and 172 actions available at the time of this writing, there are over 76,000 distinct recipes you can make on IFTTT.  I really wanted to make something that would convey the wonderful variety of combinations that IFTTT makes possible.

<!--
![if-logo-then-logo-animation](https://gist.github.com/jhamon/19da977e9fe095e9601c/raw/c3830dcd563427effc867a44e249ada0a1e64d3f/slottt-fixed-short-scroll.gif)
-->

The animation I was imaginging takes some visual inspiration from the spinners on a slot machine.  After a little planning, I realized it wouldn't be too difficult to pull off with some CSS sleight of hand and a bit of JavaScript.  If you exclude the long list of asset urls, the finished JavaScript only weighs in around 50 lines.  In this article, I'm going to explain how I was able to combine absolute positioning with `overlow:hidden` and a small amount of jQuery to build a neat slot machine effect that works in all major browsers.

## Game plan

I decided that one easy approach would be to have three types of elements:

  - **A mask**: a wrapper div (or mask div) with a fixed size, `position: relative` and `overflow: hidden`.  For this project, I chose the class name `slottt-machine-recipe__mask`.
  - **An inner container to hold the icons**: an inner div to hold the icon images with `position: absolute`.  For this project I chose the class name `slottt-machine-recipe__items_container`.
  - **The actual icons**: I'm fortunate that IFTTT's great design team had already done the work of preparing nice looking assets in standard sizes for each [channel](http://www.ifttt.com/channels) supported on our platform.  To get around some weird issues I was having with unwanted extra spacing below `img` elements, I chose to make square divs with the icon images set as their backgrounds. I marked each icon div with the class `slottt-machine-recipe__item`

This setup is sufficient to conceal all but the "current" icon. The animation is achieved by manipulating the `top` property on the absolutely positioned container. To drive home the CSS setup, you can see what this arrangement looks like with `overflow: hidden` commented out and some extra border styles turned on:

![CSS setup](https://gist.githubusercontent.com/jhamon/19da977e9fe095e9601c/raw/50094976d831bd44561857efb0150d387450754d/IFTTT%20slot%20machine.png)

## Writing the CSS

All together, the CSS for those different elements looks something like this:

```css
.slottt-machine-recipe__mask {
    position: relative;
    overflow: hidden;
    width: 150px;
    height: 150px;
    display: inline-block;

    // These make the icons look better while
    // sitting inline with the if/then text.
    margin-left: 10px;
    margin-right: 10px;
    margin-bottom: -20px;

    // This border style is shown in the screenshot
    // but is not used in the final effect.
    /* border: 2px solid red; */
}

.slottt-machine-recipe__items_container {
    position: absolute;

    // This border style is shown in the screenshot
    // but is not used in the final effect.
    /* border: 2px dotted green; */
}

// The actual icon images will be set as
// backgrounds on divs of this class.
.slottt-machine-recipe__item {
    width: 150px;
    height: 150px;
    margin: 0px;
    padding: 0px;
    background-size: contain;
}
```

## Building the HTML

```html
<div class="slottt-machine-recipe">
  <span class="recipe_if">if</span>
  <div class="slottt-machine-recipe__mask" id="trigger_slot">
      <div class="slottt-machine-recipe__items_container">
      </div>
  </div>

  <span class="recipe_then">then</span>
  <div class="slottt-machine-recipe__mask" id="action_slot">
      <div class="slottt-machine-recipe__items_container">
      </div>
  </div>
</div>
```

Starting with this basic skeleton, I still needed to add the divs for each icon.  Since I had such a large number of icons to display and I wanted to be able to easily change them in the future without crawling through the raw html, I chose to build the innermost icon divs programmatically from a list of urls. I omitted the list to save space, but want to show the general approach:

```javascript
var triggers = [
  // a giant list of icon image urls
]

var actions = [
 // another giant list of icon image urls
]

function buildSlotItem (imgURL) {
    return $('<div>').addClass('slottt-machine-recipe__item')
                      .css({'background-image': 'url(' + imgURL + ')'})
}

function buildSlotContents ($container, imgURLArray) {
  $items = imgURLArray.map(buildSlotItem);
  $container.append($items);
}
```

This code gets invoked to build a div for each icon after the page is loaded:

```javascript
$(document).ready( function () {
  $trigger = $('#trigger_slot .slottt-machine-recipe__items_container');
  buildSlotContents($trigger, triggers);

  $action = $('#action_slot .slottt-machine-recipe__items_container');
  buildSlotContents($action, actions);

  setInterval(animate, 3500); // I'll talk about this later.
});
```

## Basic Animation

Since the inner div has `position: absolute` we can position it precisely with respect to the parent div as long as the parent has `position: relative`.  This means that changing which icon is displayed in the non-hidden area of the mask div can be done by setting the `top` position property on the inner container div to a multiple of the image size (150 pixels in this case).

From there, making a "sliding" effect is just a matter of animating the change of the `top` property with jQuery's `animate` function [(docs here)](http://api.jquery.com/animate/).  We could have written our own loop to take care of this, but jQuery has already done a nice job of implementing different easing functions, like `swing`, that specify a property's rate of change over time. Using non-linear easing gives the animation a nice polished feel.

```javascript
function animate() {
  var triggerIndex = randomSlotttIndex(triggers.length);
  $trigger.animate({top: -triggerIndex*150}, 500, 'swing');

  var actionIndex = randomSlotttIndex(actions.length);
  $action.animate({top: -actionIndex*150}, 700, 'swing');
}
```

![](https://gist.github.com/jhamon/19da977e9fe095e9601c/raw/427c34b8526ada47a1d94db62e37911ffcb2b02c/slottt-v1.gif)

## Forever upward

By now we are 90% to the finished result.  But instead of randomly scrolling the icons up or down, I really wanted them to scroll infinitely in the same direction. To pull this off we need to do a small amount of extra work to pop elements off the top of our inner container and push them onto the end.  By doing this, we can always scroll in the same direction without running out of icons to display.

```javascript
// Take the first n child elements from the $container and move them
// to the end.
function popPushNItems ($container, n) {
    $children = $container.find('.slottt-machine-recipe__item');
    $children.slice(0, n).insertAfter($children.last());

    if (n === $children.length) {
      popPushNItems($container, 1);
    }
}

// After the slide animation is complete, we want to pop some items off
// the front of the container and push them onto the end. This is
// so the animation can slide upward infinitely without adding
// inifinte div elements inside the container.
function rotateContents ($container, n) {
    setTimeout(function () {
      popPushNItems($container, n);
      $container.css({top: 0});
    }, 300);
}

function animate() {
  var triggerIndex = randomSlotttIndex(triggers.length);
  var actionIndex = randomSlotttIndex(actions.length);

  $trigger.animate({top: -triggerIndex*150}, 500, 'swing', function () {
    rotateContents($trigger, triggerIndex);
  });

  $action.animate({top: -actionIndex*150}, 700, 'swing', function () {
    rotateContents($action, actionIndex);
  });
}
```
You can see the resultant effect best by turning off the mask div's `overflow:hidden` property:

![](https://gist.github.com/jhamon/19da977e9fe095e9601c/raw/905d842398735d5522a59768742847535f61b1d9/pushpop.gif)

## Fine-tuning slide distance

For the basic version of the animation, I was just choosing a random icon to scroll to with a function like this:

```javascript
function randomSlotttIndex(max) {
  return (Math.random() * max | 0);
}
```

This was sufficient to test other aspects of the project, but in the finished product I really want to ensure that the icon we're spinning to is sufficiently "far" away that the random slot machine feel is preserved; randomly choosing to stay at the current position or roll to an icon only a few notches away just isn't as satisfying.  So, we modify our random index selection to account for that and reject small index choices.

```javascript
function randomSlotttIndex(max) {
  var randIndex = (Math.random() * max | 0);
  return (randIndex > 10) ? randIndex : randomSlotttIndex(max);
}
```

It's not a problem to reject these small indices as slide targets because of the way we are popping elements off and pushing them onto the end.  All the icons will be cycled through the different positions and will eventually be selected for display.

## Conclusion

That about wraps it up, and I hope you learned something that will be useful to you in your future projects.  You can view and tinker with the finished result on [codepen.io](http://codepen.io/jhamon/pen/GhrjF).
