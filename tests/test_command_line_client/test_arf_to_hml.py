import os
import sys
import tempfile
import uuid

import mock
import pytest

import tests.any_test_help
from oval_graph.command_line_client.arf_to_html import ArfToHtml


def get_client_arf_to_html(src, rule):
    return ArfToHtml(["--display", tests.any_test_help.get_src(src), rule])


def get_client_arf_to_html_with_define_dest(src, rule):
    return ArfToHtml(
        ["--output", tests.any_test_help.get_src(
            os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))),
         tests.any_test_help.get_src(src),
         rule])


def get_client_arf_to_html_with_option_show_failed_rules(src, rule):
    return ArfToHtml(["--show-failed-rules",
                      tests.any_test_help.get_src(src), rule])


def get_client_arf_to_html_with_option_show_not_selected_rules(src, rule):
    return ArfToHtml(["--show-not-selected-rules",
                      tests.any_test_help.get_src(src),
                      rule])


def get_client_arf_to_html_with_option_show_not_selected_rules_and_show_failed_rules(
        src,
        rule):
    return ArfToHtml(["--show-not-selected-rules",
                      "--show-failed-rules",
                      tests.any_test_help.get_src(src),
                      rule])


def try_expection_for_prepare_graph(src, rule, err):
    client = get_client_arf_to_html(src, rule)
    rules = {'rules': [rule]}
    with pytest.raises(Exception, match=err):
        assert client.prepare_data(rules)


def test_prepare_graph_with_non_existent_rule():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    rule = 'non-existent_rule'
    try_expection_for_prepare_graph(src, rule, '404')


def test_prepare_graph_with_not_selected_rule():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    rule = 'xccdf_org.ssgproject.content_rule_package_nis_removed'
    try_expection_for_prepare_graph(src, rule, 'not selected')


def try_expection_for_search_rule_id(src, rule, err):
    client = get_client_arf_to_html(src, rule)
    with pytest.raises(Exception, match=err):
        assert client.search_rules_id()


def test_search_non_existent_rule():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    rule = 'non-existent_rule'
    try_expection_for_search_rule_id(src, rule, '404')


def test_search_rule_id_not_selected_rule():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    rule = 'xccdf_org.ssgproject.content_rule_package_nis_removed'
    try_expection_for_search_rule_id(src, rule, 'not selected')


@pytest.mark.usefixtures("remove_generated_reports_in_root")
def test_prepare_tree():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    rule = 'xccdf_org.ssgproject.content_rule_package_abrt_removed'
    client = get_client_arf_to_html(src, rule)
    rules = {'rules': [rule]}
    results_src = client.prepare_data(rules)
    tests.any_test_help.compare_results_html(results_src[0])
    client.kill_web_browsers()


def test_prepare_tree_and_save_in_defined_destination():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    rule = 'xccdf_org.ssgproject.content_rule_package_abrt_removed'
    client = get_client_arf_to_html_with_define_dest(src, rule)
    rules = {'rules': [rule]}
    results_src = client.prepare_data(rules)
    tests.any_test_help.compare_results_html(results_src[0])


def test_get_questions_not_selected(capsys):
    src = 'test_data/ssg-fedora-ds-arf.xml'
    regex = r'_package_\w+_removed'
    client = get_client_arf_to_html_with_option_show_not_selected_rules(
        src, regex)
    tests.any_test_help.get_questions_not_selected(capsys, client)


def test_get_questions_not_selected_and_show_failed_rules(capsys):
    src = 'test_data/ssg-fedora-ds-arf.xml'
    regex = r'_package_\w+_removed'
    client = get_client_arf_to_html_with_option_show_not_selected_rules_and_show_failed_rules(
        src, regex)
    tests.any_test_help.get_questions_not_selected_and_show_failed_rules(
        capsys, client)


