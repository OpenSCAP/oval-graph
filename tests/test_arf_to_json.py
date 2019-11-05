import pytest
import tempfile
import os
import uuid


from oval_graph.arf_to_json import ArfToJson
import tests.any_test_help


def get_client_arf_to_json(src, rule):
    return ArfToJson(
        [tests.any_test_help.get_src(src), rule])


def get_client_arf_to_json_with_define_dest(src, rule):
    return ArfToJson(["--out",
                      tests.any_test_help.get_src(os.path.join(tempfile.gettempdir(),
                                                               str(uuid.uuid4()))),
                      tests.any_test_help.get_src(src),
                      rule])


def try_expection_for_prepare_graph(src, rule, err):
    client = get_client_arf_to_json(src, rule)
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


def test_prepare_json(capsys):
    src = 'test_data/ssg-fedora-ds-arf.xml'
    rule = 'xccdf_org.ssgproject.content_rule_package_abrt_removed'
    client = get_client_arf_to_json(src, rule)
    rules = {'rules': [rule]}
    results_src = client.prepare_data(rules)
    assert not results_src
    captured = capsys.readouterr()
    print(repr(captured.out))
    assert captured.out == (
        '{\n'
        '    "node_id": "xccdf_org.ssgproject.content_rule_package_abrt_removed",\n'
        '    "type": "operator",\n'
        '    "value": "and",\n'
        '    "negation": false,\n'
        '    "comment": "Package abrt Removed",\n'
        '    "child": [\n'
        '        {\n'
        '            "node_id": "oval:ssg-package_abrt_removed:def:1",\n'
        '            "type": "operator",\n'
        '            "value": "and",\n'
        '            "negation": false,\n'
        '            "comment": null,\n'
        '            "child": [\n'
        '                {\n'
        '                    "node_id": "oval:ssg-test_package_abrt_removed:tst:1",\n'
        '                    "type": "value",\n'
        '                    "value": "false",\n'
        '                    "negation": false,\n'
        '                    "comment": "package abrt is removed",\n'
        '                    "child": null\n'
        '                }\n'
        '            ]\n'
        '        }\n'
        '    ]\n'
        '}\n')


def test_prepare_json_and_save_in_defined_destination():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    rule = 'xccdf_org.ssgproject.content_rule_package_abrt_removed'
    client = get_client_arf_to_json_with_define_dest(src, rule)
    rules = {'rules': [rule]}
    results_src = client.prepare_data(rules)
    tests.any_test_help.compare_results_json(results_src[0])
