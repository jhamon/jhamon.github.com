Title: Pelican blog says: Hello World!
Slug: hello-world
Date: 9/2/2013
Tags: tech
Summary: Can you hear me now?
<!-- Category: Personal -->

This is my first attempt to generate a blog using the Pelican static blog generator.  I'm hopeful that this will work because the last tool I tried to use, a static site generator called [hyde](http://www.github.com/hyde), seems to have been abandoned by its maintainer.  The official hyde installation instructions no longer work, and the maintainer has not addressed any of the issues languishing in the bug tracker since I filed my report about a month ago.  Prior to that I messed around with Jekyll/Octopress, but I'm not much of a rubyist.

But that's all okay because **[Pelican](http://www.github.com/getpelican/pelican)** is the cool new kid on the block: it's a python-based static website generator with a thriving community of users and contributors.  I'm not surprised the project is growing rapidly, because getting started with Pelican is as simple as running their `pelican-quickstart` script and answering a few questions about how you intended to use your site.  

## How to change the theme on your new Pelican-powered blog

After running the `pelican-quickstart` script and copying over some existing writing to the `content/` folder I was ready to tweak the theme.  It took a bit of googling for me to figure this out, so I'll summarize it here for anyone who is having a problem customizing their Pelican site theme.

First, get the `pelican-themes` repository:

    :::bash
    $ mkdir ~/path/to/themes
    $ cd ~/path/to/themes
    $ git clone git://github.com/getpelican/pelican-themes.git

Look through the screenshots and choose a theme that you like from those now present in `~/path/to/themes/pelican-themes/`.  When you find one that seems close to what you want, you're ready to update your Pelican configuration files:

    :::python
    # Put this in your pelicanconf.py file
    THEME = '~/path/to/themes/pelican-themes/theme_dir'

where `theme_dir` is the directory of the theme you like.  Next rebuild your site with `make html` and you're good to go.

The best way to get started on a custom theme of your own design is to copy one of the themes in the `pelican-themes` repo and start tinkering.  By doing that, you already have the necesasry structure in place for generating a theme.  The `simple` theme is provided for those who want to start from a relatively blank canvas.

Good luck with Pelican, and happy blogging!

