---
layout: post
title: "AdoptMeme:<br>Meme generator meets petfinder.com"
date: 2013-11-15 16:05:44 -0800
comments: true
categories: projects
---

<p>When I began <a href="http://www.adoptme.me">AdoptMe.me</a>, I knew it was an ambitious project because of the many moving parts involved.  I learned a lot from the process, both successes and failures, but the project is currently on inedefinite hiatus. You can view the bones live on the web at <a href="http://www.adoptme.me">AdoptMe.me</a>.  </p>

<p>I originally conceived of the site as a cat meme generator in the same vein as icanhascheezburger, but with a social mission of bringing visibility to cats languishing in animal shelters. I thought that if a person is going to spend their time making funny captions for cat images and sharing them around, they might as well give the visibility to a cat that needs it.  </p>

<a href="http://www.adoptme.me"><img class="projects pull-left" src="images/AdoptMeme.png" alt="AdoptMe.me meme editor"></a>

<p>The technical vision was that I would pull images and data from the free petfinder.com API, push them into my Amazon S3 bucket, let users caption them with a canvas-based JavaScript editor, and then send the resulting image off to my Amazon S3 bucket.  The image would be watermarked with a generated shortlink that viewers of the image could follow to learn more about how to adopt that animal should they be interested in doing so.</p>

<h3>Rails Backend</h3>

<p>A lot needs to happen behind the scenes to create a site handling image media and integrating with third-party APIs.  Since I was deploying on Heroku, first order of business was to find a third-party provider of storage for all my image assets.  Amazon S3 was the obvious choice because it is cheap, fast, and reliable.  Amazon provides an official <span class="code">aws-sdk</span> gem for interacting with their web services, but it contains hundreds of methods for dozens of services so I ended up writing my own <span class="code">Storable</span> module that extends <span class="code">ActiveSupport::Concerns</span> to wrap just the functionality I needed with a simpler API.  My <span class="code">Storable</span> module follows a template pattern, allowing me to easily store and retrieve image data associated with any of my ActiveRecord models by specifying a filename root and including the module.</p>

<p>The backend included models for <span class="code">Pet</span>, <span class="code">Image</span>, and <span class="code">Caption</span>.  Pet models were created and populated using data fetched from the Petfinder JSON API.  I quickly discovered that their free API is worth about what I paid for it (i.e. not much), and I spent a lot of time writing code to clean or discard bogus responses.  <span class="code">Image</span> tracked the metadata for unaltered images associated with a <span class="code">Pet</span>, and <span class="code">Caption</span> tracked metadata for each user-created meme.  Having separate <span class="code">Image</span> and <span class="code">Caption</span> made the associations clear and easily extensible should I want to find, say, all memes with common text content or all memes derived from a particular animal or photo.</p>  

<p>I decided not to build views on the server side, because I knew the image editor I wanted to write would involve heavy JavaScript.  So the data in my models is all exposed via a JSON API for consumption by a client-side application I would develop with Backbone.js.</p>

<p>Finally, I used <span class="code">figaro</span> to manage my third-party credentials.  The <span class="code">figaro</span> gem allows me to store my private credentials in an initialization file that is not checked into source control, but the gem will load them into an environment variable for you when the app boots up.</p>

<h3>Backbone.js, HTML5 Canvas Frontend</h3>

<p>Visiting the site you will be served a static page with the Backbone application.  Much of the data is bootstrapped into the page to avoid unnecessary calls to my JSON API.  I made Backbone views for an index page, a meme creation editor, and a show pet/meme page where viewers could learn more about adopting.  Each of these views is complex, and involves one or more sub-views.</p>

<p>Coding an MVP version of the canvas-based meme editor was a straightforward task after some of my other Canvas projects.  A cat image is set as the background for the canvas element.  As the user types, the editor listens to keypress events and updates the overlayed text.  I wanted each image to have a shortlink-style url in the corner where a viewer of the image could visit and learn more about adopting the pet.  So I wrote the shortlink and watermarking logic on the backend, and was nearing the last piece of the MVP puzzle: uploading my newly captioned images.</p>

<h3> Problems with the Same-Origin Policy</h3>

<p>It is at that moment that I ran head-on into a Same-Origin security error.  I learned, painfully, that the browser's Same-Origin Policy was not going to let me save any of my users meme images directly to S3 because the background cat image was not coming from the same origin as the page I was serving from Heroku.  What I thought was going to be as easy as a call to <span class="code">canvas.toDataURL()</span> ended up being a much bigger problem.</p>

<p>I fiddled with server side generation of the captioned images using <span class="code">imagemagick</span> via the <span class="code">rmagick</span> gem.  I actually got this to work and its what you will experience if you try to use the live version of the site at this time.  This backend image manipulation is why the actual results do not match the editor preview. I realized quickly, however, that <span class="code">imagemagick</span> was slow, and I knew that blocking my Rails application with big image processing jobs was going to be unacceptably slow with more than one or two concurrent users.  And the image work wasn't a candidate to be a deferred job because the user is waiting to see their creation and share it around on the web.  </p>


<h3> Hiatus </h3>

<p>Given my knowledge at the time, the whole thing seemed unsalvageable at that point.  I made the decision to put the project on hold while I kept learning and working on other things, hoping to get back to it one day and do the job right.  Since then I've learned that what I originally intended may be possible with CORS, Cross-Origin Resource Sharing, so I'm excited to pick up again where I left off.</p>
