import tempfile
import uuid
from pathlib import Path

import pytest

from oval_graph.command_line_client.arf_to_html import ArfToHtml

from ...test_tools import TestTools

PATH_TO_REPORT = Path('../../global_test_data/ssg-fedora-ds-arf.xml')
TOP_PATH = Path(__file__).parent

EXPECTED_RULES_ID = [
    'xccdf_org.ssgproject.content_rule_package_abrt_removed',
    'xccdf_org.ssgproject.content_rule_package_sendmail_removed'
]


def get_client_arf_to_html(rule, optional_args=None):
    path = str(TOP_PATH / PATH_TO_REPORT)
    args = ["--display", path, rule]
    if optional_args is not None:
        args.extend(optional_args)
    client = ArfToHtml(args)
    client.load_file()
    return client


@pytest.mark.parametrize("rule, error_pattern", [
    ('non-existent_rule', '404'),
    ('xccdf_org.ssgproject.content_rule_package_nis_removed', 'notselected'),
])
def test_expection_prepare_data(rule, error_pattern):
    client = get_client_arf_to_html(rule)
    rules = {'rules': [rule]}
    with pytest.raises(Exception, match=error_pattern):
        assert client.prepare_data(rules)


@pytest.mark.parametrize("rule, error_pattern", [
    ('non-existent_rule', '404'),
    ('xccdf_org.ssgproject.content_rule_package_nis_removed', 'notselected'),
])
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


@pytest.mark.parametrize("args, result", [
    (
        ["--show-not-selected-rules"],
        EXPECTED_RULES_ID,
    ),
    (
        ["--show-not-selected-rules", "--show-failed-rules"],
        [EXPECTED_RULES_ID[0]],
    ),
])
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


@pytest.mark.parametrize("part_of_id_rule, result", [
    ('xccdf_org.ssgproject.', 184),
    (r'_package_\w+_removed', 2),
    ('fips', 1),
    ('audit', 110),
    ('password', 15),
])
def test_search_rules_id(part_of_id_rule, result):
    client = get_client_arf_to_html(part_of_id_rule)
    assert len(client.search_rules_id()) == result
