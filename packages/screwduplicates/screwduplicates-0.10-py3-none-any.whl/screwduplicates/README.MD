# provides a simple and efficient way to remove duplicates from an iterable (even with unhashable elements, optional order preservation)

## pip install screwduplicates

#### Tested against Windows 10 / Python 3.10 / Anaconda

### Duplicate Removal: 

It effectively removes duplicate elements from an iterable, ensuring that the returned iterable only contains unique values. This can be useful in scenarios where duplicate values need to be eliminated to avoid redundant or incorrect data.

### Flexibility: 

The function accepts a wide range of iterable types, including lists, tuples, and custom iterable objects. It can handle both hashable and unhashable elements, accommodating diverse data types.

### Order Preservation: 

The function provides an option to preserve the original order of elements in the iterable by setting the keep_order parameter to True. This is valuable when the order of elements matters, such as maintaining the sequence of items in a list.

### Error Handling: 

If the input iterable contains unhashable elements, the function gracefully handles the TypeError that arises during the conversion to a set. Instead of raising an error, it automatically switches to preserving order and includes a representation of the unhashable element in the output.


```python
testdict = {
    "List": [5, 4, 1, 2, 2, 3, 4, 5],
    "Set": {1, 2, 3, 4, 5},
    "Tuple": (1, 3, 4, 2, 3, 4, 5, 5, 5, 2, 2, 1),
    "Dictionary": {"a": 1, "b": 2, "c": 3},
    "String": "Hello",
    "Bytes": b"Hello",
    "List of strings": ["Hello", "World", "Hello"],
    "List of numbers": [2.5, 3.5, 1.5, 2.5, 3.5],
    "Empty list": [],
    "Set of strings": {"apple", "banana", "cherry"},
    "Set of numbers": {1, 2, 3, 4, 5},
    "Tuple of strings": ("apple", "banana", "cherry", "banana", "banana"),
    "Tuple of numbers": (3, 4, 5, 1, 2, 3, 4, 2, 3, 4, 2, 3, 4, 5),
    "Dictionary with numbers": {1: "one", 2: "two", 3: "three"},
    "Dictionary with strings": {"a": "apple", "b": "banana", "c": "cherry"},
    "List of mixed types": [1, "a", 2.5, True, True, True, 1, "a", "Hello"],
    "Set of mixed types": {1, "a", 2.5, True, "Hello"},
    "Tuple of mixed types": (1, "a", 2.5, True, "Hello", 1, "a", 2.5),
    "Nested list": [[1, 2], [3, 4], [5, 6], [1, 2], [3, 4], [3, 4], [5, 6]],
    "Nested set": {frozenset({1, 2}), frozenset({3, 4}), frozenset({5, 6})},
    "Nested tuple": ((1, 2), (3, 4), (5, 6), (3, 4)),
    "List with None value": [1, None, 3, None, 5],
    "Set with None value": {1, None, 3, None, 5},
    "Tuple with None value": (1, None, 3, None, 5),
    "List with boolean values": [True, False, True],
    "Set with boolean values": {True, False},
    "Tuple with boolean values": (True, False, True),
    "List with repeated values": [1, 1, 1, 1, 1],
    "Set with repeated values": {1, 1, 1, 1, 1},
    "Tuple with repeated values": (1, 1, 1, 1, 1),
    "List with mixed types and duplicates": [1, "a", 2, "a", 3, True, 3],
    "Set with mixed types and duplicates": {1, "a", 2, "a", 3, True},
    "Tuple with mixed types and duplicates": (1, "a", 2, "a", 3, True),
    "List with empty strings": ["", "World", "World", "Hello", "World"],
    "Set with empty strings": {"", "World", "Hello", "World", "World"},
}

from screwduplicates import del_duplicates
for key, item in testdict.items():
    print(f"\n---------------\n{key}:")
    print(f"Original: {item}")
    print(f"dont't keep order: {del_duplicates(item,keep_order=False)}")
    print(f"Keep order: {del_duplicates(item,keep_order=True)}")


# ---------------
# List:
# Original: [5, 4, 1, 2, 2, 3, 4, 5]
# dont't keep order: [1, 2, 3, 4, 5]
# Keep order: [5, 4, 1, 2, 3]
# ---------------
# Set:
# Original: {1, 2, 3, 4, 5}
# dont't keep order: {1, 2, 3, 4, 5}
# Keep order: {1, 2, 3, 4, 5}
# ---------------
# Tuple:
# Original: (1, 3, 4, 2, 3, 4, 5, 5, 5, 2, 2, 1)
# dont't keep order: (1, 2, 3, 4, 5)
# Keep order: (1, 3, 4, 2, 5)
# ---------------
# Dictionary:
# Original: {'a': 1, 'b': 2, 'c': 3}
# dont't keep order: {'a': 1, 'b': 2, 'c': 3}
# Keep order: {'a': 1, 'b': 2, 'c': 3}
# ---------------
# String:
# Original: Hello
# dont't keep order: {'H', 'o', 'l', 'e'}
# Keep order: ['H', 'e', 'l', 'o']
# ---------------
# Bytes:
# Original: b'Hello'
# dont't keep order: b'Hleo'
# Keep order: b'Helo'
# ---------------
# List of strings:
# Original: ['Hello', 'World', 'Hello']
# dont't keep order: ['World', 'Hello']
# Keep order: ['Hello', 'World']
# ---------------
# List of numbers:
# Original: [2.5, 3.5, 1.5, 2.5, 3.5]
# dont't keep order: [1.5, 2.5, 3.5]
# Keep order: [2.5, 3.5, 1.5]
# ---------------
# Empty list:
# Original: []
# dont't keep order: []
# Keep order: []
# ---------------
# Set of strings:
# Original: {'cherry', 'apple', 'banana'}
# dont't keep order: {'cherry', 'apple', 'banana'}
# Keep order: {'cherry', 'apple', 'banana'}
# ---------------
# Set of numbers:
# Original: {1, 2, 3, 4, 5}
# dont't keep order: {1, 2, 3, 4, 5}
# Keep order: {1, 2, 3, 4, 5}
# ---------------
# Tuple of strings:
# Original: ('apple', 'banana', 'cherry', 'banana', 'banana')
# dont't keep order: ('cherry', 'apple', 'banana')
# Keep order: ('apple', 'banana', 'cherry')
# ---------------
# Tuple of numbers:
# Original: (3, 4, 5, 1, 2, 3, 4, 2, 3, 4, 2, 3, 4, 5)
# dont't keep order: (1, 2, 3, 4, 5)
# Keep order: (3, 4, 5, 1, 2)
# ---------------
# Dictionary with numbers:
# Original: {1: 'one', 2: 'two', 3: 'three'}
# dont't keep order: {1: 'one', 2: 'two', 3: 'three'}
# Keep order: {1: 'one', 2: 'two', 3: 'three'}
# ---------------
# Dictionary with strings:
# Original: {'a': 'apple', 'b': 'banana', 'c': 'cherry'}
# dont't keep order: {'a': 'apple', 'b': 'banana', 'c': 'cherry'}
# Keep order: {'a': 'apple', 'b': 'banana', 'c': 'cherry'}
# ---------------
# List of mixed types:
# Original: [1, 'a', 2.5, True, True, True, 1, 'a', 'Hello']
# dont't keep order: [1, 2.5, 'a', 'Hello']
# Keep order: [1, 'a', 2.5, 'Hello']
# ---------------
# Set of mixed types:
# Original: {1, 2.5, 'a', 'Hello'}
# dont't keep order: {1, 2.5, 'a', 'Hello'}
# Keep order: {1, 2.5, 'a', 'Hello'}
# ---------------
# Tuple of mixed types:
# Original: (1, 'a', 2.5, True, 'Hello', 1, 'a', 2.5)
# dont't keep order: (1, 2.5, 'a', 'Hello')
# Keep order: (1, 'a', 2.5, 'Hello')
# ---------------
# Nested list:
# Original: [[1, 2], [3, 4], [5, 6], [1, 2], [3, 4], [3, 4], [5, 6]]
# dont't keep order: [[1, 2], [3, 4], [5, 6]]
# Keep order: [[1, 2], [3, 4], [5, 6]]
# ---------------
# Nested set:
# Original: {frozenset({3, 4}), frozenset({5, 6}), frozenset({1, 2})}
# dont't keep order: {frozenset({3, 4}), frozenset({5, 6}), frozenset({1, 2})}
# Keep order: {frozenset({3, 4}), frozenset({5, 6}), frozenset({1, 2})}
# ---------------
# Nested tuple:
# Original: ((1, 2), (3, 4), (5, 6), (3, 4))
# dont't keep order: ((1, 2), (3, 4), (5, 6))
# Keep order: ((1, 2), (3, 4), (5, 6))
# ---------------
# List with None value:
# Original: [1, None, 3, None, 5]
# dont't keep order: [1, 3, None, 5]
# Keep order: [1, None, 3, 5]
# ---------------
# Set with None value:
# Original: {1, 3, None, 5}
# dont't keep order: {1, 3, None, 5}
# Keep order: {1, 3, None, 5}
# ---------------
# Tuple with None value:
# Original: (1, None, 3, None, 5)
# dont't keep order: (1, 3, None, 5)
# Keep order: (1, None, 3, 5)
# ---------------
# List with boolean values:
# Original: [True, False, True]
# dont't keep order: [False, True]
# Keep order: [True, False]
# ---------------
# Set with boolean values:
# Original: {False, True}
# dont't keep order: {False, True}
# Keep order: {False, True}
# ---------------
# Tuple with boolean values:
# Original: (True, False, True)
# dont't keep order: (False, True)
# Keep order: (True, False)
# ---------------
# List with repeated values:
# Original: [1, 1, 1, 1, 1]
# dont't keep order: [1]
# Keep order: [1]
# ---------------
# Set with repeated values:
# Original: {1}
# dont't keep order: {1}
# Keep order: {1}
# ---------------
# Tuple with repeated values:
# Original: (1, 1, 1, 1, 1)
# dont't keep order: (1,)
# Keep order: (1,)
# ---------------
# List with mixed types and duplicates:
# Original: [1, 'a', 2, 'a', 3, True, 3]
# dont't keep order: [1, 2, 3, 'a']
# Keep order: [True, 'a', 2, 3]
# ---------------
# Set with mixed types and duplicates:
# Original: {1, 2, 3, 'a'}
# dont't keep order: {1, 2, 3, 'a'}
# Keep order: {1, 2, 3, 'a'}
# ---------------
# Tuple with mixed types and duplicates:
# Original: (1, 'a', 2, 'a', 3, True)
# dont't keep order: (1, 2, 3, 'a')
# Keep order: (True, 'a', 2, 3)
# ---------------
# List with empty strings:
# Original: ['', 'World', 'World', 'Hello', 'World']
# dont't keep order: ['', 'World', 'Hello']
# Keep order: ['', 'World', 'Hello']
# ---------------
# Set with empty strings:
# Original: {'', 'World', 'Hello'}
# dont't keep order: {'', 'World', 'Hello'}
# Keep order: {'', 'World', 'Hello'}

```