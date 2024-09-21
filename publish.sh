#!/bin/bash
set -euxo pipefail

auto=false

if [ -z "${1:-}" ]; then
    echo "Commit message or -a"
    exit 1
fi

if [ "${1}" = '-a' ]; then
    auto=true
fi

rm -rf docs output
cp assets/favicon-prd.ico assets/favicon.ico
jbake . docs
git add .
if [ "$auto" = 'true' ]; then
    git commit -m 'Update chords'
else
    git commit -m "$1"
fi
git push