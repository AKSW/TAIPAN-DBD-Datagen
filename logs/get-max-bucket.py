#!/home/ivan/.virtualenvs/tablegen/bin/python3

f = open("headers_buckets", "r")
max_n = 0
max_size = 0
for i, line in enumerate(f.readlines()):
    if (2 + i % 3) == 3:
        _list = eval(line.strip())
        _n = sum(_list)
        if _n > max_n:
            max_n = _n
        _size = len(_list)
        if _size > max_size:
            max_size = _size

print(max_n)
print(max_size)
