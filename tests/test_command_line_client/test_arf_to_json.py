import pytest
import tempfile
import os
import uuid
import json
import mock
import sys
from datetime import datetime
import time

from oval_graph.command_line_client.arf_to_json import ArfToJson
import tests.any_test_help


def get_client_arf_to_json(src, rule):
    return ArfToJson(
        [tests.any_test_help.get_src(src), rule])


def get_client_arf_to_json_with_define_dest(src, rule, out_src=None):
    out_src = str(uuid.uuid4()) + ".json" if out_src is None else out_src
    return ArfToJson(["--output",
                      tests.any_test_help.get_src(os.path.join(tempfile.gettempdir(), out_src)),
                      tests.any_test_help.get_src(src),
                      rule])


def get_client_arf_to_json_with_option_show_failed_rules(src, rule):
    return ArfToJson(["--show-failed-rules",
                      tests.any_test_help.get_src(src), rule])


def get_client_arf_to_json_with_option_show_not_selected_rules(src, rule):
    return ArfToJson(["--show-not-selected-rules",
                      tests.any_test_help.get_src(src),
                      rule])


def get_client_arf_to_json_with_option_show_not_selected_rules_and_show_failed_rules(
        src,
        rule):
    return ArfToJson(["--show-not-selected-rules",
                      "--show-failed-rules",
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
    assert captured.out == (
        '{\n'
        '    "xccdf_org.ssgproject.content_rule_package_abrt_removed' +
        client.date +
        '": {\n'
        '        "node_id": "xccdf_org.ssgproject.content_rule_package_abrt_removed",\n'
        '        "type": "operator",\n'
        '        "value": "and",\n'
        '        "negation": false,\n'
        '        "comment": "Package abrt Removed",\n'
        '        "tag": "Rule",\n'
        '        "test_result_details": null,\n'
        '        "child": [\n'
        '            {\n'
        '                "node_id": "oval:ssg-package_abrt_removed:def:1",\n'
        '                "type": "operator",\n'
        '                "value": "and",\n'
        '                "negation": false,\n'
        '                "comment": "The RPM package abrt should be removed.",\n'
        '                "tag": "Definition",\n'
        '                "test_result_details": null,\n'
        '                "child": [\n'
        '                    {\n'
        '                        "node_id": "oval:ssg-test_package_abrt_removed:tst:1",\n'
        '                        "type": "value",\n'
        '                        "value": "false",\n'
        '                        "negation": false,\n'
        '                        "comment": "package abrt is removed",\n'
        '                        "tag": "Test",\n'
        '                        "test_result_details": {\n'
        '                            "id": "oval:ssg-test_package_abrt_removed:tst:1",\n'
        '                            "comment": "package abrt is removed",\n'
        '                            "objects": [\n'
        '                                {\n'
        '                                    "oval:ssg-obj_package_abrt_removed:obj:1":'
        ' "complete",\n'
        '                                    "rpminfo_object": {\n'
        '                                        "name": "abrt",\n'
        '                                        "arch": "x86_64",\n'
        '                                        "epoch": "(none)",\n'
        '                                        "release": "2.fc30",\n'
        '                                        "version": "2.12.0",\n'
        '                                        "evr": "0:2.12.0-2.fc30",\n'
        '                                        "signature_keyid": "ef3c111fcfc659b9",\n'
        '                                        "extended_name":'
        ' "abrt-0:2.12.0-2.fc30.x86_64"\n'
        '                                    }\n'
        '                                }\n'
        '                            ]\n'
        '                        },\n'
        '                        "child": null\n'
        '                    }\n'
        '                ]\n'
        '            }\n'
        '        ]\n'
        '    }\n'
        '}\n')


def test_prepare_json_and_save_in_defined_destination():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    rule = 'xccdf_org.ssgproject.content_rule_package_abrt_removed'
    client = get_client_arf_to_json_with_define_dest(src, rule)
    rules = {'rules': [rule]}
    results_src = client.prepare_data(rules)
    tests.any_test_help.compare_results_json(results_src[0])


def test_is_empty_file():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    rule = 'xccdf_org.ssgproject.content_rule_package_abrt_removed'
    client = get_client_arf_to_json_with_define_dest(src, rule)
    empty_file_src = tests.any_test_help.get_src('test_data/empty_file.json')
    assert client.file_is_empty(empty_file_src)


def test_if_file_has_content():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    rule = 'xccdf_org.ssgproject.content_rule_package_abrt_removed'
    client = get_client_arf_to_json_with_define_dest(src, rule)
    file_src = tests.any_test_help.get_src('test_data/JsTree_json0.json')
    assert not client.file_is_empty(file_src)


def test_creation_json_with_two_more_rule():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    rule = 'xccdf_org.ssgproject.content_rule_package_abrt_removed'
    client = get_client_arf_to_json_with_define_dest(src, rule)
    rules = {'rules': [rule]}
    result_src = client.prepare_data(rules)
    time.sleep(1)  # wait for change time in saved rule name
    client1 = get_client_arf_to_json_with_define_dest(src, rule, result_src[0])
    result_src_second_rule = client1.prepare_data(rules)
    assert result_src == result_src_second_rule
    data = None
    with open(result_src[-1], 'r') as f:
        data = json.load(f)
    rules_id = list(data.keys())
    assert len(rules_id) == 2
    assert data[rules_id[0]] == data[rules_id[1]]
    referenc_result = tests.any_test_help.any_get_test_data_json(
        'test_data/referenc_result_data_json.json')
    assert referenc_result[
        "xccdf_org.ssgproject.content_rule_package_abrt_removed"] == data[rules_id[0]]


def test_creation_json_two_selected_rules():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    rule = 'xccdf_org.ssgproject.content_rule_package_abrt_removed'
    rule1 = 'xccdf_org.ssgproject.content_rule_disable_host_auth'
    client = get_client_arf_to_json_with_define_dest(src, rule)
    rules = {'rules': [rule, rule1]}
    result_src = client.prepare_data(rules)
    data = None
    with open(result_src[-1], 'r') as f:
        data = json.load(f)
    rules_id = list(data.keys())
    assert len(rules_id) == 2
    referenc_result = tests.any_test_help.any_get_test_data_json(
        'test_data/referenc_result_data_json.json')
    assert referenc_result[
        "xccdf_org.ssgproject.content_rule_package_abrt_removed"] == data[rules_id[0]]
    assert rule1 in rules_id[1]


def test_get_questions_not_selected(capsys):
    src = 'test_data/ssg-fedora-ds-arf.xml'
    regex = r'_package_\w+_removed'
    client = get_client_arf_to_json_with_option_show_not_selected_rules(
        src, regex)
    tests.any_test_help.get_questions_not_selected(capsys, client)


def test_get_questions_not_selected_and_show_failed_rules(capsys):
    src = 'test_data/ssg-fedora-ds-arf.xml'
    regex = r'_package_\w+_removed'
    client = get_client_arf_to_json_with_option_show_not_selected_rules_and_show_failed_rules(
        src, regex)
    tests.any_test_help.get_questions_not_selected_and_show_failed_rules(
        capsys, client)


def test_get_questions_with_option_show_failed_rules():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    regex = r'_package_\w+_removed'
    client = get_client_arf_to_json_with_option_show_failed_rules(src, regex)
    tests.any_test_help.get_questions_with_option_show_failed_rules(client)


def test_if_not_installed_inquirer_with_option_show_failed_rules(capsys):
    with mock.patch.dict(sys.modules, {'inquirer': None}):
        src = 'test_data/ssg-fedora-ds-arf.xml'
        regex = r'_package_\w+_removed'
        client = get_client_arf_to_json_with_option_show_failed_rules(
            src, regex)
        client.isatty = True
        tests.any_test_help.if_not_installed_inquirer_with_option_show_failed_rules(
            capsys, client)


def test_if_not_installed_inquirer_with_option_show_not_selected_rules(
        capsys):
    with mock.patch.dict(sys.modules, {'inquirer': None}):
        src = 'test_data/ssg-fedora-ds-arf.xml'
        regex = r'_package_\w+_removed'
        client = get_client_arf_to_json_with_option_show_not_selected_rules(
            src, regex)
        client.isatty = True
        tests.any_test_help.if_not_installed_inquirer_with_option_show_not_selected_rules(
            capsys, client)


def test_if_not_installed_inquirer_with_option_show_not_selected_rules_and_show_failed_rules(
        capsys):
    with mock.patch.dict(sys.modules, {'inquirer': None}):
        src = 'test_data/ssg-fedora-ds-arf.xml'
        regex = r'_package_\w+_removed'
        client = get_client_arf_to_json_with_option_show_not_selected_rules_and_show_failed_rules(
            src, regex)
        client.isatty = True
        (tests.any_test_help.
         if_not_installed_inquirer_with_option_show_not_selected_rules_and_show_failed_rules(
             capsys, client))
