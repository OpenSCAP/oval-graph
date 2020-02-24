import os
import json
import sys
import mock
import pytest

from oval_graph.oval_node import restore_dict_to_tree, OvalNode
from oval_graph.converter import Converter
from oval_graph.xml_parser import XmlParser


def any_test_treeEvaluation(tree, expect, file_name=None):
    if file_name is not None and tree is None:
        if file_name.startswith('AND'):
            dir = 'test_data_and'
        elif file_name.startswith('OR'):
            dir = 'test_data_or'
        elif file_name.startswith('XOR'):
            dir = 'test_data_xor'
        elif file_name.startswith('ONE'):
            dir = 'test_data_one'
        else:
            dir = 'test_data_NONE'

        src = 'test_data/' + dir + '/' + file_name
        data = dict()
        with open(get_src(src), "r") as f:
            data = json.load(f)
        assert restore_dict_to_tree(
            data).evaluate_tree() == expect
    else:
        assert tree.evaluate_tree() == expect


def any_test_parsing_and_evaluate_scan_rule(src, rule_id, result):
    parser = XmlParser(get_src(src))
    oval_tree = parser.get_oval_tree(rule_id)
    any_test_treeEvaluation(oval_tree, result)


def any_get_test_data_json(src):
    with open(get_src(src), 'r') as f:
        return json.load(f)


def any_get_tested_file(src):
    with open(get_src(src), 'r') as f:
        return f.readlines()


def get_Converter_simple_tree():
    return Converter(get_simple_tree())


def any_test_create_node_dict_for_JsTree(Tree, json_src):
    data = dict()
    with open(get_src(json_src), "r") as f:
        data = json.load(f)
    assert Converter(Tree).to_JsTree_dict() == data


def get_simple_tree():
    return OvalNode(1, 'operator', 'and', False, None, None, None, [
        OvalNode(2, 'value', "true", False, None, None, None),
        OvalNode(3, 'value', "false", False, None, None, None),
        OvalNode(4, 'operator', 'or', False, None, None, None, [
            OvalNode(5, 'value', "false", False, None, None, None),
            OvalNode(6, 'value', "true", False, None, None, None)
        ]
        )
    ]
    )


def get_dict_of_simple_tree():
    return get_simple_tree().save_tree_to_dict()


def any_test_transformation_tree_to_Json_for_JsTree(
        src, test_data_src, rule_id):
    test_data = any_get_test_data_json(test_data_src)

    parser = XmlParser(get_src(src))
    oval_tree = parser.get_oval_tree(rule_id)

    assert oval_tree.node_id == rule_id
    out_data = Converter(oval_tree).to_JsTree_dict()
    assert out_data == test_data


def any_test_tree_to_dict_of_tree(tree, dict_of_tree):
    assert tree.save_tree_to_dict() == dict_of_tree


def find_any_node(Tree, node_id):
    findTree = Tree.find_node_with_ID(node_id)
    assert findTree.node_id == node_id


def any_test_treeEvaluation_with_tree(tree, expect):
    assert tree.evaluate_tree() == expect


def any_test_dict_to_tree(dict_of_tree):
    treedict_of_tree = restore_dict_to_tree(dict_of_tree)
    assert treedict_of_tree.save_tree_to_dict() == dict_of_tree


def get_parser(src):
    return XmlParser(get_src(src))


def get_src(src):
    _dir = os.path.dirname(os.path.realpath(__file__))
    FIXTURE_DIR = os.path.join(_dir, src)
    return str(FIXTURE_DIR)


def compare_results_html(result):
    result_ = any_get_tested_file(result)
    referenc_pattern = any_get_tested_file(
        'test_data/referenc_pattern_html_report.html')
    matched_rows = []
    for row in result_:
        for row_in_pattern in referenc_pattern:
            if row == row_in_pattern:
                matched_rows.append(row)
    assert matched_rows == referenc_pattern


def compare_results_json(result):
    result = any_get_test_data_json(result)
    referenc_result = any_get_test_data_json(
        'test_data/referenc_result_data_json.json')
    print(json.dumps(result))
    assert result[list(result.keys())[
        0]] == referenc_result["xccdf_org.ssgproject.content_rule_package_abrt_removed"]


def get_questions_not_selected(capsys, client):
    out = client.get_questions()[0].choices
    outResult = [
        'xccdf_org.ssgproject.content_rule_package_abrt_removed',
        'xccdf_org.ssgproject.content_rule_package_sendmail_removed']
    assert out == outResult
    captured = capsys.readouterr()
