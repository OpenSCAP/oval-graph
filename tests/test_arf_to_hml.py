import pytest
import tempfile
import os
import uuid

from oval_graph.arf_to_html import ArfToHtml
import tests.any_test_help


def get_client_arf_to_html(src, rule):
    return ArfToHtml(
        ["--off-web-browser", tests.any_test_help.get_src(src), rule])


def get_client_arf_to_html_with_define_dest(src, rule):
    return ArfToHtml(
        ["--output", tests.any_test_help.get_src(
            os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))),
         "--off-web-browser",
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
    tests.any_test_help.compare_results_js(results_src[0])


def test_prepare_tree_and_save_in_defined_destination():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    rule = 'xccdf_org.ssgproject.content_rule_package_abrt_removed'
    client = get_client_arf_to_html_with_define_dest(src, rule)
    rules = {'rules': [rule]}
    results_src = client.prepare_data(rules)
    tests.any_test_help.compare_results_js(results_src[0])
