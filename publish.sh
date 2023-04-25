#!/bin/bash

rm -r docs output
jbake . docs
git add .
git commit
git push