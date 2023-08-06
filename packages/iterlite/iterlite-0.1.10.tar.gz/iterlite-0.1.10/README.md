# Better iterators for python (all typed)

## Examples

### 1. Simple

```python
## create iterator for even integers squared
even_integers = Iter(range(100)) \
    .filter(lambda x: x % 2 == 0) \
    .map(lambda x: x ** 2)

## to evaluate into a list use
my_list = even_integers.to_list()

## The smart list will allow the usage of iterator notation again by
times2_iter = my_list.iter() \
    .map(lambda x: x * 2)
```

### 2. Usage with inbuilt types
Unfortunately python doesn't support extensions to in-built types.
Thus we can only create wrappers to allow the functionality

To use it with in-built lists while keeping the list functionality use
```python
# Instead of 
my_list = list([5, 4, 3, 2, 1])
# Use the following to be Iter compatible
my_list = SList([5, 4, 3, 2, 1])
```

### 3. Sized iterators
When using stored data where we know the size of the collection (see [collection](https://docs.python.org/3/library/collections.html))

Then we can wrap them slightly differently to have a few more functions in a nice format
```python
# store the list as a collection iterable (aka sized)
my_collection = IterCollection(list(10)) 

# Then we can know the length of the collection without having to traverse the iterator
l = my_collection.len() # will call the __len__ of the wrapped class. In this case list

# We can also reverse the collection
rev = my_collection.reversed() # returns an iterator not a collection

```