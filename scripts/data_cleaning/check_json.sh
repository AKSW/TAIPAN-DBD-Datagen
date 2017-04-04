#!/bin/bash

for f in metadata/* 
do
    echo $f >> json_check.log
    jsonlint-cli $f >> json_check.log
done
