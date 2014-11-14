---
layout: post
title: "Don't reinvent the wheel :<br>Rails validations beyond the basics"
date: 2013-10-10 23:43:11 -0700
comments: true
categories: ruby rails refactoring
---

If you've gone through a Rails tutorial like the Hartl Rails Tutorial or Rails For Zombies, you'll be familiar with common model validations that prevent saving duplicate or incomplete records.  Throughout this piece I'll be talking about a `Padawan` class, that might begin looking something like this:

```ruby
class Padawan < ActiveRecord::Base
  validates :age, :presence => true
end
```

This is a fine first step, but it only goes a small distance toward verifying any records we might try to save are actual valid Padawans. There is a conspicuous lack of business logic. Right now anyone with an age can be saved into the database, even those who are too old to begin the training.

## Custom validations

If we dig in a little further with documentation and Stack Overflow answers we begin to learn about defining custom validators that implement attribute checks that are tailored to our application.  

A custom validator is just a method that adds an error message if a given conditions is not met.  A validator method that does not add any error messages is considered to have passed.  So it's simple to begin writing code like this:

```ruby
class Padawan < ActiveRecord::Base
  validates :age, :presence => true
  validate :not_too_old_to_be_trained
    
  def not_too_old_to_be_trained
    errors.add(:age, "is too old to be trained") if age > 9
  end
end
```

We can fire up the console and quickly verify this does what we expect

```ruby
2.0.0-p247 :008 > luke = Padawan.create(name: "Luke Skywalker", age: 25)
   (0.1ms)  begin transaction
  Padawan Exists (0.1ms)  SELECT  1 AS one FROM "padawans"  WHERE "padawans"."name" = 'Luke Skywalker' LIMIT 1
   (0.0ms)  rollback transaction
 => #<Padawan id: nil, age: 25, name: "Luke Skywalker", midichlorian_count: nil, created_at: nil, updated_at: nil>
2.0.0-p247 :009 > luke.errors.full_messages
 => ["Age is too old to be trained"]
```

Suck it, Luke Skywalker!  You're too old to be trained!  

## Not the refactor you were looking for

We're successfully keeping the old fogies out of the Jedi Academy now, but plenty of people would look at this new code and be like 

