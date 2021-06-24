import json
import subprocess
import time

import pexpect
from readchar import key

from ..test_tools import TestTools
from .command_constants import ARF_TO_JSON, COMMAND_START, TEST_ARF_XML_PATH


def run_commad_and_save_output_to_file(parameters):
    path = str(TestTools.get_random_path_in_tmp()) + '.json'
    with open(path, 'w+') as output:
        subprocess.check_call(parameters, stdout=output)
    return path


def test_command_arf_to_json():
    path = str(TestTools.get_random_path_in_tmp()) + '.json'
    out = subprocess.check_output(ARF_TO_JSON)
    with open(path, "w+") as data:
        data.writelines(out.decode('utf-8'))
    TestTools.compare_results_json(path)


def test_command_arf_to_json_is_tty():
    src = run_commad_and_save_output_to_file(ARF_TO_JSON)
    TestTools.compare_results_json(src)


def test_inquirer_choice_rule():
    path = str(TestTools.get_random_path_in_tmp()) + '.json'

    command_parameters = [*ARF_TO_JSON]
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
    with open(path, "w+") as data:
        data.writelines(row.decode("utf-8") for row in out[24:])
    TestTools.compare_results_json(path)


def test_command_parameter_all():
    command = [*COMMAND_START,
               "arf-to-json",
               "--all",
               TEST_ARF_XML_PATH,
               ".",
               ]
    src = run_commad_and_save_output_to_file(command)
    with open(src, "r") as data:
        rules = json.load(data)
    assert len(rules.keys()) == 184


def test_command_parameter_all_and_show_failed_rules():
    command = [*COMMAND_START,
               'arf-to-json',
               '--all',
               '--show-failed-rules',
               TEST_ARF_XML_PATH,
               r'_package_\w+_removed'
               ]
    src = run_commad_and_save_output_to_file(command)
    with open(src, "r") as data:
        rules = json.load(data)
    assert len(rules.keys()) == 1


def test_command_with_parameter_out():
    command = [*COMMAND_START,
               'arf-to-json',
               '--all',
               TEST_ARF_XML_PATH,
               r'_package_\w+_removed'
               ]
    src = run_commad_and_save_output_to_file(command)

    time.sleep(5)

    command.append('-o' + src)
    subprocess.check_call(command)

    with open(src, "r") as data:
        rules = json.load(data)
    assert len(rules.keys()) == 4