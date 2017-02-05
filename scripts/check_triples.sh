#!/bin/bash

for f in triples_unquoted/*.nt 
do
    echo $f
    ./apache-jena-3.1.1/bin/riot -v --validate $f >> triples_check.log
done
