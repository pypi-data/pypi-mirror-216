# from pipeable import select, ITer
from enumerable import Iter

# print(list(range(10) | select(lambda x: x ** 2)))
iter = Iter[int](list(range(10)))

print(iter.map(lambda x: x ** 2).to_list().iter().map(lambda x: x + 2).collect(list))
print(iter.map(lambda x: x ** 2).map(lambda x: x + 1).collect(list))
print(iter.map(lambda x: x * 2).to_collection().__reversed__().collect(list))
print(iter.map(lambda x: x ** 2).to_list())