import pytest

from oval_graph.command_line_client.client import Client

from .constants_for_tests import PATH_TO_ARF_REPORT


def get_client(rule, optional_args=None):
    path = str(PATH_TO_ARF_REPORT)
    args = [path, rule]
    if optional_args is not None:
        args.extend(optional_args)
    return Client(args)


def test_search_rules_id_not_implemented_error():
    part_of_id_rule = 'xccdf_org.ssgproject.'
    client = get_client(part_of_id_rule)
    with pytest.raises(NotImplementedError):
        assert client.search_rules_id()


def test_get_only_fail_rules_not_implemented_error():
    part_of_id_rule = 'xccdf_org.ssgproject.'
    client = get_client(part_of_id_rule)
    with pytest.raises(NotImplementedError):
        assert client.get_only_fail_rule(['rule-id'])
