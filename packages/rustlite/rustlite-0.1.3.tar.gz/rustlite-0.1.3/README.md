# Better iterators for python (all typed)

## Examples

### simple

```python
## create iterator for even integers squared
even_integers = Iter[int](range(100)) \
    .filter(lambda x: x % 2 == 0) \
    .map(lambda x: x ** 2)

## to evaluate into a list use
basic_list = even_integers.collect(list)
smart_list = even_integers.to_list()

## The smart list will allow the usage of iterator notation again by
times2_iter = smart_list.iter() \
    .map(lambda x: x * 2)
```