def test_get_questions_with_option_show_failed_rules():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    regex = r'_package_\w+_removed'
    client = get_client_arf_to_html_with_option_show_failed_rules(src, regex)
    tests.any_test_help.get_questions_with_option_show_failed_rules(client)


def test_if_not_installed_inquirer_with_option_show_failed_rules(capsys):
    with mock.patch.dict(sys.modules, {'inquirer': None}):
        src = 'test_data/ssg-fedora-ds-arf.xml'
        regex = r'_package_\w+_removed'
        client = get_client_arf_to_html_with_option_show_failed_rules(
            src, regex)
        client.isatty = True
        tests.any_test_help.if_not_installed_inquirer_with_option_show_failed_rules(
            capsys, client)


def test_if_not_installed_inquirer_with_option_show_not_selected_rules(capsys):
    with mock.patch.dict(sys.modules, {'inquirer': None}):
        src = 'test_data/ssg-fedora-ds-arf.xml'
        regex = r'_package_\w+_removed'
        client = get_client_arf_to_html_with_option_show_not_selected_rules(
            src, regex)
        client.isatty = True
        tests.any_test_help.if_not_installed_inquirer_with_option_show_not_selected_rules(
            capsys, client)


def test_if_not_installed_inquirer_with_option_show_not_selected_rules_and_show_failed_rules(
        capsys):
    with mock.patch.dict(sys.modules, {'inquirer': None}):
        src = 'test_data/ssg-fedora-ds-arf.xml'
        regex = r'_package_\w+_removed'
        client = get_client_arf_to_html_with_option_show_not_selected_rules_and_show_failed_rules(
            src, regex)
        client.isatty = True
        (tests.any_test_help.
         if_not_installed_inquirer_with_option_show_not_selected_rules_and_show_failed_rules(
             capsys, client))


def test_search_rules_id():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    part_of_id_rule = 'xccdf_org.ssgproject.'
    client = get_client_arf_to_html(src, part_of_id_rule)
    assert len(client.search_rules_id()) == 184


def test_get_questions():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    regex = r'_package_\w+_removed'
    client = get_client_arf_to_html(src, regex)
    out = client.get_questions()[0].choices
    rule1 = 'xccdf_org.ssgproject.content_rule_package_abrt_removed'
    rule2 = 'xccdf_org.ssgproject.content_rule_package_sendmail_removed'
    assert out[0] == rule1
    assert out[1] == rule2


def test_get_wanted_not_selected_rules_from_array_of_IDs():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    regex = r'_package_\w+_removed'
    client = get_client_arf_to_html(src, regex)

    out = [
        'xccdf_org.ssgproject.content_rule_package_nis_removed',
        'xccdf_org.ssgproject.content_rule_package_ntpdate_removed',
        'xccdf_org.ssgproject.content_rule_package_telnetd_removed',
        'xccdf_org.ssgproject.content_rule_package_gdm_removed',
        'xccdf_org.ssgproject.content_rule_package_setroubleshoot_removed',
        'xccdf_org.ssgproject.content_rule_package_mcstrans_removed']

    assert out == client._get_wanted_rules(
        client.arf_xml_parser.notselected_rules)


def test_get_wanted_rules_from_array_of_ids():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    regex = r'_package_\w+_removed'
    client = get_client_arf_to_html(src, regex)

    out = [
        'xccdf_org.ssgproject.content_rule_package_abrt_removed',
        'xccdf_org.ssgproject.content_rule_package_sendmail_removed',
    ]

    assert out == client._get_wanted_rules(
        client.arf_xml_parser.used_rules.keys())


def test_arf_to_html_if_not_installed_inquirer(capsys):
    with mock.patch.dict(sys.modules, {'inquirer': None}):
        src = 'test_data/ssg-fedora-ds-arf.xml'
        regex = r'_package_\w+_removed'
        client = get_client_arf_to_html(src, regex)
        tests.any_test_help.any_client_if_not_installed_inquirer(
            client, capsys, regex)
