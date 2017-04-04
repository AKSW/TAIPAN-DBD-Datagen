#!/bin/bash

for f in $(find . -type fls); do tail -n1 $f | read -r _ || echo >> $f; done
