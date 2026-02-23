def fib(n):
    n_1, n_2 = 1, 1
    for i in range(n):
        yield n_1
        n_1, n_2 = n_2, n_1 + n_2

print(", ".join(str(x) for x in fib(10)))

def f_gen(m):
    s = 1
    for n in range(1,m):
        yield n**2 + s
        s += 1

a = f_gen(5)
for i in a:
    print(i)