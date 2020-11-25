import os
import sys
import tempfile
import uuid

import mock
import pytest

import tests.any_test_help
from oval_graph.command_line_client.json_to_html import JsonToHtml


def get_client_json_to_html(src, rule):
    return JsonToHtml(["--display", tests.any_test_help.get_src(src), rule])


def get_client_json_to_html_with_define_dest(src, rule):
    return JsonToHtml(
        ["--output", tests.any_test_help.get_src(
            os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))),
         tests.any_test_help.get_src(src),
         rule,
         ])


def try_expection_for_prepare_graph(src, rule, err):
    rules = {'rules': [rule]}
    with pytest.raises(Exception, match=err):
        client = get_client_json_to_html(src, rule)
        assert client.prepare_data(rules)


def test_prepare_graph_with_not_valid_file():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    rule = 'xccdf_org.ssgproject.content_rule_package_abrt_removed'
    try_expection_for_prepare_graph(src, rule, 'is not valid json')


def test_prepare_graph_with_not_exist_rule():
    src = 'test_data/referenc_html_report.html'
    rule = 'xccdf_org.ssgproject.content_rule_package_abrt_removed'
    try_expection_for_prepare_graph(src, rule, 'No such file or directory:')


def test_prepare_graph_with_bat_data():
    src = 'test_data/bad_result_data_json.json'
    rule = 'xccdf_org.ssgproject.content_rule_package_abrt_removed'
    try_expection_for_prepare_graph(src, rule, 'valid for OVAL tree')


def test_search_non_existent_rule():
    src = 'test_data/referenc_result_data_json.json'
    rule = 'non-existent_rule'
    err = '404'
    client = get_client_json_to_html(src, rule)
    with pytest.raises(Exception, match=err):
        assert client.search_rules_id()


@pytest.mark.usefixtures("remove_generated_reports_in_root")
def test_prepare_tree():
    src = 'test_data/referenc_result_data_json.json'
    rule = 'xccdf_org.ssgproject.content_rule_package_abrt_removed'
    client = get_client_json_to_html(src, rule)
    results_src = client.prepare_data({'rules': client.search_rules_id()})
    tests.any_test_help.compare_results_html(results_src[0])
    client.kill_web_browsers()


def test_prepare_tree_and_save_in_defined_destination():
    src = 'test_data/referenc_result_data_json.json'
    rule = 'xccdf_org.ssgproject.content_rule_package_abrt_removed'
    client = get_client_json_to_html_with_define_dest(src, rule)
    results_src = client.prepare_data({'rules': client.search_rules_id()})
    tests.any_test_help.compare_results_html(results_src[0])


def test_search_rules_id():
    src = 'test_data/referenc_result_data_json.json'
    part_of_id_rule = 'xccdf_org.ssgproject.'
    client = get_client_json_to_html(src, part_of_id_rule)
    assert len(client.search_rules_id()) == 184


def test_get_questions():
    src = 'test_data/referenc_result_data_json.json'
    regex = r'_package_\w+_removed'
    client = get_client_json_to_html(src, regex)
    out = client.get_questions()[0].choices
    rule1 = 'xccdf_org.ssgproject.content_rule_package_abrt_removed'
    rule2 = 'xccdf_org.ssgproject.content_rule_package_sendmail_removed'
    assert out[0] == rule1
    assert out[1] == rule2


def test_get_wanted_rules_from_array_of_ids():
    src = 'test_data/referenc_result_data_json.json'
    regex = r'_package_\w+_removed'
    client = get_client_json_to_html(src, regex)

    out = [
        'xccdf_org.ssgproject.content_rule_package_abrt_removed',
        'xccdf_org.ssgproject.content_rule_package_sendmail_removed',
    ]

    assert out == client._get_wanted_rules(
        client.json_data_file.keys())


def test_json_to_html_if_not_installed_inquirer(capsys):
    with mock.patch.dict(sys.modules, {'inquirer': None}):
        src = 'test_data/referenc_result_data_json.json'
        regex = r'_package_\w+_removed'
        client = get_client_json_to_html(src, regex)
        client.isatty = True
        tests.any_test_help.any_client_if_not_installed_inquirer(
            client, capsys, regex)


def test_get_only_fail_rules_not_implemented_error():
    src = 'test_data/referenc_result_data_json.json'
    part_of_id_rule = 'xccdf_org.ssgproject.'
    client = get_client_json_to_html(src, part_of_id_rule)
    with pytest.raises(NotImplementedError):
        assert client.get_only_fail_rule(['rule-id'])


def test_get_rows_of_unselected_rules_not_implemented_error():
    src = 'test_data/referenc_result_data_json.json'
    part_of_id_rule = 'xccdf_org.ssgproject.'
    client = get_client_json_to_html(src, part_of_id_rule)
    with pytest.raises(NotImplementedError):
        assert client._get_rows_of_unselected_rules()
