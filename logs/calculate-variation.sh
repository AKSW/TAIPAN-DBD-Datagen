#!/bin/bash

#
# This script takes verbalization.log, remove blank lines and u symbol before '
# Then it will split it into two files (odd and even lines) and perform diff
#

LOG_FILENAME=$1
LOG_FILENAME_CLEANED="verbalization.log.cleaned"
LOG_FILENAME_BEFORE="verbalization.log.before"
LOG_FILENAME_AFTER="verbalization.log.after"

cp $LOG_FILENAME $LOG_FILENAME_CLEANED

sed -i -e "s/u'/'/g" $LOG_FILENAME_CLEANED
sed -i -e "/^\s*$/d" $LOG_FILENAME_CLEANED
awk '0 == (NR) % 2' $LOG_FILENAME_CLEANED > $LOG_FILENAME_BEFORE
awk '0 == (NR + 1) % 2' $LOG_FILENAME_CLEANED > $LOG_FILENAME_AFTER
DIFFERENT_LINES=$(diff -y --suppress-common-lines $LOG_FILENAME_BEFORE $LOG_FILENAME_AFTER | grep "^" | tail -n +3 | wc -l)
TOTAL_LINES=$(cat $LOG_FILENAME_BEFORE | wc -l)
echo "DIFFERENT_LINES: $DIFFERENT_LINES"
echo "TOTAL_LINES: $TOTAL_LINES"
rm $LOG_FILENAME_CLEANED $LOG_FILENAME_BEFORE $LOG_FILENAME_AFTER

#
# Run this for the view on differences between logs:
# diff -y --suppress-common-lines $LOG_FILENAME_BEFORE $LOG_FILENAME_AFTER | grep "^" | tail -n +3
#
