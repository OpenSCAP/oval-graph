import tempfile
import uuid
from pathlib import Path

import pytest

from oval_graph.command_line_client.arf_to_html import ArfToHtml

from ...test_tools import TestTools
from .constants_for_tests import (EXPECTED_RULES_ID, EXPECTED_RULES_ID_WITH_ARGS,
                                  SEARCH_BAD_RULES, SEARCH_RULES, PATH_TO_REPORT)


def get_client_arf_to_html(rule, optional_args=None):
    path = str(PATH_TO_REPORT)
    args = ["--display", path, rule]
    if optional_args is not None:
        args.extend(optional_args)
    client = ArfToHtml(args)
    client.load_file()
    return client


@pytest.mark.parametrize("rule, error_pattern", SEARCH_BAD_RULES)
def test_expection_prepare_data(rule, error_pattern):
    client = get_client_arf_to_html(rule)
    rules = {'rules': [rule]}
    with pytest.raises(Exception, match=error_pattern):
        assert client.prepare_data(rules)


@pytest.mark.parametrize("rule, error_pattern", SEARCH_BAD_RULES)
def test_expection_search_rules_id(rule, error_pattern):
    client = get_client_arf_to_html(rule)
    with pytest.raises(Exception, match=error_pattern):
        assert client.search_rules_id()


@pytest.mark.parametrize("args", [
    (None),
    (["--output", str(Path(tempfile.gettempdir()) / Path(str(uuid.uuid4())))]),
])
@pytest.mark.usefixtures("remove_generated_reports_in_root")
def test_prepare_tree(args):
    rule = 'xccdf_org.ssgproject.content_rule_package_abrt_removed'
    client = get_client_arf_to_html(rule, args)
    TestTools.prepare_tree_test(client, rule)


@pytest.mark.parametrize("args, result", EXPECTED_RULES_ID_WITH_ARGS)
def test_get_questions_with_parameters(capsys, args, result):
    rule = r'_package_\w+_removed'
    client = get_client_arf_to_html(rule, args)
    TestTools.get_questions_not_selected(capsys, client, result)


def test_get_questions_with_option_show_failed_rules():
    rule = r'_package_\w+_removed'
    client = get_client_arf_to_html(rule, ["--show-failed-rules"])
    TestTools.get_questions_with_option_show_failed_rules(client)


def test_get_questions():
    rule = r'_package_\w+_removed'
    client = get_client_arf_to_html(rule)
    out = client.get_questions()[0].choices
    assert out == EXPECTED_RULES_ID


@pytest.mark.parametrize("part_of_id_rule, result", SEARCH_RULES)
def test_search_rules_id(part_of_id_rule, result):
    client = get_client_arf_to_html(part_of_id_rule)
    assert len(client.search_rules_id()) == result
