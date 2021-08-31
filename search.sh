#!/bin/bash

#cat ./queries.txt | while read query;
# do
##   echo $query
#  python src/search.py ./indexes $query
#done
python src/search.py ./indexes "$2"
