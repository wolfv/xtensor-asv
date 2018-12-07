#!/bin/sh
while read p; do
  asv run $p
done < $1
