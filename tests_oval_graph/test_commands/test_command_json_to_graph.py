import json
import os
import re
import subprocess

import pexpect
import pytest
from readchar import key

from ..test_tools import TestTools
from .test_command_arf_to_json import BASE_COMMAND as COMMAND_ARF_TO_JSON

START_OF_COMMAND = ['python3',
                    '-m',
                    'oval_graph.command_line',
                    'json-to-graph',
                    ]


@pytest.mark.usefixtures("remove_generated_reports_in_root")
def test_command_json_to_graph():
    src = TestTools.get_random_dir_in_tmp() + '.json'
    out = subprocess.check_output(COMMAND_ARF_TO_JSON)

    with open(src, "w+") as output:
        output.writelines(out.decode('utf-8'))

    command = [*START_OF_COMMAND,
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
    out = subprocess.check_output(COMMAND_ARF_TO_JSON)
    with open(src, "w+") as output:
        output.writelines(out.decode('utf-8'))

    command = [*START_OF_COMMAND,
               '-o', '.',
               '--verbose',
               src,
               'xccdf_org.ssgproject.content_rule_package_abrt_removed'
               ]
    out = subprocess.check_output(command,
                                  cwd='./',
                                  stderr=subprocess.STDOUT)
    src_regex = r"\"(\.\/.*?)\""
    src = re.search(src_regex, out.decode('utf-8')).group(1)
    file_src = '.{}'.format(src)
    TestTools.compare_results_html(file_src)


def test_command_json_to_graph_is_tty():
    src = TestTools.get_random_dir_in_tmp() + '.json'
    with open(src, 'w+') as output:
        subprocess.check_call(COMMAND_ARF_TO_JSON, stdout=output)

    out_dir = TestTools.get_random_dir_in_tmp()
    commad = [*START_OF_COMMAND,
              '--out',
              out_dir,
              src,
              'xccdf_org.ssgproject.content_rule_package_abrt_removed'
              ]
    subprocess.check_output(commad)

    file_src = os.path.join(out_dir, os.listdir(out_dir)[0])
    TestTools.compare_results_html(file_src)


def test_inquirer_choice_rule():
    src = TestTools.get_random_dir_in_tmp() + '.json'
    args = ['-m',
            'oval_graph.command_line',
            'arf-to-json',
            'tests_oval_graph/global_test_data/ssg-fedora-ds-arf.xml',
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
    args = [*START_OF_COMMAND,
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
    assert len(os.listdir(out_dir)) == 1
    assert ("xccdf_org.ssgproject.content_rule_package_abrt_removed"
            in os.listdir(out_dir)[0])


def test_command_parameter_all():
    src = TestTools.get_random_dir_in_tmp() + '.json'
    command = ['python3',
               '-m',
               'oval_graph.command_line',
               'arf-to-json',
               '--all',
               'tests_oval_graph/global_test_data/ssg-fedora-ds-arf.xml',
               '.'
               ]
    with open(src, 'w+') as output:
        subprocess.check_call(command, stdout=output)

    with open(src, "r") as data:
        rules = json.load(data)
    assert len(rules.keys()) == 184
    out_dir = TestTools.get_random_dir_in_tmp()
    command = [*START_OF_COMMAND,
               src,
               '.',
               '--all',
               '-o',
               out_dir
               ]
    subprocess.check_call(command)
    assert len(os.listdir(out_dir)) == 184
