import re
import subprocess
from pathlib import Path

import pytest

from ..test_tools import TestTools
from .command_constants import ARF_TO_GRAPH, COMMAND_START, TEST_ARF_XML_PATH


def get_command_with_random_output_path():
    path = TestTools.get_random_path_in_tmp()
    command = [*ARF_TO_GRAPH]
    command[command.index('.')] = str(path)
    return command, str(path)


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
    src_regex = r"\"(.*?)\"$"
    src = re.search(src_regex, out.decode('utf-8')).group(1)
    file_src = Path(__file__).parent.parent.parent / src
    TestTools.compare_results_html(file_src)


def test_command_arf_to_graph_with_out_parameter():
    command, src = get_command_with_random_output_path()
    subprocess.check_call(command)
    TestTools.compare_results_html(src)


def test_command_parameter_all():
    path = TestTools.get_random_path_in_tmp()
    command = [*COMMAND_START,
               'arf-to-graph',
               '--all',
               '-o',
               str(path),
               TEST_ARF_XML_PATH,
               '.',
               ]
    subprocess.check_call(command)
    assert len(list(path.glob("**/*.html"))) == 184


def test_command_parameter_all_and_show_failed_rules():
    path = TestTools.get_random_path_in_tmp()
    command = [*COMMAND_START,
               'arf-to-graph',
               '--all',
               '--show-failed-rules',
               '-o',
               str(path),
               TEST_ARF_XML_PATH,
               r'_package_\w+_removed'
               ]
    subprocess.check_call(command)
    assert path.is_file()
