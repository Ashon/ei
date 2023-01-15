#!/bin/bash

set -euo pipefail

option=$1

# Read version
VERSION_PATH="ei/__about__.py"
VERSION_STR=$(python -c 'from ei.__about__ import VERSION; print(VERSION)')
VERSION=(${VERSION_STR//./ })

MAJOR="${VERSION[0]}"
MINOR="${VERSION[1]}"
PATCH="${VERSION[2]}"

echo "Make new release from $VERSION_STR (up $option version)"

if [ $option = 'major' ]; then
  MAJOR=$(($MAJOR + 1))
  MINOR=0
  PATCH=0

elif [ $option = 'minor' ]; then
  MINOR=$(($MINOR + 1))
  PATCH=0

elif [ $option = 'patch' ]; then
  PATCH=$(($PATCH + 1))

else
  exit 1

fi

NEW_VERSION="$MAJOR.$MINOR.$PATCH"
echo "New release is created $NEW_VERSION"

# Write new version, commit
echo "VERSION = '${NEW_VERSION}'" > $VERSION_PATH
git add $VERSION_PATH
git commit -am "Release $NEW_VERSION"
git tag $NEW_VERSION

echo "New release tag is created $NEW_VERSION"
echo "Push to main repository (tag: $NEW_VERSION)"
git push origin master $NEW_VERSION
echo "Done"

exit 0
