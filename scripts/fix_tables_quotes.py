import os
from os import listdir
from os.path import isfile, join

table_folder = "./table/csv"
output_folder = "./table_fixed"
table_files = [f for f in listdir(table_folder) if isfile(join(table_folder, f))]

for _file in table_files:
    f = open(join(table_folder, _file))
    output = open(join(output_folder, _file), "w")
    
    for line in f.readlines():
        entries = line.split('","')
        for num, entry in enumerate(entries):
            entries[num] = entry.replace('"',"").strip()
        csv_string = '"' + '","'.join(entries) + '"'
        output.write(csv_string)
    f.close()
    output.close()
