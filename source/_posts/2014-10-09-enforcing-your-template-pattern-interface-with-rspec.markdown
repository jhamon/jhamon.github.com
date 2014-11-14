---
layout: post
title: "Enforcing your Template Pattern interface with RSpec shared examples"
date: 2014-10-09 18:00:35 -0700
comments: true
categories: rails testing rspec design-patterns
---

The template pattern comes into play when you have several different use cases that are mostly the same but differ in just a few ways.  Shared functionality and skeleton methods are defined in a base class, which will be overridden by each subclass.  Each subclass provides a different implementation for the skeleton functions, and because all these objects all share a common interface we can use them interchangeably in other parts of our code.

## Using class inheritance

The simplest way of implementing the template pattern is to define a base class that your various implementations inherit from and override. All of the methods we want included in the template subclasses must raise errors if not overridden.  That way, if no implementation is present in a subclass we will see an error.

Take these printer classes for example.

```ruby
class BasePrinter
  def prepare_and_print(data)
    print(magical_formatting(data))
  end

  def magical_formatting(data)
    "Magical data: #{data}"
  end

  def print(data)
    raise "Not implemented!"
  end
end

class PlainPrinter < BasePrinter
  def print(data)
    puts data
  end
end

class ShufflePrinter < BasePrinter
  def print(data)
    puts data.split("").shuffle.join
  end
end

class BogusPrinter < BasePrinter
  def bogus_print
    # whatever
  end
end
```

Now if we do `BogusPrinter.new.prepare_and_print(data)` we will see a "Not impelmented!" error because the expected `print` method was not defined in the subclass. A quick and easy fix.

This gets the job done, but doesn't seem ideal.  What if we want to make a printer class that writes data to a PDF file?  We might need this class to inherit from another class providing complex PDF logic.

```ruby
class PDFPrinter < BadassPDFLibrary
  def print(data)
    # do stuff
  end
end
```

## Wrap the base template into a module

Ruby only has single inheritance, so there's no way to subclass `BasePrinter` and `BadassPDFLibrary`.  One way around the single-inheritance problem is to wrap up our `BasePrinter` into a module to be included.

```ruby
module BasePrinter
  def prepare_and_print(data)
    print(magical_formatting(data))
  end

  def magical_formatting(data)
    "Magical data: #{data}"
  end

  def print(data)
    raise "not implemented"
  end
end

class PlainPrinter
  include BasePrinter

  def print(data)
    puts data
  end
end

class ShufflePrinter
  include BasePrinter

  def print(data)
    puts data.split("").shuffle.join
  end
end

class BogusPrinter
  include BasePrinter

  def bogus_print
    # whatever
  end
end

class PDFPrinter < BadassPDFLibrary
  include BasePrinter

  def print(data)
    # do stuff
  end
end
```

## Leveraging RSpec `shared_examples`

Using modules is a perfectly workable solution if we need to inherit from a different class.  But there's a third way we can enforce our expectations on the printer interface. That is to write some shared examples for this code that check for the presence of the expected methods.


```ruby

shared_examples "a printer class" do
  let(:printer) { described_class.new }

  it "should expose a #print method" do
    expect(printer).to respond_to(:print)
  end

  describe "#print" do
    it "should return nil" do
      expect(printer.print("Hello, World!")).to be_nil
    end
  end
end

printers = [
 PlainPrinter,
 BogusPrinter,
 ShufflePrinter,
 PDFPrinter
]

printers.each do |printer_class|
  describe printer_class do
    it_behaves_like "a printer class"
  end
end
```

This approach goes beyond the error-raising we get from the module or base class and allows us to make stipulations about the return values from each template method.  With a few tests like this, we can dispense with the need for abstract base methods.
