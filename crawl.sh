#!/bin/bash

MYDIR=$(dirname $0)
mkdir $MYDIR/out 2>/dev/null
rm -f $MYDIR/out/crawl.log $MYDIR/out/crawl.csv
scrapy crawl \
  -O $MYDIR/out/crawl.csv \
  -a download_path=$MYDIR/out media 2>&1 | tee $MYDIR/out/crawl.log
