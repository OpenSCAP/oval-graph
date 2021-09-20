import tempfile
import uuid
from pathlib import Path

import pytest

from oval_graph.command_line_client.json_to_html import JsonToHtml

from ...test_tools import TestTools
from .constants_for_tests import (PATH_TO_ARF_REPORT, PATH_TO_BAD_RESULT_JSON,
                                  PATH_TO_JSON_REPORT,
                                  PATH_TO_REFERENCE_RESULT_HTML, SEARCH_RULES)


def get_client_json_to_html(rule, optional_args=None, src=None):
    path = str(PATH_TO_JSON_REPORT)
    if src is not None:
        path = str(src)
    args = ["--display", path, rule]
    if optional_args is not None:
        args.extend(optional_args)
    client = JsonToHtml(args)
    client.load_file()
    return client


@pytest.mark.parametrize("src, error_pattern", [
    (str(PATH_TO_ARF_REPORT), 'is not valid json'),
    (str(PATH_TO_REFERENCE_RESULT_HTML), 'No such file or directory:'),
    (str(PATH_TO_BAD_RESULT_JSON), 'valid for OVAL tree')
])
def test_expection_for_prepare_graph(src, error_pattern):
    rule = 'xccdf_org.ssgproject.content_rule_package_abrt_removed'
    rules = {'rules': [rule]}
    with pytest.raises(Exception, match=error_pattern):
        client = get_client_json_to_html(rule, None, src)
        assert client.prepare_data(rules)


def test_search_non_existent_rule():
    rule = 'non-existent_rule'
    err = '404'
    client = get_client_json_to_html(rule)
    with pytest.raises(Exception, match=err):
        assert client.search_rules_id()


@pytest.mark.parametrize("args", [
    (None),
    (["--output", str(Path(tempfile.gettempdir() / Path(str(uuid.uuid4()))))]),
])
@pytest.mark.usefixtures("remove_generated_reports_in_root")
def test_prepare_tree(args):
    rule = 'xccdf_org.ssgproject.content_rule_package_abrt_removed'
    client = get_client_json_to_html(rule, args)
    TestTools.prepare_tree_test(client, rule)


@pytest.mark.parametrize("part_of_id_rule, result", SEARCH_RULES)
def test_search_rules_id(part_of_id_rule, result):
    client = get_client_json_to_html(part_of_id_rule)
    assert len(client.search_rules_id()) == result


def test_get_only_fail_rules_not_implemented_error():
    part_of_id_rule = 'xccdf_org.ssgproject.'
    client = get_client_json_to_html(part_of_id_rule)
    with pytest.raises(NotImplementedError):
        assert client.get_only_fail_rule(['rule-id'])
