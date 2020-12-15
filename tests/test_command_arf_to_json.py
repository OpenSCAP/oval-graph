import subprocess
import os
import time
import json
import pytest
import pexpect
from readchar import key

import tests.any_test_help


def run_commad_and_save_output_to_file(parameters):
    src = tests.any_test_help.get_random_dir_in_tmp() + '.json'
    with open(src, 'w+') as output:
        subprocess.check_call(parameters, stdout=output)
    return src


def test_command_arf_to_json():
    src = tests.any_test_help.get_random_dir_in_tmp() + '.json'
    out = subprocess.check_output(['python3',
                                   '-m',
                                   'oval_graph.command_line',
                                   'arf-to-json',
                                   'tests/test_data/ssg-fedora-ds-arf.xml',
                                   'xccdf_org.ssgproject.content_rule_package_abrt_removed'
                                   ])
    with open(src, "w+") as f:
        f.writelines(out.decode('utf-8'))
    tests.any_test_help.compare_results_json(src)


def test_command_arf_to_json_is_tty():
    src = run_commad_and_save_output_to_file(
        [
            'python3',
            '-m',
            'oval_graph.command_line',
            'arf-to-json',
            'tests/test_data/ssg-fedora-ds-arf.xml',
            'xccdf_org.ssgproject.content_rule_package_abrt_removed'
        ])
    tests.any_test_help.compare_results_json(src)


def test_inquirer_choice_rule():
    src = tests.any_test_help.get_random_dir_in_tmp() + '.json'
    sut = pexpect.spawn('python3',
                        ['-m',
                         'oval_graph.command_line',
                         'arf-to-json',
                         'tests/test_data/ssg-fedora-ds-arf.xml',
                         r'_package_\w+_removed'
                         ])
    sut.expect(r'\w+')
    sut.send(key.DOWN)
    sut.send(key.SPACE)
    sut.send(key.SPACE)
    sut.send(key.UP)
    sut.send(key.SPACE)
    sut.send(key.ENTER)
    sut.wait()
    out = sut.readlines()
    with open(src, "w+") as f:
        f.writelines(row.decode("utf-8") for row in out[24:])
    tests.any_test_help.compare_results_json(src)


def test_command_parameter_all():
    src = run_commad_and_save_output_to_file(
        [
            'python3',
            '-m',
            'oval_graph.command_line',
            'arf-to-json',
            '--all',
            'tests/test_data/ssg-fedora-ds-arf.xml',
            '.'
        ])
    with open(src, "r") as f:
        rules = json.load(f)
    assert len(rules.keys()) == 184


def test_command_parameter_all_and_show_failed_rules():
    src = run_commad_and_save_output_to_file(
        [
            'python3',
            '-m',
            'oval_graph.command_line',
            'arf-to-json',
            '--all',
            '--show-failed-rules',
            'tests/test_data/ssg-fedora-ds-arf.xml',
            r'_package_\w+_removed'
        ])
    with open(src, "r") as f:
        rules = json.load(f)
    assert len(rules.keys()) == 1


def test_command_with_parameter_out():
    src = run_commad_and_save_output_to_file(
        [
            'python3',
            '-m',
            'oval_graph.command_line',
            'arf-to-json',
            '--all',
            'tests/test_data/ssg-fedora-ds-arf.xml',
            r'_package_\w+_removed'
        ])
    time.sleep(5)
    subprocess.check_call(['python3',
                           '-m',
                           'oval_graph.command_line',
                           'arf-to-json',
                           '--all',
                           'tests/test_data/ssg-fedora-ds-arf.xml',
                           r'_package_\w+_removed',
                           '-o' + src
                           ])
    with open(src, "r") as f:
        rules = json.load(f)
    assert len(rules.keys()) == 4


def test_bad_command_arf_to_json_with_verbose():
    out = subprocess.check_output(
        [
            'python3',
            '-m',
            'oval_graph.command_line',
            'arf-to-json',
            '-v',
            'tests/test_data/xccdf_org.ssgproject.content_profile_ospp-results-initial.xml',
            '.'],
        stderr=subprocess.STDOUT)
    out_string = out.decode('utf-8')
    assert out_string.find("Traceback") > -1
    assert out_string.find("Warning:") > -1
    assert out_string.find("Error:") > -1


def test_bad_command_arf_to_json():
    out = subprocess.check_output(
        [
            'python3',
            '-m',
            'oval_graph.command_line',
            'arf-to-graph',
            'tests/test_data/xccdf_org.ssgproject.content_profile_ospp-results-initial.xml',
            '.'],
        stderr=subprocess.STDOUT)
    out_string = out.decode('utf-8')
    assert out.decode('utf-8').find("Traceback") == -1
    assert out.decode('utf-8').find("Warning:") > -1
    assert out.decode('utf-8').find("Error:") > -1
