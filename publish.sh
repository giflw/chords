#!/bin/bash

auto=false

if [ "$1" = '-a' ]; then
    auto=true
fi

rm -rf docs output
jbake . docs
git add .
if [ "$auto" = 'true' ]; then
    git commit -m 'Update chords'
else
    git commit
fi
git push