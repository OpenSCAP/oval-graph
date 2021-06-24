import subprocess

import pytest

COMMAND_START = ['python3',
                 '-m',
                 'oval_graph.command_line'
                 ]

JSON_TO_GRAPH_COMMAND = [*COMMAND_START,
                         'json-to-graph',
                         'tests_oval_graph/global_test_data/ssg-fedora-ds-arf.xml',
                         '.'
                         ]


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
    command = [*JSON_TO_GRAPH_COMMAND, '-v']
    out = subprocess.check_output(command,
                                  stderr=subprocess.STDOUT)
    out_string = out.decode('utf-8')
    assert out_string.find("Traceback") > -1
    assert out_string.find("Error:") > -1


def test_bad_command_json_to_graph():
    out = subprocess.check_output(JSON_TO_GRAPH_COMMAND,
                                  stderr=subprocess.STDOUT)
    out_string = out.decode('utf-8')
    assert out_string.find("Traceback") == -1
    assert out_string.find("Error:") > -1
