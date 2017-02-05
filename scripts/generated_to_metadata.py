import json
import os

from opentablebench.RDFQuery import get_label

ids = json.load(open("table/list"))

for _id in ids:
    if os.path.exists("metadata/"+_id):
        continue
    _class_file = open("generated/classes/"+_id+".csv")
    _class = _class_file.read()
    _class_uri = _class.split(",")[2].replace('"','')
    _class_label = _class.split(",")[1].replace('"','')
    _properties_file = open("generated/properties/"+_id+".csv")
    properties = []
    for _property in _properties_file.readlines():
        _property_uri = _property.split(",")[0].replace('"','')
        _property_col = int(_property.split(",")[3].replace('"','').replace("\n",""))
        _property_label = get_label(_property_uri)
        properties.append({"label":_property_label,"URI":_property_uri,"column":_property_col})
    _sc_file = open("generated/subject_columns/"+_id+".csv")
    _sc = _sc_file.read()
    _sc = int(_sc.split(",")[1].replace('"',''))
    json_struct = {
        "class": {"label":_class_label,"URI":_class_uri},
        "properties": properties,
        "subject_column": _sc
    }
    json_string = json.dumps(json_struct)
    f = open("metadata/"+_id, "w")
    f.write(json_string)
    f.close()
