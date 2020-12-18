import subprocess
import os
import json
import pytest
import tempfile
import pexpect
from readchar import key

import tests.any_test_help


@pytest.mark.usefixtures("remove_generated_reports_in_root")
def test_command_json_to_graph():
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
    subprocess.check_call(['python3',
                           '-m',
                           'oval_graph.command_line',
                           'json-to-graph',
                           '-o', '.',
                           src,
                           'xccdf_org.ssgproject.content_rule_package_abrt_removed'
                           ], cwd='./')
    file_src = tests.any_test_help.find_files(
        "graph-of-xccdf_org.ssgproject.content_rule_package_abrt_removed",
        '../')
    tests.any_test_help.compare_results_html(file_src[0])


@pytest.mark.usefixtures("remove_generated_reports_in_root")
def test_command_json_to_graph_with_verbose():
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
    out = subprocess.check_output(['python3',
                                   '-m',
                                   'oval_graph.command_line',
                                   'json-to-graph',
                                   '-o', '.',
                                   '--verbose',
                                   src,
                                   'xccdf_org.ssgproject.content_rule_package_abrt_removed'
                                   ],
                                  cwd='./',
                                  stderr=subprocess.STDOUT)
    src = out.decode('utf-8').split('\n')[-2]
    tests.any_test_help.compare_results_html('.' + src)


def test_command_json_to_graph_is_tty():
    src = tests.any_test_help.get_random_dir_in_tmp() + '.json'
    with open(src, 'w+')as output:
        subprocess.check_call(['python3',
                               '-m',
                               'oval_graph.command_line',
                               'arf-to-json',
                               'tests/test_data/ssg-fedora-ds-arf.xml',
                               'xccdf_org.ssgproject.content_rule_package_abrt_removed'
                               ],
                              stdout=output)
    out_dir = tests.any_test_help.get_random_dir_in_tmp()
    out = subprocess.check_output(['python3',
                                   '-m',
                                   'oval_graph.command_line',
                                   'json-to-graph',
                                   '--out',
                                   out_dir,
                                   src,
                                   'xccdf_org.ssgproject.content_rule_package_abrt_removed'
                                   ])
    tests.any_test_help.compare_results_html(
        os.path.join(out_dir, os.listdir(out_dir)[0]))


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
    sut.send(key.UP)
    sut.send(key.SPACE)
    sut.send(key.ENTER)
    sut.wait()
    out = sut.readlines()

    with open(src, "w+") as f:
        f.writelines(row.decode("utf-8") for row in out[20:])
    tests.any_test_help.compare_results_json(src)

    out_dir = tests.any_test_help.get_random_dir_in_tmp()
    sut = pexpect.spawn('python3',
                        ['-m',
                         'oval_graph.command_line',
                         'json-to-graph',
                         '-o',
                         out_dir,
                         src,
                         '.'
                         ])
    sut.expect(r'\w+')
    sut.send(key.DOWN)
    sut.send(key.SPACE)
    sut.send(key.ENTER)
    sut.wait()
    assert len(os.listdir(out_dir)) == 1
    assert ("xccdf_org.ssgproject.content_rule_package_abrt_removed"
            in os.listdir(out_dir)[0])


def test_command_parameter_all():
    src = tests.any_test_help.get_random_dir_in_tmp() + '.json'
    with open(src, 'w+')as output:
        subprocess.check_call(['python3',
                               '-m',
                               'oval_graph.command_line',
                               'arf-to-json',
                               '--all',
                               'tests/test_data/ssg-fedora-ds-arf.xml',
                               '.'
                               ],
                              stdout=output)
    with open(src, "r") as f:
        rules = json.load(f)
    assert len(rules.keys()) == 184
    out_dir = tests.any_test_help.get_random_dir_in_tmp()
    subprocess.check_call(['python3',
                           '-m',
                           'oval_graph.command_line',
                           'json-to-graph',
                           src,
                           '.',
                           '--all',
                           '-o',
                           out_dir
                           ])
    assert len(os.listdir(out_dir)) == 184


def test_bad_command_json_to_graph_with_verbose():
    out = subprocess.check_output(['python3',
                                   '-m',
                                   'oval_graph.command_line',
                                   'json-to-graph',
                                   '-v',
                                   'tests/test_data/ssg-fedora-ds-arf.xml',
                                   '.'
                                   ],
                                  stderr=subprocess.STDOUT)
    out_string = out.decode('utf-8')
    assert out_string.find("Traceback") > -1
    assert out_string.find("Error:") > -1


def test_bad_command_json_to_graph():
    out = subprocess.check_output(['python3',
                                   '-m',
                                   'oval_graph.command_line',
                                   'json-to-graph',
                                   'tests/test_data/ssg-fedora-ds-arf.xml',
                                   '.'
                                   ],
                                  stderr=subprocess.STDOUT)
    out_string = out.decode('utf-8')
    assert out_string.find("Traceback") == -1
    assert out_string.find("Error:") > -1
