#!/bin/bash

#
# This bash script remove header items by the stop list PATTERNS
# and clean up the log file to contain only arrays of string
# one per line
#

LOG_FILENAME="log.out"
PATTERNS[1]="u'Wikipage revision ID'" 
PATTERNS[2]="u'Wikipage page ID'" 
PATTERNS[3]="u'sameAs'" 
PATTERNS[4]="u'Link from a Wikipage to an external page'" 
PATTERNS[5]="u'isPrimaryTopicOf'" 
PATTERNS[6]="u'wasDerivedFrom'" 
PATTERNS[7]="u'Wikipage disambiguates'"

ARRAY_LENGTH=${#PATTERNS[@]}
for i in $(seq 1 ${#PATTERNS[@]})
do
  PATTERN=${PATTERNS[$i]}
  PATTERN_IN_MIDDLE="s#$PATTERN, ##g"
  sed -i -e "$PATTERN_IN_MIDDLE" $LOG_FILENAME
  PATTERN_IN_END="s#, $PATTERN##g"
  sed -i -e "$PATTERN_IN_END" $LOG_FILENAME
done

#Remove everything until [ - start of an array
sed -i -e "s/.*\[/\[/g" $LOG_FILENAME
#Remove lines which are not an array
sed -i '/^[0-9]/ d' $LOG_FILENAME
