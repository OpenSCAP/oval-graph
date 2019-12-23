import os
import json

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
    return OvalNode(1, 'operator', 'and', False, None, [
        OvalNode(2, 'value', "true", False, None),
        OvalNode(3, 'value', "false", False, None),
        OvalNode(4, 'operator', 'or', False, None, [
            OvalNode(5, 'value', "false", False, None),
            OvalNode(6, 'value', "true", False, None)
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


def compare_results_js(result):
    result = any_get_tested_file(
        os.path.join(result, 'data.js'))
    referenc_result = any_get_tested_file(
        'test_data/referenc_result_data_tree.js')


def compare_results_json(result):
    result = any_get_test_data_json(result)
    referenc_result = any_get_test_data_json(
        'test_data/referenc_result_data_json.json')
    assert result[list(result.keys())[
        0]] == referenc_result["xccdf_org.ssgproject.content_rule_package_abrt_removed"]
