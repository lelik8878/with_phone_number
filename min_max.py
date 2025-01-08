
def func1():
    return 1

def func2():
    yield 2
    yield 3
    yield 4

new_gen = func2()

print(func1)
print(func2)
print(func1())
print(func2())
print(next(new_gen))
print(next(new_gen))
print(next(new_gen))
