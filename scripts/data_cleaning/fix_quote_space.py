import os
from os import listdir
from os.path import isfile, join

triples_folder = "./rdf"
output_folder = "./rdf_fixed"
triple_files = [f for f in listdir(triples_folder) if isfile(join(triples_folder, f))]

for _file in triple_files:
    f = open(join(triples_folder, _file))
    output = open(join(output_folder, _file), "w")
    
    for line in f.readlines():
        try:
            line = line.split(">\"")
            line = "> \"".join(line)
            output.write(line)
        except:
            pass
    f.close()
    output.close()
