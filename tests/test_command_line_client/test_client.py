import re
import json
import mock
import sys
import os
import tempfile

import pytest

from oval_graph.command_line_client.client import Client
import tests.any_test_help


def get_client(src, rule):
    return Client(
        [tests.any_test_help.get_src(src), rule])


def get_client_on_web_browser(src, rule):
    return Client(
        [tests.any_test_help.get_src(src), rule])


def test_client():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    rule = 'rule'
    client = get_client(src, rule)
    assert client.source_filename == tests.any_test_help.get_src(src)
    assert client.rule_name == rule


def test_search_rules_id():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    part_of_id_rule = 'xccdf_org.ssgproject.'
    client = get_client(src, part_of_id_rule)
    assert len(client.search_rules_id()) == 184


def test_search_rules_id_on_web_browser():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    part_of_id_rule = 'xccdf_org.ssgproject.'
    client = get_client_on_web_browser(src, part_of_id_rule)
    assert len(client.search_rules_id()) == 184


def test_search_non_existent_rule():
    rule = 'random_rule_which_doest_exist'
    src = 'test_data/ssg-fedora-ds-arf.xml'
    client = get_client(src, rule)
    with pytest.raises(Exception, match='404 rule "{}" not found!'.format(rule)):
        assert client.search_rules_id()


def test_find_not_selected_rule():
    rule = 'xccdf_org.ssgproject.content_rule_ntpd_specify_remote_server'
    src = 'test_data/ssg-fedora-ds-arf.xml'
    client = get_client(src, rule)
    with pytest.raises(Exception, match=rule):
        assert client.search_rules_id()


def test_search_rules_with_regex():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    regex = r'_package_\w+_removed'
    client = get_client(src, regex)
    assert len(client.search_rules_id()) == 2


def test_get_questions():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    regex = r'_package_\w+_removed'
    client = get_client(src, regex)
    out = client.get_questions()[0].choices
    rule1 = 'xccdf_org.ssgproject.content_rule_package_abrt_removed'
    rule2 = 'xccdf_org.ssgproject.content_rule_package_sendmail_removed'
    assert out[0] == rule1
    assert out[1] == rule2


def test_get_wanted_not_selected_rules_from_array_of_IDs():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    regex = r'_package_\w+_removed'
    client = get_client(src, regex)

    out = [
        'xccdf_org.ssgproject.content_rule_package_nis_removed',
        'xccdf_org.ssgproject.content_rule_package_ntpdate_removed',
        'xccdf_org.ssgproject.content_rule_package_telnetd_removed',
        'xccdf_org.ssgproject.content_rule_package_gdm_removed',
        'xccdf_org.ssgproject.content_rule_package_setroubleshoot_removed',
        'xccdf_org.ssgproject.content_rule_package_mcstrans_removed']

    assert out == client._get_wanted_rules_from_array_of_IDs(
        client.xml_parser.notselected_rules)


def test_get_wanted_rules_from_array_of_IDs():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    regex = r'_package_\w+_removed'
    client = get_client(src, regex)

    out = [
        'xccdf_org.ssgproject.content_rule_package_abrt_removed',
        'xccdf_org.ssgproject.content_rule_package_sendmail_removed',
    ]

    assert out == client._get_wanted_rules_from_array_of_IDs(
        client.xml_parser.used_rules.keys())


def test_search_not_selected_rule():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    non_existent_rule = 'xccdf_org.ssgproject.content_rule_package_nis_removed'
    with pytest.raises(Exception, match=non_existent_rule):
        assert get_client(src, non_existent_rule).search_rules_id()


def test_if_not_installed_inquirer(capsys):
    with mock.patch.dict(sys.modules, {'inquirer': None}):
        src = 'test_data/ssg-fedora-ds-arf.xml'
        regex = r'_package_\w+_removed'
        client = get_client(src, regex)
        client.isatty = True
        out = client.run_gui_and_return_answers()
        assert out is None
        captured = capsys.readouterr()
        assert len(re.findall(regex, captured.out)) == 2
