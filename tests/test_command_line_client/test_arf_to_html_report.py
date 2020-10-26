import os
import tempfile
import uuid

import pytest

import tests.any_test_help
from oval_graph.command_line_client.arf_to_html_report import ArfToHtmlReport


def get_client_arf_to_html(src):
    return ArfToHtmlReport([tests.any_test_help.get_src(src)])


def get_client_arf_to_html_with_define_dest(src):
    return ArfToHtmlReport(
        ["--output", tests.any_test_help.get_src(
            os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))),
         tests.any_test_help.get_src(src)
         ])


def try_expection_for_prepare_graph(src, err):
    with pytest.raises(Exception, match=err):
        client = get_client_arf_to_html(src)
        rules = {'rules': ['.']}
        assert client.prepare_data(rules)


def test_prepare_report_with_bad_file():
    src = 'test_data/xccdf_org.ssgproject.content_profile_ospp-results-initial.xml'

    try_expection_for_prepare_graph(src, 'not arf report')


@pytest.mark.usefixtures("remove_generated_reports_in_root")
def test_prepare_report():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    client = get_client_arf_to_html(src)
    rules = {'rules': ['.']}
    results_src = client.prepare_data(rules)
    client.kill_web_browsers()
    assert os.path.exists(results_src[0])


def test_prepare_report_and_save_in_defined_destination():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    client = get_client_arf_to_html_with_define_dest(src)
    rules = {'rules': ['.']}
    results_src = client.prepare_data(rules)
    assert os.path.exists(results_src[0])