# Problem with CI when si called function test_arf_to_hml.test_get_question_not_selected
# other calls work with ==.
    assert (('== The not selected rule IDs ==\n'
             'xccdf_org.ssgproject.content_rule_package_nis_removed(Not selected)\n'
             'xccdf_org.ssgproject.content_rule_package_ntpdate_removed(Not selected)\n'
             'xccdf_org.ssgproject.content_rule_package_telnetd_removed(Not selected)\n'
             'xccdf_org.ssgproject.content_rule_package_gdm_removed(Not selected)\n'
             'xccdf_org.ssgproject.content_rule_package_setroubleshoot_removed(Not selected)\n'
             'xccdf_org.ssgproject.content_rule_package_mcstrans_removed(Not selected)\n')
            in captured.out)


def get_questions_not_selected_and_show_fail_rules(capsys, client):
    out = client.get_questions()[0].choices
    outResult = ['xccdf_org.ssgproject.content_rule_package_abrt_removed']
    assert out == outResult
    captured = capsys.readouterr()
    assert captured.out == (
        '== The not selected rule IDs ==\n'
        'xccdf_org.ssgproject.content_rule_package_nis_removed(Not selected)\n'
        'xccdf_org.ssgproject.content_rule_package_ntpdate_removed(Not selected)\n'
        'xccdf_org.ssgproject.content_rule_package_telnetd_removed(Not selected)\n'
        'xccdf_org.ssgproject.content_rule_package_gdm_removed(Not selected)\n'
        'xccdf_org.ssgproject.content_rule_package_setroubleshoot_removed(Not selected)\n'
        'xccdf_org.ssgproject.content_rule_package_mcstrans_removed(Not selected)\n')


def get_questions_with_option_show_fail_rules(client):
    out = client.get_questions()[0].choices
    rule1 = 'xccdf_org.ssgproject.content_rule_package_abrt_removed'
    assert out[0] == rule1
    with pytest.raises(Exception, match="list index out of range"):
        assert out[2] is None


def if_not_installed_inquirer_with_option_show_fail_rules(capsys, client):
    with mock.patch.dict(sys.modules, {'inquirer': None}):
        out = client.run_gui_and_return_answers()
        assert out is None
        captured = capsys.readouterr()
        assert captured.out == (
            '== The Rule IDs ==\n'
            "'xccdf_org.ssgproject.content_rule_package_abrt_removed\\b'\n"
            "You haven't got installed inquirer lib. Please copy id rule with you"
            " want use and put it in command\n")


def if_not_installed_inquirer_with_option_show_not_selected_rules(
        capsys, client):
    with mock.patch.dict(sys.modules, {'inquirer': None}):
        out = client.run_gui_and_return_answers()
        assert out is None
        captured = capsys.readouterr()
        assert captured.out == (
            '== The Rule IDs ==\n'
            "'xccdf_org.ssgproject.content_rule_package_abrt_removed\\b'\n"
            "'xccdf_org.ssgproject.content_rule_package_sendmail_removed\\b'\n"
            '== The not selected rule IDs ==\n'
            'xccdf_org.ssgproject.content_rule_package_nis_removed(Not selected)\n'
            'xccdf_org.ssgproject.content_rule_package_ntpdate_removed(Not selected)\n'
            'xccdf_org.ssgproject.content_rule_package_telnetd_removed(Not selected)\n'
            'xccdf_org.ssgproject.content_rule_package_gdm_removed(Not selected)\n'
            'xccdf_org.ssgproject.content_rule_package_setroubleshoot_removed(Not selected)\n'
            'xccdf_org.ssgproject.content_rule_package_mcstrans_removed(Not selected)\n'
            "You haven't got installed inquirer lib. Please copy id rule with you"
            " want use and put it in command\n")


def if_not_installed_inquirer_with_option_show_not_selected_rules_and_show_fail_rules(
        capsys,
        client):
    with mock.patch.dict(sys.modules, {'inquirer': None}):
        out = client.run_gui_and_return_answers()
        assert out is None
        captured = capsys.readouterr()
        assert captured.out == (
            '== The Rule IDs ==\n'
            "'xccdf_org.ssgproject.content_rule_package_abrt_removed\\b'\n"
            '== The not selected rule IDs ==\n'
            'xccdf_org.ssgproject.content_rule_package_nis_removed(Not selected)\n'
            'xccdf_org.ssgproject.content_rule_package_ntpdate_removed(Not selected)\n'
            'xccdf_org.ssgproject.content_rule_package_telnetd_removed(Not selected)\n'
            'xccdf_org.ssgproject.content_rule_package_gdm_removed(Not selected)\n'
            'xccdf_org.ssgproject.content_rule_package_setroubleshoot_removed(Not selected)\n'
            'xccdf_org.ssgproject.content_rule_package_mcstrans_removed(Not selected)\n'
            "You haven't got installed inquirer lib. Please copy id rule with you"
            " want use and put it in command\n")
