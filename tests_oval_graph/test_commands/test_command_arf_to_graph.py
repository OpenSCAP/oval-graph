import os
import re
import subprocess

import pexpect
import pytest
from readchar import key

from ..test_tools import TestTools
from .command_constants import ARF_TO_GRAPH, COMMAND_START, TEST_ARF_XML_PATCH


def get_command_with_random_output_patch():
    src = TestTools.get_random_dir_in_tmp()
    command = [*ARF_TO_GRAPH]
    command[command.index('.')] = src
    return command, src


@pytest.mark.usefixtures("remove_generated_reports_in_root")
def test_command_arf_to_graph():
    subprocess.check_call(ARF_TO_GRAPH,
                          cwd='./')
    file_src = TestTools.find_files(
        "graph-of-xccdf_org.ssgproject.content_rule_package_abrt_removed",
        "../")
    TestTools.compare_results_html(file_src[0])


@pytest.mark.usefixtures("remove_generated_reports_in_root")
def test_command_arf_to_graph_with_verbose():
    command = [*ARF_TO_GRAPH, '--verbose']
    out = subprocess.check_output(command,
                                  cwd='./',
                                  stderr=subprocess.STDOUT)
    # Reads path to file from verbose output
    src_regex = r"\"(\.\/.*?)\""
    src = re.search(src_regex, out.decode('utf-8')).group(1)
    file_src = '.{}'.format(src)
    TestTools.compare_results_html(file_src)


def test_command_arf_to_graph_with_out_parameter():
    command, src = get_command_with_random_output_patch()
    subprocess.check_call(command)
    file_src = os.path.join(src, os.listdir(src)[0])
    TestTools.compare_results_html(file_src)


def test_inquirer_choice_rule():
    src = TestTools.get_random_dir_in_tmp()
    command_parameters = [*COMMAND_START,
                          'arf-to-graph',
                          '-o',
                          src,
                          TEST_ARF_XML_PATCH,
                          r'_package_\w+_removed'
                          ]
    command_parameters.remove("python3")
    sut = pexpect.spawn("python3", command_parameters)
    sut.expect(r'\w+')
    sut.send(key.DOWN)
    sut.send(key.SPACE)
    sut.send(key.ENTER)
    sut.wait()
    assert len(os.listdir(src)) == 1
    assert ("xccdf_org.ssgproject.content_rule_package_sendmail_removed"
            in os.listdir(src)[0])


def test_command_parameter_all():
    src = TestTools.get_random_dir_in_tmp()
    command = [*COMMAND_START,
               'arf-to-graph',
               '--all',
               '-o',
               src,
               TEST_ARF_XML_PATCH,
               '.',
               ]
    subprocess.check_call(command)
    assert len(os.listdir(src)) == 184


def test_command_parameter_all_and_show_failed_rules():
    src = TestTools.get_random_dir_in_tmp()
    command = [*COMMAND_START,
               'arf-to-graph',
               '--all',
               '--show-failed-rules',
               '-o',
               src,
               TEST_ARF_XML_PATCH,
               r'_package_\w+_removed'
               ]
    subprocess.check_call(command)
    assert len(os.listdir(src)) == 1
