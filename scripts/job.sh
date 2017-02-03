#!/bin/bash
input="./arg_list"
while IFS= read -r var
do
  fn=$(echo $var | sed -e 's#^.*/##g')
  python script.py "$var" > tables_fixed/$fn
done < "$input"
