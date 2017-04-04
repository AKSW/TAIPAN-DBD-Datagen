#!/bin/bash

for f in table/csv_fixed/* 
do
    echo $f >> check_tables.log
    csvlint $f >> check_tables.log
done
