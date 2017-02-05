#!/bin/bash

#for f in table/csv/*.csv 
for f in table_fixed/*.csv 
do
    echo $f
    ./csvlint-v0.2.0-linux-amd64/csvlint $f
done
