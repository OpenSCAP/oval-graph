import pytest
import tempfile
import os
import uuid

from oval_graph.command_line_client.json_to_html import JsonToHtml
import tests.any_test_help


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
