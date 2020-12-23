import sys

import mock
import pytest

import tests.any_test_help
from oval_graph.command_line_client.client import Client


def get_client(src, rule):
    return Client(
        [tests.any_test_help.get_src(src), rule])


def get_client_all(src, rule):
    return Client(
        [tests.any_test_help.get_src(src), rule, '--all'])


def test_client():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    rule = 'rule'
    client = get_client(src, rule)
    assert client.source_filename == tests.any_test_help.get_src(src)
    assert client.rule_name == rule


def test_search_rules_id_not_implemented_error():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    part_of_id_rule = 'xccdf_org.ssgproject.'
    client = get_client(src, part_of_id_rule)
    with pytest.raises(NotImplementedError):
        assert client.search_rules_id()


def test_get_questions_not_implemented_error():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    regex = r'_package_\w+_removed'
    client = get_client(src, regex)
    with pytest.raises(NotImplementedError):
        assert client.get_questions()[0].choices


def test_if_not_installed_inquirer_not_implemented_error():
    with mock.patch.dict(sys.modules, {'inquirer': None}):
        src = 'test_data/ssg-fedora-ds-arf.xml'
        regex = r'_package_\w+_removed'
        client = get_client(src, regex)
        client.isatty = True

        with pytest.raises(NotImplementedError):
            assert client.run_gui_and_return_answers()


def test_if_tty_and_use_parameter_all_not_implemented_error():
    with mock.patch.dict(sys.modules, {'inquirer': None}):
        src = 'test_data/ssg-fedora-ds-arf.xml'
        regex = r'_package_\w+_removed'
        client = get_client_all(src, regex)
        client.isatty = True

        with pytest.raises(NotImplementedError):
            assert client.run_gui_and_return_answers()


def test_get_only_fail_rules_not_implemented_error():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    part_of_id_rule = 'xccdf_org.ssgproject.'
    client = get_client(src, part_of_id_rule)
    with pytest.raises(NotImplementedError):
        assert client.get_only_fail_rule(['rule-id'])


def test_get_rows_of_unselected_rules_not_implemented_error():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    part_of_id_rule = 'xccdf_org.ssgproject.'
    client = get_client(src, part_of_id_rule)
    with pytest.raises(NotImplementedError):
        assert client._get_rows_of_unselected_rules()
