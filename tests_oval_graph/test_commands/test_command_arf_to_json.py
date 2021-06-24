import json
import subprocess
import time

import pexpect
from readchar import key

from ..test_tools import TestTools

START_OF_COMMAND = ['python3',
                    '-m',
                    'oval_graph.command_line',
                    'arf-to-json',
                    ]

BASE_COMMAND = [*START_OF_COMMAND,
                'tests_oval_graph/global_test_data/ssg-fedora-ds-arf.xml',
                'xccdf_org.ssgproject.content_rule_package_abrt_removed'
                ]


def run_commad_and_save_output_to_file(parameters):
    src = TestTools.get_random_dir_in_tmp() + '.json'
    with open(src, 'w+') as output:
        subprocess.check_call(parameters, stdout=output)
    return src


def test_command_arf_to_json():
    src = TestTools.get_random_dir_in_tmp() + '.json'
    out = subprocess.check_output(BASE_COMMAND)
    with open(src, "w+") as data:
        data.writelines(out.decode('utf-8'))
    TestTools.compare_results_json(src)


def test_command_arf_to_json_is_tty():
    src = run_commad_and_save_output_to_file(BASE_COMMAND)
    TestTools.compare_results_json(src)


def test_inquirer_choice_rule():
    src = TestTools.get_random_dir_in_tmp() + '.json'

    command_parameters = [*BASE_COMMAND]
    command_parameters.remove("python3")
    command_parameters.remove('xccdf_org.ssgproject.content_rule_package_abrt_removed')
    command_parameters.append(r'_package_\w+_removed')
    sut = pexpect.spawn('python3', command_parameters)

    sut.expect(r'\w+')
    keys = [key.DOWN, key.SPACE, key.SPACE, key.UP, key.SPACE, key.ENTER]
    for key_ in keys:
        sut.send(key_)
    sut.wait()
    out = sut.readlines()
    with open(src, "w+") as data:
        data.writelines(row.decode("utf-8") for row in out[24:])
    TestTools.compare_results_json(src)


def test_command_parameter_all():
    command = [*START_OF_COMMAND,
               '--all',
               'tests_oval_graph/global_test_data/ssg-fedora-ds-arf.xml',
               '.'
               ]
    src = run_commad_and_save_output_to_file(command)
    with open(src, "r") as data:
        rules = json.load(data)
    assert len(rules.keys()) == 184


def test_command_parameter_all_and_show_failed_rules():
    command = [*START_OF_COMMAND,
               '--all',
               '--show-failed-rules',
               'tests_oval_graph/global_test_data/ssg-fedora-ds-arf.xml',
               r'_package_\w+_removed'
               ]
    src = run_commad_and_save_output_to_file(command)
    with open(src, "r") as data:
        rules = json.load(data)
    assert len(rules.keys()) == 1


def test_command_with_parameter_out():
    command = [*START_OF_COMMAND,
               '--all',
               'tests_oval_graph/global_test_data/ssg-fedora-ds-arf.xml',
               r'_package_\w+_removed'
               ]
    src = run_commad_and_save_output_to_file(command)

    time.sleep(5)

    command.append('-o' + src)
    subprocess.check_call(command)

    with open(src, "r") as data:
        rules = json.load(data)
    assert len(rules.keys()) == 4
