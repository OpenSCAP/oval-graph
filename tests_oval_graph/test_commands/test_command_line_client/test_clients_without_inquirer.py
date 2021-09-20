import pytest

from ...test_tools import TestTools
from .test_client_arf_to_html import get_client_arf_to_html
from .test_client_arf_to_json import get_client_arf_to_json
from .test_client_json_to_html import get_client_json_to_html


@pytest.mark.parametrize("get_client, args, rules_count, not_selected_rules_count", [
    (
        get_client_arf_to_html,
        ["--show-failed-rules"],
        1, 0,
    ),
    (
        get_client_arf_to_html,
        ["--show-not-selected-rules"],
        2, 6,
    ),
    (
        get_client_arf_to_html,
        ["--show-failed-rules", "--show-not-selected-rules"],
        1, 6,
    ),
    (
        get_client_arf_to_html,
        [],
        2, 0,
    ),
    (
        get_client_arf_to_json,
        ["--show-failed-rules"],
        1, 0,
    ),
    (
        get_client_arf_to_json,
        ["--show-not-selected-rules"],
        2, 6,
    ),
    (
        get_client_arf_to_json,
        ["--show-failed-rules", "--show-not-selected-rules"],
        1, 6,
    ),
    (
        get_client_arf_to_json,
        [],
        2, 0,
    ),
    (
        get_client_json_to_html,
        [],
        2, 0,
    ),
])
def test_get_gui_with_parameters(
        capsys, get_client, args, rules_count, not_selected_rules_count):
    rule = r'_package_\w+_removed'
    client = get_client(rule, args)
    client.isatty = True
    out = client.run_gui_and_return_answers()
    assert out is None
    captured = capsys.readouterr()
    regex = r'rule_package_\w+_removed\$'
    TestTools.find_all_in_string(regex, rules_count, captured.out)
    regex = r'rule_package_\w+_removed +\(Not selected\)'
    TestTools.find_all_in_string(regex, not_selected_rules_count, captured.out)
