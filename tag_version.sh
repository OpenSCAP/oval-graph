#!/bin/sh
# Script for tag version of python package and push to git repo

set -e

version=$1

git tag "${version}"
git push --follow-tags
git push upstream master
