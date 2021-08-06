import subprocess

import pytest

from .command_constants import BAD_JSON_TO_GRAPH, COMMAND_START


@pytest.mark.parametrize("command_name, optional_args", [
    ('arf-to-graph', []),
    ('arf-to-json', []),
    ('arf-to-graph', ['-v']),
    ('arf-to-json', ['-v']),
])
def test_command_with_bad_arf_file(command_name, optional_args):
    command = [
        *COMMAND_START,
        command_name,
        ('tests_oval_graph/global_test_data/'
         'xccdf_org.ssgproject.content_profile_ospp-results-initial.xml'),
        '.'
    ]
    command.extend(optional_args)

    out = subprocess.check_output(
        command,
        stderr=subprocess.STDOUT)
    out_string = out.decode('utf-8')
    if '-v' in optional_args:
        assert out_string.find("Traceback") > -1
    else:
        assert out_string.find("Traceback") == -1
    assert out_string.find("Warning:") > -1
    assert out_string.find("Error:") > -1


def test_bad_command_json_to_graph_with_verbose():
    command = [*BAD_JSON_TO_GRAPH, '-v']
    out = subprocess.check_output(command,
                                  stderr=subprocess.STDOUT)
    out_string = out.decode('utf-8')
    assert out_string.find("Traceback") > -1
    assert out_string.find("Error:") > -1


def test_bad_command_json_to_graph():
    out = subprocess.check_output(BAD_JSON_TO_GRAPH,
                                  stderr=subprocess.STDOUT)
    out_string = out.decode('utf-8')
    assert out_string.find("Traceback") == -1
    assert out_string.find("Error:") > -1
