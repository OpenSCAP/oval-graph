import os
import json
import sys
import mock
import pytest
import uuid
import tempfile
import re

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


def get_random_dir_in_tmp():
    return os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))


def any_get_test_data_json(src):
    with open(get_src(src), 'r') as f:
        return json.load(f)


def any_get_tested_file(src):
    with open(get_src(src), 'r') as f:
        return f.readlines()


def get_Converter_simple_tree():
    return Converter(get_simple_tree())


def any_test_create_node_dict_for_JsTree(tree, json_src):
    data = dict()
    with open(get_src(json_src), "r") as f:
        data = json.load(f)
    assert Converter(tree).to_JsTree_dict() == data


def get_simple_tree():
    return OvalNode(
        node_id=1,
        node_type='operator',
        value='and',
        children=[
            OvalNode(
                node_id=2,
                node_type='value',
                value='true',
            ),
            OvalNode(
                node_id=3,
                node_type='value',
                value='false',
            ),
            OvalNode(
                node_id=4,
                node_type='operator',
                value='or',
                children=[
                    OvalNode(
                        node_id=5,
                        node_type='value',
                        value='false',
                    ),
                    OvalNode(
                        node_id=6,
                        node_type='value',
                        value="true",
                    ),
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


def find_any_node(tree, node_id):
    findTree = tree.find_node_with_ID(node_id)
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
    reference_pattern = any_get_tested_file(
        'test_data/referenc_pattern_html_report.txt')
    start_pattern = False
    count_row = 0
    for row in result_:
        if row == '<script>var data_of_tree = {\n':
            start_pattern = True
        if start_pattern and "xccdforgssgprojectcontentrulepackageabrtremoved" in row:
            row = re.sub(r'[0-9]+', '', row)
        count_row += (1 if start_pattern and row in reference_pattern else 0)
        if row == '};</script><div>\n':
            break
    assert count_row == len(reference_pattern)


def compare_results_json(result):
    result = any_get_test_data_json(result)
    reference_result = any_get_test_data_json(
        'test_data/referenc_result_data_json.json')
    rule_name = "xccdf_org.ssgproject.content_rule_package_abrt_removed"
    result_rule_name = [
        x for x in result.keys() if re.search(
            rule_name, x)]
    assert (result[result_rule_name[0]]
            == reference_result[rule_name])


def _find_all_in_string(regex, count, string):
    assert len(re.findall(regex, string)) == count


def get_questions_not_selected(capsys, client):
    out = client.get_questions()[0].choices
    outResult = [
        'xccdf_org.ssgproject.content_rule_package_abrt_removed',
        'xccdf_org.ssgproject.content_rule_package_sendmail_removed']
    assert out == outResult
    captured = capsys.readouterr()
# Problem with CI when si called function test_arf_to_hml.test_get_question_not_selected
# other calls work with ==.
    regex = r'rule_package_\w+_removed\(Not selected\)'
    _find_all_in_string(regex, 6, captured.out)


def get_questions_not_selected_and_show_failed_rules(capsys, client):
    out = client.get_questions()[0].choices
    outResult = ['xccdf_org.ssgproject.content_rule_package_abrt_removed']
    assert out == outResult
    captured = capsys.readouterr()
    regex = r'rule_package_\w+_removed\(Not selected\)'
    _find_all_in_string(regex, 6, captured.out)


def get_questions_with_option_show_failed_rules(client):
    out = client.get_questions()[0].choices
    rule1 = 'xccdf_org.ssgproject.content_rule_package_abrt_removed'
    assert out[0] == rule1
    with pytest.raises(Exception, match="list index out of range"):
        assert out[2] is None


def if_not_installed_inquirer_with_option_show_failed_rules(capsys, client):
    with mock.patch.dict(sys.modules, {'inquirer': None}):
        out = client.run_gui_and_return_answers()
        assert out is None
        captured = capsys.readouterr()
        assert "inquirer" in captured.out
        regex = r'rule_package_\w+_removed\$'
        _find_all_in_string(regex, 1, captured.out)


def if_not_installed_inquirer_with_option_show_not_selected_rules(
        capsys, client, count_of_selected_rule=2):
    with mock.patch.dict(sys.modules, {'inquirer': None}):
        out = client.run_gui_and_return_answers()
        assert out is None
        captured = capsys.readouterr()
        assert "inquirer" in captured.out
        regex = r'rule_package_\w+_removed\$'
        _find_all_in_string(regex, count_of_selected_rule, captured.out)
        regex = r'rule_package_\w+_removed\(Not selected\)'
        _find_all_in_string(regex, 6, captured.out)


def if_not_installed_inquirer_with_option_show_not_selected_rules_and_show_failed_rules(
        capsys,
        client):
    if_not_installed_inquirer_with_option_show_not_selected_rules(
        capsys, client, 1)


def find_files(file_name, search_path):
    result = []
    for root, dir_, files in os.walk(search_path):
        for filename in files:
            if file_name in filename:
                result.append(os.path.abspath(os.path.join(root, filename)))
    return result


def any_client_if_not_installed_inquirer(client, capsys, regex):
    client.isatty = True

    out = client.run_gui_and_return_answers()
    assert out is None
    captured = capsys.readouterr()
    assert len(re.findall(regex, captured.out)) == 2
