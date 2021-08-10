import json
import os
import re
import subprocess
from pathlib import Path

import pexpect
import pytest
from readchar import key

from ..test_tools import TestTools
from .command_constants import ARF_TO_JSON, COMMAND_START, TEST_ARF_XML_PATCH


@pytest.mark.usefixtures("remove_generated_reports_in_root")
def test_command_json_to_graph():
    src = TestTools.get_random_dir_in_tmp() + '.json'
    out = subprocess.check_output(ARF_TO_JSON)

    with open(src, "w+") as output:
        output.writelines(out.decode('utf-8'))

    command = [*COMMAND_START,
               'json-to-graph',
               '-o', '.',
               src,
               'xccdf_org.ssgproject.content_rule_package_abrt_removed'
               ]
    subprocess.check_call(command, cwd='./')
    file_src = TestTools.find_files(
        "graph-of-xccdf_org.ssgproject.content_rule_package_abrt_removed",
        '../')
    TestTools.compare_results_html(file_src[0])


@pytest.mark.usefixtures("remove_generated_reports_in_root")
def test_command_json_to_graph_with_verbose():
    src = TestTools.get_random_dir_in_tmp() + '.json'
    out = subprocess.check_output(ARF_TO_JSON)
    with open(src, "w+") as output:
        output.writelines(out.decode('utf-8'))

    command = [*COMMAND_START,
               'json-to-graph',
               '-o', '.',
               '--verbose',
               src,
               'xccdf_org.ssgproject.content_rule_package_abrt_removed'
               ]
    out = subprocess.check_output(command,
                                  cwd='./',
                                  stderr=subprocess.STDOUT)
    src_regex = r"\"(.*?)\"$"
    src = re.search(src_regex, out.decode('utf-8')).group(1)
    file_src = Path(__file__).parent.parent.parent / src
    TestTools.compare_results_html(file_src)


def test_command_json_to_graph_is_tty():
    src = TestTools.get_random_dir_in_tmp() + '.json'
    with open(src, 'w+') as output:
        subprocess.check_call(ARF_TO_JSON, stdout=output)

    out_dir = TestTools.get_random_dir_in_tmp()
    commad = [*COMMAND_START,
              'json-to-graph',
              '--out',
              out_dir,
              src,
              'xccdf_org.ssgproject.content_rule_package_abrt_removed'
              ]
    subprocess.check_output(commad)

    TestTools.compare_results_html(out_dir)


def test_inquirer_choice_rule():
    src = TestTools.get_random_dir_in_tmp() + '.json'
    args = ['-m',
            'oval_graph.command_line',
            'arf-to-json',
            TEST_ARF_XML_PATCH,
            r'_package_\w+_removed'
            ]

    sut = pexpect.spawn('python3', args)
    sut.expect(r'\w+')
    keys = [key.DOWN, key.SPACE, key.UP, key.SPACE, key.ENTER]
    for key_ in keys:
        sut.send(key_)
    sut.wait()
    out = sut.readlines()

    with open(src, "w+") as output:
        output.writelines(row.decode("utf-8") for row in out[20:])
    TestTools.compare_results_json(src)

    out_dir = TestTools.get_random_dir_in_tmp()
    args = [*COMMAND_START,
            'json-to-graph',
            '-o',
            out_dir,
            src,
            '.'
            ]
    args.remove("python3")

    sut = pexpect.spawn('python3', args)
    sut.expect(r'\w+')
    keys = [key.DOWN, key.SPACE, key.ENTER]
    for key_ in keys:
        sut.send(key_)
    sut.wait()
    assert os.path.isfile(out_dir)


def test_command_parameter_all():
    src = TestTools.get_random_dir_in_tmp() + '.json'
    command = [*COMMAND_START,
               'arf-to-json',
               '--all',
               TEST_ARF_XML_PATCH,
               '.'
               ]
    with open(src, 'w+') as output:
        subprocess.check_call(command, stdout=output)

    with open(src, "r") as data:
        rules = json.load(data)
    assert len(rules.keys()) == 184
    out_dir = TestTools.get_random_dir_in_tmp()
    command = [*COMMAND_START,
               'json-to-graph',
               src,
               '.',
               '--all',
               '-o',
               out_dir
               ]
    subprocess.check_call(command)
    assert len(os.listdir(out_dir)) == 184
