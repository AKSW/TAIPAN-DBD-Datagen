#!/bin/bash
input="./arg_list"
while IFS= read -r var
do
  fn=$(echo $var | sed -e 's#^.*/##g')
  sed 's/>"/> "/g' $var > triples_fixed/$fn
done < "$input"
