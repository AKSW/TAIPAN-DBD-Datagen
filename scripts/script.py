import sys

f = open(sys.argv[1])

for _num, line in enumerate(f.readlines()):
    if _num == 0:
        header_list = eval(eval(line))[0]
        header_string = '"' + '","'.join(header_list) + '"'
        print(header_string, end="\n")
    else:
        print(line, end="")

