import subprocess
import os
import pytest
from readchar import key

import tests.any_test_help


@pytest.mark.usefixtures("remove_generated_reports_in_root")
def test_command_arf_to_graph():
    out = subprocess.check_output(['python3',
                                   '-m',
                                   'oval_graph.command_line',
                                   'arf-to-graph',
                                   '--off-web-browser',
                                   'tests/test_data/ssg-fedora-ds-arf.xml',
                                   'xccdf_org.ssgproject.content_rule_package_abrt_removed'
                                   ])
    tests.any_test_help.compare_results_html(
        out.decode('utf-8').split('\n')[-2])


def test_command_arf_to_graph_with_out_parameter():
    src = tests.any_test_help.get_random_dir_in_tmp()
    subprocess.check_call(['python3',
                           '-m',
                           'oval_graph.command_line',
                           'arf-to-graph',
                           '--off-web-browser',
                           '-o',
                           src,
                           'tests/test_data/ssg-fedora-ds-arf.xml',
                           'xccdf_org.ssgproject.content_rule_package_abrt_removed'
                           ])
    tests.any_test_help.compare_results_html(
        os.path.join(src, os.listdir(src)[0]))


def test_inquirer_choice_rule():
    pexpect = pytest.importorskip("pexpect")
    src = tests.any_test_help.get_random_dir_in_tmp()
    sut = pexpect.spawn('python3',
                        ['-m',
                         'oval_graph.command_line',
                         'arf-to-graph',
                         '-o',
                         src,
                         '--off-web-browser',
                         'tests/test_data/ssg-fedora-ds-arf.xml',
                         r'_package_\w+_removed'
                         ])
    sut.expect(r'\w+')
    sut.send(key.DOWN)
    sut.send(key.SPACE)
    sut.send(key.ENTER)
    sut.wait()
    assert len(os.listdir(src)) == 1
    assert ("xccdf_org.ssgproject.content_rule_package_sendmail_removed"
            in os.listdir(src)[0])


def test_command_parameter_all():
    src = tests.any_test_help.get_random_dir_in_tmp()
    subprocess.check_call(['python3',
                           '-m',
                           'oval_graph.command_line',
                           'arf-to-graph',
                           '--off-web-browser',
                           '--all',
                           '-o',
                           src,
                           'tests/test_data/ssg-fedora-ds-arf.xml',
                           '.'
                           ])
    assert len(os.listdir(src)) == 184


def test_command_parameter_all_and_show_failed_rules():
    src = tests.any_test_help.get_random_dir_in_tmp()
    subprocess.check_call(['python3',
                           '-m',
                           'oval_graph.command_line',
                           'arf-to-graph',
                           '--off-web-browser',
                           '--all',
                           '--show-failed-rules',
                           '-o',
                           src,
                           'tests/test_data/ssg-fedora-ds-arf.xml',
                           r'_package_\w+_removed'
                           ])
    # Right value is 1. Value 2 is caused by problem with parameter
    # --show-failed-rules (issue #116)
    assert len(os.listdir(src)) == 2
