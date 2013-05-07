Title: Array slicing in Ruby and Python
Author: Jennifer Hamon
slug: array-slicing
Date: 03-29-2013
Category: Ruby, Python
Summary: Both Ruby and Python are use zero-indexed arrays, but each have their own quirks in the way they handle string slicing.
Status: Draft
-----------

I have an interest in foreign languages.  If you read web forums where foreign language nerds like to congregate you will hear a lot of opinions on whether it is harmful to learn similar languages at the same time. For example, many will tell you not to learn Esperanto while learning Spanish because it is too easy to confuse the two similar vocabularies in your mind.  

I'm surprised I don't often hear similar advice when it comes to programming languages.  I am trying to learn Ruby right now coming from a background in scientific programming with Python.  Since Ruby and Pyton are so similar, I've been on the lookout for similarities that could trip me up.  I think one of the best ways to keep each language separate in my mind is to explicityly address the differences.  In this entry, I'll take a look at how Ruby and Python differ in their handling of arrays. 

Both Ruby and Python are zero-indexed, which just means that the first element of the list is accessed with index zero.  So, for example, in Python

	:python
	>>> mylist = ["fuzzy", "pickles"]
	>>> mylist[0]
	'fuzzy'
	>>> mylist.append("furry")
	>>> mylist
	['fuzzy', 'pickles', 'furry']

And the same thing in Ruby is just 

	:ruby
	>> mylist = ["fuzzy", "pickles"]
	=> ["fuzzy", "pickles"]
	>> mylist[0]
  => "fuzzy"
	>> mylist << 'furry' # append element
	=> ["fuzzy", "pickles", "furry"]

So far there's almost one to one correspondence between the syntax of Python lists and Ruby arrays.  Where things start to get confusing is with array slicing. It's easy to get confused by array slicing in either language because they are often taught using just a few examples without much explanation.  We have to keep in mind that **array slicing is a "fence-post" problem.** 

## Fence post problems

Array slicing is a fence post problem because working with fenceposts rather than indexes lets you describe exactly where your slice is "cutting" the original array. A list with 5 elements (indexes shown) is separated by **6** fenceposts, which in Pythona and Ruby are also zero-indexed:

				| 0 | 1 | 2 | 3 | 4 |   <-- list element indices (fences)
				0   1   2   3   4   5   <-- slice indices (fenceposts)

Python gives us a lot of sugar when it comes to slicing lists.  The colon shorthand lets us access any sublist, access every n elements, and even reverse lists all using the same compact expressions.

	:python
	>>> range(10)[0:4]
	[0, 1, 2, 3]

	:ruby
	>> (0..10).to_a[0,4]
	=> [0, 1, 2, 3]

These two snippets look almost the same, right?  Don't be fooled! Python's colon syntax is specifying a sensible `[start_slice_index:end_slice_index:index_step(optional)]` format while ruby's bracket notation is taking `[start_slice_index, length of sublist to return]`. So, actually, these slice notations are not the same at all.

Python's colon notation is powerful and let's us easily slice out every second or third element in a list or reverse a list.

:python
>>> range(10)[0:10:3]
[0, 3, 6, 9]

So far as I know the same thing is not possible in ruby without rolling your own block.

:ruby
>> (0..10).to_a.select { |i| i % 3 == 0}
=> [0, 3, 6, 9]

So simple cases like "give me every third element of this list" are a little more verbose in ruby, but the tradeoff is that we have the power to easily craft more detailed custom filters.
