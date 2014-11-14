---
layout: post
title: "My very own link shortener"
date: 2014-11-12 16:19:03 -0800
comments: false
categories: projects
published: false
---

I created this Backbone/Rails app because sometimes it's nice to have shortlinks, but I wanted to retain control of my links rather than routing them through a third-party service I have no control over. In it's present form, it only has one user-facing feature: enter a URL and recieve back a valid shortlink. It does one thing, and does it well.


## Rails Backend

Even though the public-facing site is almost trivial in what it offers at this time, I have kept in mind the analytics features of sites like Bitly.com while implementing a backend with separate models for `PageView`, `Shortlink`, `TargetUrl`, and `User`.

When you follow a shortlink, a controller logs that visit by creating a `PageView` before sending you on your way to your destination. Having distinct `Shortlink` and `TargetUrl` means that I will be able to easily compute and show visit analytics on a per-site or per-shortlink or per-user basis if I ever get around to it. `Shortlink` and `TargetUrl` must be separate models because a user might own a shortlink but not the associated target url; many people might create their own shortlinks for the same online destination.

The site serves my present needs just fine in its present form so I haven't built-out the analytics frontend. But I enjoyed thinking about the associations needed in the domain model on the backend.