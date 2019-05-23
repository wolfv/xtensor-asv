#!/bin/sh
while read p; do
  echo "Running $p"
  asv run $p -v
done < $1
