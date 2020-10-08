#!/bin/sh
# Build script of python package

set -e
name="oval-graph"
module="oval_graph"

unit_test() {
    python3 -m pytest
}

commit_version() {
    version=$1
    module=$2
    git add ${module}/__init__.py
    git add oval-graph.spec
    git commit -m "${version}"
}

install_build_requirements() {
    python3 -m pip install --user --upgrade setuptools wheel twine
}

build_backage() {
    rm -rf dist
    python3 setup.py sdist bdist_wheel
}

update_version_package() {
    module=$1
    old_version=$2
    new_version=$3
    sed -i "s/$old_version/$new_version/g" ${module}/__init__.py
}

update_version_rpm() {
    version=$1
    name=$2
    rpmdev-bumpspec "${name}".spec --comment="release ${version}" -n "${version}" --userstring="Jan Rodak <jrodak@redhat.com>"
}

load_upstream() {
    git checkout master
    git pull upstream master
}

if [ "$1" = "" ]; then
    echo "Missing version parameter!"
    exit 1
fi
    
new_version=$1

if ! echo "$new_version" | grep -q -E '^[0-9]{1,}.[0-9]{1,}.[0-9]{1,}$'; then
    echo "Bad version format!"
    exit 1
fi

if git status --porcelain=v1 | grep -q '^\(.M\|M.\)'; then
    echo "Not commited changes!"
    exit 1
fi

load_upstream

# Update version in file
old_version=$(python3 setup.py --version)
update_version_package "$module" "$old_version" "$new_version" 
version=$(python3 setup.py --version)
update_version_rpm "$version" "$name"

# Prepare build tools
install_build_requirements

# Test before build
unit_test

# Build
build_backage

# Upload to PyPi
twine upload dist/*

# Commit version
commit_version "$version" "$module"

# Tag version and upload to git repo
./tag_version.sh "${version}"

