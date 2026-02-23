class MyIterator:
    def __init__(self, max_value):
        self.max_value = max_value
        self.current_value = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_value < self.max_value:
            self.current_value += 1
            return self.current_value
        else:
            raise StopIteration

my_iters = MyIterator(5)
for i in my_iters:
    print(i)

my_list = [1, 2, 3, 4, 5]
for item in my_list:
    print(item)


