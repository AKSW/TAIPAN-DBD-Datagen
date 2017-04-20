import os
import json

from os.path import exists

server_list = ["server-0", "server-30", "server-50"]

for server_id in server_list:
    id_list_file = os.path.join(server_id, "table", "list")
    id_list = open(id_list_file, 'rU')
    id_list = json.loads(id_list.read())
    for _id in id_list:
         table_file = os.path.join(server_id, "table", "csv", "%s.csv" % (_id,))
         metadata_file = os.path.join(server_id, "metadata", "%s" % (_id,))
         triples_file = os.path.join(server_id, "triples", "%s.nt" % (_id,))
         if not exists(table_file):
             print("Table does not exist %s" % (_id,))
         if not exists(metadata_file):
             print("Metadata does not exist %s" % (_id,))
         if not exists(triples_file):
             print("RDF does not exist %s" % (_id,))

