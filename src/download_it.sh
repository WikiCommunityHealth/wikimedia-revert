#!/bin/bash

FROM=2001
TO=2021


for YEAR in $(seq $FROM $TO);
do    
    echo "Downloading..."
    curl https://dumps.wikimedia.org/other/mediawiki_history/2021-01/itwiki/2021-01.itwiki."${YEAR}".tsv.bz2 --output it"${YEAR}".tsv.bz2
    echo -e "Downloaded $YEAR\n"
done
