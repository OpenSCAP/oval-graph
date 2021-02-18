#!/usr/bin/env bash
# Test script for testing command entry points

name="oval-graph"
test_file_src="./tests/test_data/ssg-fedora-ds-arf.xml"
tmp_dir_src="./tmp_data"
tmp_json_file_src="${tmp_dir_src}/data.json"

test_result=0
overall_test_result=0

usage() {
    cat <<EOF
usage: bash ./test_commands.sh
-c    | --clean                  Removes created files
-v    | --verbose                Displays details about the tests
-io   | --install-oval-graph     Install oval-graph from source
-h    | --help                   Brings up this menu
EOF
}

clean=false
verbose=false
oval_graph_install=false

for arg in "$@"; do
    case $arg in
    -c | --clean)
        shift
        clean=true
        ;;
    -v | --verbose)
        shift
        verbose=true
        ;;
    -io | --install-oval-graph)
        shift
        oval_graph_install=true
        ;;
    -h | --help)
        usage
        exit
        ;;
    *)
        echo "Unknown argument ->${arg}<-"
        exit 1
        ;;
    esac
done

test_if_is_instaled_oval_graph() {
    rpm -q $name >/dev/null 2>&1
    is_rpm_installed=$?
    pip list | grep -F $name
    is_pip_package_installed=$?
    if [ ! $is_rpm_installed ] || [ ! $is_pip_package_installed ]; then
        echo "$name NOT installed"
        exit 1
    fi
}

install_package_from_source() {
    install_pip="pip install --upgrade pip"
    install_oval_graph="pip install -e ."

    if [ $verbose = true ]; then
        echo "Start install"
        $install_pip
        $install_oval_graph
        echo "End install"
    else
        $install_pip &>/dev/null
        $install_oval_graph &>/dev/null
    fi
}

report() {
    if [ $verbose = true ]; then
        if [ $test_result -eq 0 ]; then
            printf "Result: %-70s \x1b[32mpassed\x1b[0m\n" "$*"
        else
            printf "Result: %-70s \x1b[31mfailed\x1b[0m\n\n" "$*"
        fi
    fi
}

test() {
    test_name="$1"
    command="$2"
    msg=""
    if [ $verbose = true ]; then
        echo "Start: $test_name"
        $command
    else
        $command &>/dev/null
    fi
    if [ $? -eq 0 ]; then
        test_result=0
        msg="$test_name"
    else
        test_result=1
        overall_test_result=1
        msg="$test_name: $command"
    fi
    report "${msg}"
}

test_rise_error() {
    test_name="$1"
    command="$2"
    msg=""
    if [ $verbose = true ]; then
        echo "Start: $test_name"
        $command
    else
        $command &>/dev/null
    fi
    if [ $? -eq 2 ]; then
        test_result=0
        msg="$test_name"
    else
        test_result=1
        overall_test_result=1
        msg="$test_name: $command"
    fi
    report "${msg}"
}

clean() {
    file=$1
    if [ $verbose = true ]; then
        echo "remove ${file}"
    fi
    rm -rf "${file}"
}

help_tests() {
    test arf-to-graph-help "arf-to-graph -h"
    test arf-to-json-help "arf-to-json -h"
    test json-to-graph-help "json-to-graph -h"
}

bad_args_tests() {
    test_rise_error arf-to-graph-bad_arg "arf-to-graph -hello"
    test_rise_error arf-to-json-bad_arg "arf-to-json -hello"
    test_rise_error json-to-graph-bad_arg "json-to-graph -hello"
}

basic_test() {
    test run-arf-to-graph "arf-to-graph -o ${tmp_dir_src} ${test_file_src} fips"
    clean "${tmp_json_file_src}"
    test run-arf-to-json "arf-to-json -o ${tmp_json_file_src} ${test_file_src} fips"
    test run-json-to-graph "json-to-graph -o ${tmp_dir_src} ${tmp_json_file_src} fips"
}

if [ $oval_graph_install = true ]; then
    install_package_from_source
fi

test_if_is_instaled_oval_graph
help_tests
bad_args_tests
basic_test

if [ $clean = true ]; then
    clean "${tmp_dir_src}"
fi
exit "$overall_test_result"
