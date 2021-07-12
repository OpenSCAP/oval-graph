import json
import re
import subprocess
from pathlib import Path

import pexpect
import pytest
from readchar import key

from ..test_tools import TestTools
from .command_constants import ARF_TO_JSON, COMMAND_START, TEST_ARF_XML_PATH


@pytest.mark.usefixtures("remove_generated_reports_in_root")
def test_command_json_to_graph():
    path = str(TestTools.get_random_path_in_tmp()) + '.json'
    out = subprocess.check_output(ARF_TO_JSON)

    with open(path, "w+") as output:
        output.writelines(out.decode('utf-8'))

    command = [*COMMAND_START,
               'json-to-graph',
               '-o', '.',
               path,
               'xccdf_org.ssgproject.content_rule_package_abrt_removed'
               ]
    subprocess.check_call(command, cwd='./')
    file_paths = TestTools.find_files(
        "graph-of-xccdf_org.ssgproject.content_rule_package_abrt_removed",
        '../')
    TestTools.compare_results_html(file_paths[0])


@pytest.mark.usefixtures("remove_generated_reports_in_root")
def test_command_json_to_graph_with_verbose():
    path = str(TestTools.get_random_path_in_tmp()) + '.json'
    out = subprocess.check_output(ARF_TO_JSON)
    with open(path, "w+") as output:
        output.writelines(out.decode('utf-8'))

    command = [*COMMAND_START,
               'json-to-graph',
               '-o', '.',
               '--verbose',
               path,
               'xccdf_org.ssgproject.content_rule_package_abrt_removed'
               ]
    out = subprocess.check_output(command,
                                  cwd='./',
                                  stderr=subprocess.STDOUT)
    path_regex = r"\"(.*?)\"$"
    path_search = re.search(path_regex, out.decode('utf-8')).group(1)
    file_path = Path(__file__).parent.parent.parent / path_search
    TestTools.compare_results_html(file_path)


def test_command_json_to_graph_is_tty():
    path = str(TestTools.get_random_path_in_tmp()) + '.json'
    with open(path, 'w+') as output:
        subprocess.check_call(ARF_TO_JSON, stdout=output)

    out_path = TestTools.get_random_path_in_tmp()
    commad = [*COMMAND_START,
              'json-to-graph',
              '--out',
              str(out_path),
              str(path),
              'xccdf_org.ssgproject.content_rule_package_abrt_removed'
              ]
    subprocess.check_output(commad)

    TestTools.compare_results_html(out_path)


def test_inquirer_choice_rule():
    pytest.importorskip("inquirer")
    path = str(TestTools.get_random_path_in_tmp()) + '.json'
    args = ['-m',
            'oval_graph.command_line',
            'arf-to-json',
            TEST_ARF_XML_PATH,
            r'_package_\w+_removed'
            ]

    sut = pexpect.spawn('python3', args)
    sut.expect(r'\w+')
    keys = [key.DOWN, key.SPACE, key.UP, key.SPACE, key.ENTER]
    for key_ in keys:
        sut.send(key_)
    sut.wait()
    out = sut.readlines()

    with open(path, "w+") as output:
        output.writelines(row.decode("utf-8") for row in out[20:])
    TestTools.compare_results_json(path)

    out_path = TestTools.get_random_path_in_tmp()
    args = [*COMMAND_START,
            'json-to-graph',
            '-o',
            str(out_path),
            path,
            '.'
            ]
    args.remove("python3")

    sut = pexpect.spawn('python3', args)
    sut.expect(r'\w+')
    keys = [key.DOWN, key.SPACE, key.ENTER]
    for key_ in keys:
        sut.send(key_)
    sut.wait()
    assert out_path.is_file()


def test_command_parameter_all():
    path = str(TestTools.get_random_path_in_tmp()) + '.json'
    command = [*COMMAND_START,
               'arf-to-json',
               '--all',
               TEST_ARF_XML_PATH,
               '.'
               ]
    with open(path, 'w+') as output:
        subprocess.check_call(command, stdout=output)

    with open(path, "r") as data:
        rules = json.load(data)
    assert len(rules.keys()) == 184
    out_path = TestTools.get_random_path_in_tmp()
    command = [*COMMAND_START,
               'json-to-graph',
               path,
               '.',
               '--all',
               '-o',
               str(out_path)
               ]
    subprocess.check_call(command)
    assert len(list(out_path.glob('**/*.html'))) == 184
