import graph.oval_graph
import os
import py
import json

def any_test_treeEvaluation(tree, expect):
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
    return graph.oval_graph.OvalNode(1, 'operator', 'and', [
        graph.oval_graph.OvalNode(2, 'value', "true"),
        graph.oval_graph.OvalNode(3, 'value', "false"),
        graph.oval_graph.OvalNode(4, 'operator', 'or', [
            graph.oval_graph.OvalNode(5, 'value', "false"),
            graph.oval_graph.OvalNode(6, 'value', "true")
        ]
        )
    ]
    )


def get_dict_of_simple_tree():
    return get_simple_tree().save_tree_to_dict()
