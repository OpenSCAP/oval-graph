set -e 
name="oval-graph"
module="oval_graph"

if [ "$1" != "" ]; then
    new_version=$1
    if [[ $new_version =~ ^[0-9]{1,}.[0-9]{1,}.[0-9]{1,}$ ]]; then
        old_version=$(python3 setup.py --version)
        git checkout master
        git pull upstream master
        git status --porcelain=v1 | grep -q '^\(.M\|M.\)'
        status=$?
        if [$status -eq 1];then
            # update version in file
            sed -i 's/${old_version}/${new_version}/g' ${module}/__init__.py
            if [$(python3 setup.py --version) == $new_version]; then
                # Commit version
                git add ${module}/__init__.py
                git commit -m "${version}"
                git tag "${version}"
                git push --follow-tags
                git push upstream master
                # Build  
                rm -rf dist
                python3 setup.py pytest sdist bdist_wheel
                twine upload dist/*
            fi
        fi
    else
        echo "Bad version format!"
    fi
    else 
        echo "Missing version parameter!"
fi
