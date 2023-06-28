#!/bin/bash

for i in {1..64}
do
    pattern=",$i"
    count=$(cat "$1" | grep -c "$pattern")
    echo "$i,$count"
done

