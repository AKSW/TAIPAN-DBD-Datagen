import os
from os import listdir
from os.path import isfile, join

triples_folder = "./triples_fixed"
output_folder = "./triples_unquoted"
triple_files = [f for f in listdir(triples_folder) if isfile(join(triples_folder, f))]

for _file in triple_files:
    f = open(join(triples_folder, _file))
    output = open(join(output_folder, _file), "w")
    
    for line in f.readlines():
        try:
            _subject = line.split(" ")[0]
            _predicate = line.split(" ")[1]
            _object = line.split(" ")[2:-1]
            if len(_object) == 1:
                _object = _object[0]
                if not _object.startswith("<"):
                    _object = _object.replace('"',"")
                    _object = '"%s"' % (_object,)
            else:
                _object = " ".join(_object).replace('"',"")
                _object = '"%s"' % (_object,)
            triple = "%s %s %s .\n" % (_subject, _predicate, _object)
            output.write(triple)
        except:
            pass
    f.close()
    output.close()
