import pytest
import tempfile
import os
import uuid
import mock
import sys

from oval_graph.command_line_client.arf_to_html import ArfToHtml
import tests.any_test_help


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
