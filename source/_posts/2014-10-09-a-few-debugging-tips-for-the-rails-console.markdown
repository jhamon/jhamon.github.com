---
layout: post
title: "A few debugging tips for the Rails console"
date: 2014-10-09 17:10:19 -0700
comments: true
categories: ruby
---

This post will be a little less coherent than some of the others, but I wanted to write down a few things I've found to be very helpful when trying to debug my Ruby code.

## Quickly find syntax errors

A surprising number of people don't know that you can run ruby with `-c` from the command line to learn about syntax errors. Let's say I have a simple `Dog` class with an unclosed string.

```ruby
# dog.rb
class Dog
  def initialize(name)
    @name = name
  end

  private
  def woof
    puts "woof
  end
end
```

This is a trivial example, but if I was having trouble tracking down the problem I'd do something like this:

```
$ ruby -c dog.rb
dog.rb:8: unterminated string meets end of file
dog.rb:8: syntax error, unexpected end-of-input, expecting keyword_end
```

## Inspecting instance variables

From the console, we have the power to reach inside an object and see its instance variables even if there are no getter and setter methods defined on the object.

```ruby
[2] pry(main)> d = Dog.new("Pluto")
=> #<Dog:0x007f82aac977d0 @name="Pluto">
[3] pry(main)> d.name
NoMethodError: undefined method `name' for #<Dog:0x007f82aac977d0 @name="Pluto">
from (pry):12:in `__pry__'
[4] pry(main)> d.instance_variable_get("@name")
=> "Pluto"
```

This slightly different syntax also works

```ruby
[5] pry(main)> d.instance_variable_get(:@name)
=> "Pluto"
```

If we're not sure what state the object is holding on to, we can get a list of all the defined instance variables using `#instance_variables`.

```
[6] pry(main)> d.instance_variables
=> [:@name]
```

## Calling private methods

If you want to call a private method from the command line, you can do so with `#send`.

```ruby
[7] pry(main)> d.woof
NoMethodError: private method `woof' called for #<Dog:0x007fd65acfe9b8 @name="Pluto">
from (pry):17:in `__pry__'
[8] pry(main)> d.send(:woof)
woof
=> nil
```

## Discover where a method was defined

Sometimes, especially when working on a big application with other people, it's tricky to learn where a particular method is defined.  This is especially true when classes are being extended by gems that you did not write or install yourself.  

To track those down, you can do this in the console.

```ruby
instance.method(:method_name).source_location
```

For example, I might do something like this:

```
[25] pry(main)> Rails.method(:cache).source_location
=> ["/Users/jhamon/.rvm/gems/ruby-2.0.0-p247/gems/railties-4.1.4/lib/rails.rb", 32]
```

If the `cache` method had been overridden, as it sometimes is by gems like `dalli_store`, I would see a reference to that gem instead of rails.