#!/bin/bash

for f in rdf_unquoted/*.nt 
do
    echo $f >> triples_check.log
    riot -v --validate $f >> triples_check.log 2>> triples_check.log
done
