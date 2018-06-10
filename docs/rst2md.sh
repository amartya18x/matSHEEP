#!/bin/sh
cd ../
FILES=*.txt
for f in $FILES
do
  filename="${f%.*}"
  echo "Converting $f to $filename.md"
  `pandoc $f -f rst -t markdown -o docs/$filename.md`
done
pwd
cd docs
`mv README.md index.md`