> *Woah, [magic numbers](http://stackoverflow.com/questions/47882/what-is-a-magic-number-and-why-is-it-bad)! This is not the refactor you were looking for.*

Actually, they probably wouldn't say that. But they'd be thinking it while they downgrade their opinion of you. So let's at least be a little more explicit with named constants and a bit of explanation for anybody who might work on this code after us.

```ruby
class Padawan < ActiveRecord::Base
  # Master Yoda says people over a certain age are 
  # too old to begin the training
  MAX_AGE = 9
  
  validates :age, :presence => true
  validate :not_too_old_to_be_trained
    
  def not_too_old_to_be_trained
    errors.add(:age, "is too old to be trained") if age > MAX_AGE
  end
end
```

# Babies with lightsabers? Oh my!

If we wrote a few specs against this code, we'd realize that even babies in diapers are able to pass the validation, which doesn't seem like a great idea.  Imagine the trouble a baby with a lightsaber might get into! Or a toddler who can *use the Force* during tantrums! It won't do.

Let's modify our validator to check against a range of ages, and give the validator a more appropriate name.

```ruby
class Padawan < ActiveRecord::Base
  # Master Yoda says people over a certain age are 
  # too old to begin the training...
  MAX_AGE = 9
  # ...but we can't safely put lightsabers in the 
  # hands of babes, so we need this floor threshold too.
  MIN_AGE = 5
  
  validates :age, :presence => true
  validate :is_an_acceptable_age_to_be_trained
    
  def is_an_acceptable_age_to_be_trained
    if age > MAX_AGE
     errors.add(:age, "is too old to be trained")
    elsif age < MIN_AGE
     errors.add(:age, "is too young to be trained")
    end
  end
end
```

Now that we have our age requirements down, we remember that `midichlorian_count` is also a factor when selecting Padawans for training.  To borrow a useful piece of Harry Potter argot, we don't want to waste time training squibs.  So we'd better create a validation for midichlorians too.

```ruby
class Padawan < ActiveRecord::Base
  # Master Yoda says people over a certain age are 
  # too old to begin the training...
  MAX_AGE = 9
  # ...but we can't safely put lightsabers in the 
  # hands of babes, so we need this floor threshold too.
  MIN_AGE = 5
  
  MIDICHLORIAN_THRESHOLD = 9000
  
  validates :age, :presence => true
  validate :is_an_acceptable_age_to_be_trained
  validate :has_enough_midichlorians
  
  def is_an_acceptable_age_to_be_trained
    if age > MAX_AGE
     errors.add(:age, "is too old to be trained")
    elsif age < MIN_AGE
     errors.add(:age, "is too young to be trained")
    end
  end

  def has_enough_midichlorians
    if midichlorian_count < MIDICHLORIAN_THRESHOLD
        errors.add(:midichlorian_count, "is too low to be trained") 
      end
  end
end
```

If we were writing a whole application, we could continue on adding validations in this way for quite a while.  For very small apps we might never have a problem.  

## I felt a moderately-sized disturbance in the force

If you're like me you might start to cringe as requirements increase and we find ourselves maintaining dozens of lines of validation code to do things as basic as checking whether a value falls within a range.  As it is, we're nearly up to 40 lines and all we've done is check that two properties fall within a particular range. Inconcievable! 

As we write more and more validations, patterns begin to emerge.  What's that, you say?  A *disturbance in the Force*? It's as if a thousand methods cried out all at once to be DRYed up.

```ruby
class Padawan < ActiveRecord::Base
  # Master Yoda says people over a certain age are 
  # too old to begin the training...
  MAX_AGE = 9
  # ...but we can't safely put lightsabers in the 
  # hands of babes, so we need this floor threshold too.
  MIN_AGE = 5
  
  MIDICHLORIAN_THRESHOLD = 9000
  
  validates :age, :presence => true
  validate :is_an_acceptable_age_to_be_trained
  validate :has_enough_midichlorians
    
  def is_an_acceptable_age_to_be_trained
    attribute_greater_than_or_equal_to :age, MIN_AGE
    attribute_less_than_or_equal_to :age, MAX_AGE
  end
  
  def has_enough_midichlorians
    attribute_greater_than_or_equal_to :midichlorian_count,
                                        MIDICHLORIAN_THRESHOLD
  end

  def attribute_greater_than_or_equal_to(attribute_name, minimum)
    unless self.send(attribute_name) >= minimum
      errors.add(attribute_name, "is smaller than #{minimum}")
    end
  end

  def attribute_less_than_or_equal_to(attribute_name, maximum)
    unless self.send(attribute_name) <= maximum
      errors.add(attribute_name, "is larger than #{maximum}")
    end
  end
end
```

Is this better? Now our code is even longer than before (!), but we can see how the savings from abstracting these range checks into methods would compound as we validate more attributes in the future.

This is a definite step in the right direction, but it's beginning to look like this validation logic could probably be further generalized and be pulled into a Concern; there's nothing inside `attribute_less_than_or_equal_to` or `attribute_greater_than_or_equal_to` that depends on `Padawan`. If any other ActiveRecord models have similar types of validations---and we have every reason to believe that they would---we don't want to duplicate and maintain that code in more than one place in our project.

# A little knowledge is a dangerous thing

So what's a Rails Padawan on the path to mastery to do in this situation? It turns out that the Rails developers have already solved this problem for us.

Custom validations are wonderful tools, but a little due diligence and study of the excellent [Rails Guide on ActiveRecord validations](http://guides.rubyonrails.org/active_record_validations.html) at the beginning would have saved us a lot of effort in applying them in this situation. The docs show that ActiveRecord already ships with a large set of validation helpers that handle common scenarios like this.

```ruby
class Padawan < ActiveRecord::Base
  # Master Yoda says people over a certain age are 
  # too old to begin the training...
  MAX_AGE = 9
  # ...but we can't safely put lightsabers in the 
  # hands of babes, so we need this floor threshold too.
  MIN_AGE = 5
  
  MIDICHLORIAN_THRESHOLD = 9000
  
  validates :age, :presence => true, 
                  :numericality => { greater_than: MIN_AGE, 
                                     less_than: MAX_AGE }
  validates :midichlorian_count, 
            :presence => true,
            :numericality => { greater_than: MIDICHLORIAN_THRESHOLD }
end
```

And check these out:

```ruby
  class SithLord < ActiveRecord::Base
    validates :name, 
              :format => { with: /^Darth\ /}

    validates :lightsaber_color,
              :exclusion => { in: %w(green blue) }

    validates :undercover, 
              :inclusion => { in: [true, false] }

    validates :catchphrase, :length => {
      minimum: 10,
      too_short: "must have at least %{count} characters"
    }
  end
```

May the docs be with you!