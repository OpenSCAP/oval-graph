import graph.oval_graph
import os
import py
import json


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
        _dir = os.path.dirname(os.path.realpath(__file__))
        FIXTURE_DIR = py.path.local(_dir) / src
        data = dict()
        with open(str(FIXTURE_DIR), "r") as f:
            data = json.load(f)
        assert graph.oval_graph.restore_dict_to_tree(
            data).evaluate_tree() == expect
    else:
        assert tree.evaluate_tree() == expect


def any_test_parsing_and_evaluate_scan_rule(src, rule_id, result):
    _dir = os.path.dirname(os.path.realpath(__file__))
    FIXTURE_DIR = py.path.local(_dir) / src

    oval_tree = graph.oval_graph.build_nodes_form_xml(
        str(FIXTURE_DIR), rule_id)
    any_test_treeEvaluation(oval_tree, result)


def any_get_test_data_json(src):
    _dir = os.path.dirname(os.path.realpath(__file__))
    FIXTURE_DIR = py.path.local(_dir) / src

    with open(str(FIXTURE_DIR), 'r') as f:
        data = json.load(f)
    return data


def any_test_create_node_dict_for_sigmaJs(Tree, out):
    assert Tree._create_node(0, 0) == out


def get_simple_tree():
    return graph.oval_graph.OvalNode(1, 'operator', 'and', False, [
        graph.oval_graph.OvalNode(2, 'value', "true", False),
        graph.oval_graph.OvalNode(3, 'value', "false", False),
        graph.oval_graph.OvalNode(4, 'operator', 'or', False, [
            graph.oval_graph.OvalNode(5, 'value', "false", False),
            graph.oval_graph.OvalNode(6, 'value', "true", False)
        ]
        )
    ]
    )


def get_dict_of_simple_tree():
    return get_simple_tree().save_tree_to_dict()


def any_test_transformation_tree_to_Json_for_SigmaJs(
        src, test_data_src, rule_id):
    test_data = any_get_test_data_json(test_data_src)

    oval_tree = graph.oval_graph.build_nodes_form_xml(src, rule_id)

    if oval_tree.node_id == rule_id:
        out_data = oval_tree.to_sigma_dict(0, 0)
        for i in range(len(out_data['nodes'])):
            assert out_data['nodes'][i]['label'] == test_data['nodes'][i]['label']
            assert out_data['nodes'][i]['text'] == test_data['nodes'][i]['text']
            assert out_data['nodes'][i]['url'] == test_data['nodes'][i]['url']


def any_test_tree_to_dict_of_tree(tree, dict_of_tree):
    assert tree.save_tree_to_dict() == dict_of_tree


def find_any_node(Tree, node_id):
    findTree = Tree.find_node_with_ID(node_id)
    assert findTree.node_id == node_id


def any_test_treeEvaluation_with_tree(tree, expect):
    assert tree.evaluate_tree() == expect


def any_test_dict_to_tree(dict_of_tree):
    treedict_of_tree = graph.oval_graph.restore_dict_to_tree(dict_of_tree)
    assert treedict_of_tree.save_tree_to_dict() == dict_of_tree
