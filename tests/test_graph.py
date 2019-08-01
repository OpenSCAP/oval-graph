import graph.oval_graph
import graph.evaluate 
import graph.xml_parser
import pytest
import os
import py


results_counts = {
    'true_cnt': -1,
    'false_cnt': -1,
    'error_cnt': -1,
    'unknown_cnt': -1,
    'noteval_cnt': -1,
    'notappl_cnt': -1
}


def test_bad_tree():
    with pytest.raises(ValueError) as e:
        badTree()
    assert str(
        e.value) == 'err- true, false, error, unknown. noteval, notappl have not child!'

    with pytest.raises(ValueError) as e:
        treeOnlyAnd()
    assert str(e.value) == 'err- OR, XOR, ONE, AND have child!'

    with pytest.raises(ValueError) as e:
        treeOnlyOr()
    assert str(e.value) == 'err- OR, XOR, ONE, AND have child!'

    with pytest.raises(ValueError) as e:
        treeWithBadType()
    assert str(e.value) == 'err- unknown type'

    with pytest.raises(ValueError) as e:
        treeWithBadValueOfOperator()
    assert str(e.value) == 'err- unknown operator'

    with pytest.raises(ValueError) as e:
        treeWithBadValueOfValue()
    assert str(e.value) == 'err- unknown value'


# degenered trees

def badTree():
    """
         t
         |
        and
         |
         t
    """
    t = graph.oval_graph.OvalNode(
        1, "value", "true", [
            graph.oval_graph.OvalNode(
                2, "operator", "and", [
                    graph.oval_graph.OvalNode(
                        3, "value", "true")])])
    return


def treeOnlyOr():
    """
        or
    """
    Tree = graph.oval_graph.OvalNode(1, "operator", 'or')
    return


def treeOnlyAnd():
    """
        and
    """
    Tree = graph.oval_graph.OvalNode(1, "operator", 'and')
    return


def treeWithBadValueOfOperator():
    Tree = graph.oval_graph.OvalNode(1, "operator", 'nad')
    return


def treeWithBadValueOfValue():
    Tree = graph.oval_graph.OvalNode(1, "value", 'and')
    return


def treeWithBadType():
    Tree = graph.oval_graph.OvalNode(1, "auto", 'and')
    return

# normal trees


def test_UPPERCASETree():
    t = graph.oval_graph.OvalNode(
        1, "OPERATOR", "AND", [
            graph.oval_graph.OvalNode(
                2, "VALUE", "TRUE",), graph.oval_graph.OvalNode(
                3, "VALUE", "NOTAPPL")])

# AND operator


def test_ANDTreeTrue():
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'and', [
        graph.oval_graph.OvalNode(2, 'value', "true"),
        graph.oval_graph.OvalNode(3, 'value', "true"),
        graph.oval_graph.OvalNode(4, 'value', "notappl")
    ]
    )

    any_test_treeEvaluation(Tree, "true")


def test_ANDTreeFalse():
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'and', [
        graph.oval_graph.OvalNode(2, 'value', "false"),
        graph.oval_graph.OvalNode(3, 'value', "false"),

        graph.oval_graph.OvalNode(4, 'value', "true"),
        graph.oval_graph.OvalNode(5, 'value', "error"),
        graph.oval_graph.OvalNode(6, 'value', "unknown"),
        graph.oval_graph.OvalNode(7, 'value', "noteval"),
        graph.oval_graph.OvalNode(8, 'value', "notappl")
    ]
    )

    any_test_treeEvaluation(Tree, "false")


def test_ANDTreeError():
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'and', [
                graph.oval_graph.OvalNode(2, 'value', "error"),
                graph.oval_graph.OvalNode(3, 'value', "error"),
                graph.oval_graph.OvalNode(4, 'value', "true"),
                graph.oval_graph.OvalNode(5, 'value', "unknown"),
                graph.oval_graph.OvalNode(6, 'value', "noteval"),
                graph.oval_graph.OvalNode(7, 'value', "notappl"),
                graph.oval_graph.OvalNode(8, 'value', "error")
                ])

    any_test_treeEvaluation(Tree, "error")


def test_ANDTreeUnknown():
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'and', [
                graph.oval_graph.OvalNode(2, 'value', "unknown"),
                graph.oval_graph.OvalNode(3, 'value', "unknown"),
                graph.oval_graph.OvalNode(4, 'value', "true"),
                graph.oval_graph.OvalNode(5, 'value', "unknown"),
                graph.oval_graph.OvalNode(6, 'value', "noteval"),
                graph.oval_graph.OvalNode(7, 'value', "notappl"),
                graph.oval_graph.OvalNode(8, 'value', "notappl")
                ]
                )

    any_test_treeEvaluation(Tree, "unknown")


def test_ANDTreeNoteval():
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'and', [
                graph.oval_graph.OvalNode(2, 'value', "noteval"),
                graph.oval_graph.OvalNode(3, 'value', "noteval"),
                graph.oval_graph.OvalNode(4, 'value', "true"),
                graph.oval_graph.OvalNode(5, 'value', "true"),
                graph.oval_graph.OvalNode(6, 'value', "noteval"),
                graph.oval_graph.OvalNode(7, 'value', "notappl"),
                graph.oval_graph.OvalNode(8, 'value', "notappl")
                ]
                )

    any_test_treeEvaluation(Tree, "noteval")


def test_ANDTreeNotappl():
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'and', [
        graph.oval_graph.OvalNode(2, 'value', "notappl"),
        graph.oval_graph.OvalNode(3, 'value', "notappl"),
        graph.oval_graph.OvalNode(4, 'value', "notappl")
    ]
    )

    any_test_treeEvaluation(Tree, "notappl")

# ONE operator


def test_ONETreeTrue():
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'one', [
        graph.oval_graph.OvalNode(2, 'value', "true"),
        graph.oval_graph.OvalNode(3, 'value', "false"),
        graph.oval_graph.OvalNode(4, 'value', "notappl"),
        graph.oval_graph.OvalNode(5, 'value', "false")
    ]
    )

    any_test_treeEvaluation(Tree, "true")


def test_ONETreeFalse():
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'one', [
        graph.oval_graph.OvalNode(2, 'value', "true"),
        graph.oval_graph.OvalNode(3, 'value', "true"),

        graph.oval_graph.OvalNode(4, 'value', "false"),
        graph.oval_graph.OvalNode(5, 'value', "error"),
        graph.oval_graph.OvalNode(6, 'value', "unknown"),
        graph.oval_graph.OvalNode(7, 'value', "noteval"),
        graph.oval_graph.OvalNode(8, 'value', "notappl")
    ]
    )

    any_test_treeEvaluation(Tree, "false")


def test_ONETreeFalse1():
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'one', [
        graph.oval_graph.OvalNode(2, 'value', "false"),
        graph.oval_graph.OvalNode(3, 'value', "false"),
        graph.oval_graph.OvalNode(4, 'value', "notappl")
    ]
    )

    any_test_treeEvaluation(Tree, "false")


def test_ONETreeError():
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'one', [
                graph.oval_graph.OvalNode(2, 'value', "error"),
                graph.oval_graph.OvalNode(3, 'value', "error"),
                graph.oval_graph.OvalNode(4, 'value', "true"),
                graph.oval_graph.OvalNode(5, 'value', "unknown"),
                graph.oval_graph.OvalNode(6, 'value', "noteval"),
                graph.oval_graph.OvalNode(7, 'value', "notappl"),
                graph.oval_graph.OvalNode(8, 'value', "false")
                ]
                )

    any_test_treeEvaluation(Tree, "error")


def test_ONETreeUnknown():
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'one', [
                graph.oval_graph.OvalNode(2, 'value', "unknown"),
                graph.oval_graph.OvalNode(3, 'value', "unknown"),
                graph.oval_graph.OvalNode(4, 'value', "true"),
                graph.oval_graph.OvalNode(5, 'value', "unknown"),
                graph.oval_graph.OvalNode(6, 'value', "noteval"),
                graph.oval_graph.OvalNode(7, 'value', "notappl"),
                graph.oval_graph.OvalNode(8, 'value', "false")
                ])

    any_test_treeEvaluation(Tree, "unknown")


def test_ONETreeNoteval():
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'one', [
                graph.oval_graph.OvalNode(2, 'value', "noteval"),
                graph.oval_graph.OvalNode(3, 'value', "noteval"),
                graph.oval_graph.OvalNode(4, 'value', "true"),
                graph.oval_graph.OvalNode(5, 'value', "false"),
                graph.oval_graph.OvalNode(6, 'value', "noteval"),
                graph.oval_graph.OvalNode(7, 'value', "notappl"),
                graph.oval_graph.OvalNode(8, 'value', "notappl")
                ]
                )

    any_test_treeEvaluation(Tree, "noteval")


def test_ONETreeNotappl():
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'one', [
        graph.oval_graph.OvalNode(2, 'value', "notappl"),
        graph.oval_graph.OvalNode(3, 'value', "notappl"),
        graph.oval_graph.OvalNode(4, 'value', "notappl")
    ]
    )

    any_test_treeEvaluation(Tree, "notappl")

# OR operator


def test_ORTreeTrue():
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'or', [
        graph.oval_graph.OvalNode(2, 'value', "true"),
        graph.oval_graph.OvalNode(3, 'value', "false"),

        graph.oval_graph.OvalNode(4, 'value', "true"),
        graph.oval_graph.OvalNode(5, 'value', "error"),
        graph.oval_graph.OvalNode(6, 'value', "unknown"),
        graph.oval_graph.OvalNode(7, 'value', "noteval"),
        graph.oval_graph.OvalNode(8, 'value', "notappl")
    ]
    )

    any_test_treeEvaluation(Tree, "true")


def test_ORTreeFalse():
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'or', [
        graph.oval_graph.OvalNode(2, 'value', "false"),
        graph.oval_graph.OvalNode(3, 'value', "false"),
        graph.oval_graph.OvalNode(4, 'value', "notappl")
    ]
    )

    any_test_treeEvaluation(Tree, "false")


def test_ORTreeError():
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'or', [
                graph.oval_graph.OvalNode(2, 'value', "error"),
                graph.oval_graph.OvalNode(3, 'value', "error"),
                graph.oval_graph.OvalNode(4, 'value', "false"),
                graph.oval_graph.OvalNode(5, 'value', "unknown"),
                graph.oval_graph.OvalNode(6, 'value', "noteval"),
                graph.oval_graph.OvalNode(7, 'value', "notappl"),
                graph.oval_graph.OvalNode(8, 'value', "error")
                ]
                )

    any_test_treeEvaluation(Tree, "error")


def test_ORTreeUnknown():
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'or', [
                graph.oval_graph.OvalNode(2, 'value', "unknown"),
                graph.oval_graph.OvalNode(3, 'value', "unknown"),
                graph.oval_graph.OvalNode(4, 'value', "false"),
                graph.oval_graph.OvalNode(5, 'value', "unknown"),
                graph.oval_graph.OvalNode(6, 'value', "noteval"),
                graph.oval_graph.OvalNode(7, 'value', "notappl"),
                graph.oval_graph.OvalNode(8, 'value', "notappl")
                ]
                )

    any_test_treeEvaluation(Tree, "unknown")


def test_ORTreeNoteval():
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'or', [
                graph.oval_graph.OvalNode(2, 'value', "noteval"),
                graph.oval_graph.OvalNode(3, 'value', "noteval"),
                graph.oval_graph.OvalNode(4, 'value', "false"),
                graph.oval_graph.OvalNode(5, 'value', "false"),
                graph.oval_graph.OvalNode(6, 'value', "noteval"),
                graph.oval_graph.OvalNode(7, 'value', "notappl"),
                graph.oval_graph.OvalNode(8, 'value', "notappl")
                ]
                )

    any_test_treeEvaluation(Tree, "noteval")


def test_ORTreeNotappl():
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'or', [
        graph.oval_graph.OvalNode(2, 'value', "notappl"),
        graph.oval_graph.OvalNode(3, 'value', "notappl"),
        graph.oval_graph.OvalNode(4, 'value', "notappl")
    ]
    )

    any_test_treeEvaluation(Tree, "notappl")

# XOR operator


def test_XORTreeTrue():
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'xor', [
        graph.oval_graph.OvalNode(2, 'value', "true"),
        graph.oval_graph.OvalNode(3, 'value', "false"),

        graph.oval_graph.OvalNode(4, 'value', "false"),
        graph.oval_graph.OvalNode(5, 'value', "false"),
        graph.oval_graph.OvalNode(6, 'value', "true"),
        graph.oval_graph.OvalNode(7, 'value', "true"),
        graph.oval_graph.OvalNode(8, 'value', "notappl")
    ]
    )

    any_test_treeEvaluation(Tree, "true")


def test_XORTreeFalse():
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'xor', [
        graph.oval_graph.OvalNode(2, 'value', "true"),
        graph.oval_graph.OvalNode(3, 'value', "false"),

        graph.oval_graph.OvalNode(4, 'value', "false"),
        graph.oval_graph.OvalNode(5, 'value', "true"),
        graph.oval_graph.OvalNode(6, 'value', "true"),
        graph.oval_graph.OvalNode(7, 'value', "true"),
        graph.oval_graph.OvalNode(8, 'value', "notappl")
    ]
    )

    any_test_treeEvaluation(Tree, "false")


def test_XORTreeError():
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'xor', [
                graph.oval_graph.OvalNode(2, 'value', "error"),
                graph.oval_graph.OvalNode(3, 'value', "error"),
                graph.oval_graph.OvalNode(4, 'value', "true"),
                graph.oval_graph.OvalNode(5, 'value', "unknown"),
                graph.oval_graph.OvalNode(6, 'value', "noteval"),
                graph.oval_graph.OvalNode(7, 'value', "notappl"),
                graph.oval_graph.OvalNode(8, 'value', "false")
                ]
                )

    any_test_treeEvaluation(Tree, "error")


def test_xORTreeUnknown():
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'xor', [
                graph.oval_graph.OvalNode(2, 'value', "unknown"),
                graph.oval_graph.OvalNode(3, 'value', "unknown"),
                graph.oval_graph.OvalNode(4, 'value', "true"),
                graph.oval_graph.OvalNode(5, 'value', "unknown"),
                graph.oval_graph.OvalNode(6, 'value', "noteval"),
                graph.oval_graph.OvalNode(7, 'value', "notappl"),
                graph.oval_graph.OvalNode(8, 'value', "notappl")
                ]
                )

    any_test_treeEvaluation(Tree, "unknown")


def test_XORTreeNoteval():
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'xor', [
                graph.oval_graph.OvalNode(2, 'value', "noteval"),
                graph.oval_graph.OvalNode(3, 'value', "noteval"),
                graph.oval_graph.OvalNode(4, 'value', "true"),
                graph.oval_graph.OvalNode(5, 'value', "true"),
                graph.oval_graph.OvalNode(6, 'value', "noteval"),
                graph.oval_graph.OvalNode(7, 'value', "notappl"),
                graph.oval_graph.OvalNode(8, 'value', "notappl")
                ]
                )

    any_test_treeEvaluation(Tree, "noteval")


def test_XORTreeNotappl():
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'xor', [
        graph.oval_graph.OvalNode(2, 'value', "notappl"),
        graph.oval_graph.OvalNode(3, 'value', "notappl"),
        graph.oval_graph.OvalNode(4, 'value', "notappl")
    ]
    )

    any_test_treeEvaluation(Tree, "notappl")


def test_bigOvalTree():
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'and', [
                graph.oval_graph.OvalNode(2, 'value', "false"),
                graph.oval_graph.OvalNode(3, 'operator', "xor", [
                            graph.oval_graph.OvalNode(4, 'value', 'true'),
                            graph.oval_graph.OvalNode(5, 'operator', 'one', [
                                        graph.oval_graph.OvalNode(6, 'value', 'noteval'),
                                        graph.oval_graph.OvalNode(7, 'value', 'true'), 
                                        graph.oval_graph.OvalNode(8, 'value', 'notappl')
                                        ]
                                        ),
                            graph.oval_graph.OvalNode(9, 'value', 'error')
                            ]
                            ),
                graph.oval_graph.OvalNode(10, 'operator', 'or', [
                                        graph.oval_graph.OvalNode(11, 'value', "unknown"),
                                        graph.oval_graph.OvalNode(12, 'value', "true")
                                        ]
                                        )
                ]
                )

    dict_of_tree = {'node_id': 1, 'type': 'operator', 'value': 'and',
                    'child': [
                        {'node_id': 2, 'type': 'value', 'value': "false", 'child':  None},
                        {'node_id': 3, 'type': 'operator', 'value': "xor", 'child': [
                            {'node_id': 4, 'type': 'value', 'value': "true", 'child':  None},
                            {'node_id': 5, 'type': 'operator', 'value': "one", 'child': [
                                {'node_id': 6, 'type': 'value', 'value': "noteval", 'child':  None},
                                {'node_id': 7, 'type': 'value', 'value': "true", 'child':  None},
                                {'node_id': 8, 'type': 'value', 'value': "notappl", 'child':  None}
                            ]},
                            {'node_id': 9, 'type': 'value', 'value': "error", 'child':  None}]},
                        {'node_id': 10, 'type': 'operator', 'value': 'or', 'child': [
                            {'node_id': 11, 'type': 'value', 'value': "unknown", 'child':  None},
                            {'node_id': 12, 'type': 'value', 'value': "true", 'child':  None}
                        ]
                        }
                    ]
                    }

    any_test_treeEvaluation(Tree, "false")
    any_test_tree_to_dict_of_tree(Tree, dict_of_tree)
    find_any_node(Tree, 5)
    any_test_dict_to_tree(dict_of_tree)

###################################################


def any_test_tree_to_dict_of_tree(tree, dict_of_tree):
    assert tree.save_tree_to_dict() == dict_of_tree


def find_any_node(Tree, node_id):
    findTree = Tree.find_node_with_ID(node_id)
    assert findTree.node_id == node_id


def any_test_treeEvaluation(tree, expect):
    assert tree.evaluate_tree() == expect


def any_test_dict_to_tree(dict_of_tree):
    treedict_of_tree = graph.oval_graph.restore_dict_to_tree(dict_of_tree)
    assert treedict_of_tree.save_tree_to_dict() == dict_of_tree


def test_treeRepr():
    """
        and
         |
         f
    """
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'and', [
        graph.oval_graph.OvalNode(2, 'value', "false")
    ]
    )
    assert str(Tree) == "and"


def test_add_to_tree():
    """
        and
         |
         f
    """

    dict_of_tree = {'node_id': 1,
                    'type': 'operator',
                    'value': 'and',
                    'child': [{'node_id': 2,
                               'type': 'value',
                               'value': "false",
                               'child':  None},
                              {'node_id': 3,
                               'type': 'value',
                               'value': "true",
                               'child':  None},
                              ]}

    Tree = graph.oval_graph.OvalNode(1, 'operator', 'and', [
        graph.oval_graph.OvalNode(2, 'value', "false")
    ]
    )
    Tree1 = graph.oval_graph.OvalNode(3, 'value', "true")
    Tree.add_to_tree(1, Tree1)
    assert Tree.save_tree_to_dict() == dict_of_tree


def test_ChangeValueTree():
    """
        and
        /|\
       t t or
          / \
         f   t
    """
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'and', [
        graph.oval_graph.OvalNode(2, 'value', "true"),
        graph.oval_graph.OvalNode(3, 'value', "false"),
        graph.oval_graph.OvalNode(4, 'operator', 'or', [
            graph.oval_graph.OvalNode(5, 'value', "false"),
            graph.oval_graph.OvalNode(6, 'value', "true")
        ]
        )
    ]
    )

    Tree.change_tree_value(3, "true")
    any_test_treeEvaluation(Tree, "true")


def test_bad_results_counts_for_operator_and():
    assert graph.evaluate.oval_operator_and(results_counts) is None


def test_bad_results_counts_for_operator_one():
    assert graph.evaluate.oval_operator_one(results_counts) is None


def test_bad_results_counts_for_operator_or():
    assert graph.evaluate.oval_operator_or(results_counts) is None


def test_bad_results_counts_for_operator_xor():
    assert graph.evaluate.oval_operator_xor(results_counts) is None


def test_false_noteval_greater_zero():
    assert graph.evaluate.greater_zero(results_counts,'noteval_cnt') == False


def test_false_error_unknown_eq_noteval_greater_zero():
    assert graph.evaluate.error_unknown_eq_noteval_greater_zero(results_counts) == False


def any_test_parsing_and_evaluate_scan_rule(src, rule_id, result):
    _dir = os.path.dirname(os.path.realpath(__file__))
    FIXTURE_DIR = py.path.local(_dir) / src
    
    oval_tree = graph.oval_graph.build_nodes_form_xml(str(FIXTURE_DIR), rule_id)
    any_test_treeEvaluation(oval_tree, result)


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

def any_test_create_node_dict_for_sigmaJs(Tree,out):
    assert Tree._create_node(0,0)==out

def test_create_node_dict_for_sigmaJs_0():
    out = {
        'color': '#ff0000',
        'id': 1,
        'label': 'and',
        'size': 3,
        'text': 'null',
        'url': 'null',
        'title': 1,
        'x': 0,
        'y': 0
    }
    Tree=get_simple_tree()
    any_test_create_node_dict_for_sigmaJs(Tree,out)

def test_create_node_dict_for_sigmaJs_1():
    out = {
        'color': '#00ff00',
        'id': 1,
        'label': 'and',
        'size': 3,
        'text': 'null',
        'url': 'null',
        'title': 1,
        'x': 0,
        'y': 0
    }
    Tree=graph.oval_graph.OvalNode(1, 'operator', 'and', [
                graph.oval_graph.OvalNode(2, 'value', "true")
            ]
            )

    any_test_create_node_dict_for_sigmaJs(Tree,out)

def test_create_node_dict_for_sigmaJs_2():
    out = {
        'color': '#000000',
        'id': 1,
        'label': 'and',
        'size': 3,
        'text': 'null',
        'url': 'null',
        'title': '1 and',
        'x': 0,
        'y': 0
    }
    Tree=graph.oval_graph.OvalNode(1, 'operator', 'and', [
                graph.oval_graph.OvalNode(2, 'value', "noteval")
            ]
            )

    any_test_create_node_dict_for_sigmaJs(Tree,out)

def test_create_node_dict_for_sigmaJs_3():
    out = {
        'color': '#ff0000',
        'id': 1,
        'label': 'false',
        'size': 3,
        'text': 'null',
        'url': 'null',
        'title': 1,
        'x': 0,
        'y': 0
    }
    Tree=graph.oval_graph.OvalNode(1, 'value', 'false')

    any_test_create_node_dict_for_sigmaJs(Tree,out)

def test_create_node_dict_for_sigmaJs_4():
    out = {
        'color': '#00ff00',
        'id': 1,
        'label': 'true',
        'size': 3,
        'text': 'null',
        'url': 'null',
        'title': 1,
        'x': 0,
        'y': 0
    }
    Tree=graph.oval_graph.OvalNode(1, 'value', 'true')

    any_test_create_node_dict_for_sigmaJs(Tree,out)


def test_create_node_dict_for_sigmaJs_5():
    out = {
        'color': '#000000',
        'id': 1,
        'label': 'error',
        'size': 3,
        'text': 'null',
        'url': 'null',
        'title': '1 error',
        'x': 0,
        'y': 0
    }
    Tree=graph.oval_graph.OvalNode(1, 'value', 'error')

    any_test_create_node_dict_for_sigmaJs(Tree,out)


def test_create_edge_dict_for_sigmaJs():
    print(get_simple_tree()._create_edge(1,2))
    out = {
        'id': 'random_ID',
        'source': 1,
        'target': 2
        }

    assert get_simple_tree()._create_edge(1,2)['source']==out['source']
    assert get_simple_tree()._create_edge(1,2)['target']==out['target']   

def test_create_array_of_ids_form_tree():
     array=get_simple_tree().create_list_of_id()
     assert array==[1,2,3,4,5,6]

def test_parsing_full_can_XML_and_evaluate():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    rule_id = 'xccdf_org.ssgproject.content_rule_accounts_passwords_pam_faillock_deny'
    result = 'false'

    any_test_parsing_and_evaluate_scan_rule(src, rule_id, result)


def test_parsing_and_evaluate_scan_with_extend_def():
    src = 'test_data/ssg-fedora-ds-arf-scan-with-extend-definitions.xml'
    rule_id = 'xccdf_org.ssgproject.content_rule_sysctl_net_ipv6_conf_all_disable_ipv6'
    result = 'false'

    any_test_parsing_and_evaluate_scan_rule(src, rule_id, result)


def test_parsing_and_evaluate_scan_with_pasing_rule():
    src = 'test_data/ssg-fedora-ds-arf-passing-scan.xml'
    rule_id = 'xccdf_org.ssgproject.content_rule_service_debug-shell_disabled'
    result = 'true'

    any_test_parsing_and_evaluate_scan_rule(src, rule_id, result)


def test_parsing_and_evaluate_scan_with_fail_rule():
    src = 'test_data/ssg-fedora-ds-arf-scan-fail.xml'
    rule_id = 'xccdf_org.ssgproject.content_rule_mount_option_dev_shm_noexec'
    result = 'false'

    any_test_parsing_and_evaluate_scan_rule(src, rule_id, result)


def test_parsing_and_evaluate_scan_with_rule_with_XOR():
    src = 'test_data/ssg-fedora-ds-arf-scan-with-xor.xml'
    rule_id = 'xccdf_org.ssgproject.content_rule_mount_option_nosuid_removable_partitions'
    result = 'true'

    any_test_parsing_and_evaluate_scan_rule(src, rule_id, result)


def test_parsing_and_evaluate_scan_with_11_rules():
    src = 'test_data/ssg-fedora-ds-arf-scan-with-11-rules.xml'
    rule_id = 'xccdf_org.ssgproject.content_rule_mount_option_tmp_nosuid'
    result = 'true'

    any_test_parsing_and_evaluate_scan_rule(src, rule_id, result)


def test_transformation_tree_to_Json_for_SigmaJs_0():
    test_data = {
        "nodes": [
        {
            "id": "xccdf_org.ssgproject.content_rule_accounts_passwords_pam_faillock_deny",
            "label": "and",
            "url": "null",
            "text": "null",
            "title": "xccdf_org.ssgproject.content_rule_accounts_passwords_pam_faillock_deny",
            "x": -13,
            "y": 0,
            "size": 3,
            "color": "#ff0000"
        },
        {
            "id": "oval:ssg-accounts_passwords_pam_faillock_deny:def:1",
            "label": "and",
            "url": "null",
            "text": "null",
            "title": "oval:ssg-accounts_passwords_pam_faillock_deny:def:1",
            "x": -13,
            "y": 1,
            "size": 3,
            "color": "#ff0000"
        },
        {
            "id": "oval:ssg-test_accounts_passwords_pam_faillock_preauth_silent_system-auth:tst:1",
            "label": "false",
            "url": "null",
            "text": "null",
            "title": "oval:ssg-test_accounts_passwords_pam_faillock_preauth_silent_system-auth:tst:1",
            "x": -11,
            "y": 3,
            "size": 3,
            "color": "#ff0000"
        },
        {
            "id": "oval:ssg-test_accounts_passwords_pam_faillock_account_phase_system-auth:tst:1",
            "label": "false",
            "url": "null",
            "text": "null",
            "title": "oval:ssg-test_accounts_passwords_pam_faillock_account_phase_system-auth:tst:1",
            "x": -9,
            "y": 3,
            "size": 3,
            "color": "#ff0000"
        },
        {
            "id": "oval:ssg-test_accounts_passwords_pam_faillock_preauth_silent_password-auth:tst:1",
            "label": "false",
            "url": "null",
            "text": "null",
            "title": "oval:ssg-test_accounts_passwords_pam_faillock_preauth_silent_password-auth:tst:1",
            "x": -7,
            "y": 3,
            "size": 3,
            "color": "#ff0000"
        },
        {
            "id": "oval:ssg-test_accounts_passwords_pam_faillock_account_phase_password-auth:tst:1",
            "label": "false",
            "url": "null",
            "text": "null",
            "title": "oval:ssg-test_accounts_passwords_pam_faillock_account_phase_password-auth:tst:1",
            "x": -5,
            "y": 3,
            "size": 3,
            "color": "#ff0000"
        },
        {
            "id": "b2eae097-2c22-4c0b-8796-4b76e9b1a8c0",
            "label": "and",
            "url": "null",
            "text": "null",
            "title": "b2eae097-2c22-4c0b-8796-4b76e9b1a8c0",
            "x": -3,
            "y": 3,
            "size": 3,
            "color": "#ff0000"
        },
        {
            "id": "ece33afa-c675-4a43-9366-f946181937f4",
            "label": "or",
            "url": "null",
            "text": "null",
            "title": "ece33afa-c675-4a43-9366-f946181937f4",
            "x": -1,
            "y": 5,
            "size": 3,
            "color": "#ff0000"
        },
        {
            "id": "oval:ssg-test_accounts_passwords_pam_faillock_numeric_default_check_system-auth:tst:1",
            "label": "false",
            "url": "null",
            "text": "null",
            "title": "oval:ssg-test_accounts_passwords_pam_faillock_numeric_default_check_system-auth:tst:1",
            "x": 1,
            "y": 7,
            "size": 3,
            "color": "#ff0000"
        },
        {
            "id": "oval:ssg-test_accounts_passwords_pam_faillock_authfail_deny_system-auth:tst:1",
            "label": "false",
            "url": "null",
            "text": "null",
            "title": "oval:ssg-test_accounts_passwords_pam_faillock_authfail_deny_system-auth:tst:1",
            "x": 3,
            "y": 7,
            "size": 3,
            "color": "#ff0000"
        },
        {
            "id": "c157ad0e-3326-4ae4-88d4-14a9bf7e6a84",
            "label": "or",
            "url": "null",
            "text": "null",
            "title": "c157ad0e-3326-4ae4-88d4-14a9bf7e6a84",
            "x": 3,
            "y": 5,
            "size": 3,
            "color": "#ff0000"
        },
        {
            "id": "oval:ssg-test_accounts_passwords_pam_faillock_numeric_default_check_password-auth:tst:1",
            "label": "false",
            "url": "null",
            "text": "null",
            "title": "oval:ssg-test_accounts_passwords_pam_faillock_numeric_default_check_password-auth:tst:1",
            "x": 5,
            "y": 7,
            "size": 3,
            "color": "#ff0000"
        },
        {
            "id": "oval:ssg-test_accounts_passwords_pam_faillock_authfail_deny_password-auth:tst:1",
            "label": "false",
            "url": "null",
            "text": "null",
            "title": "oval:ssg-test_accounts_passwords_pam_faillock_authfail_deny_password-auth:tst:1",
            "x": 7,
            "y": 7,
            "size": 3,
            "color": "#ff0000"
        }
        ],
        "edges": [
        {
            "id": "f8e7e5c5-facf-4ba5-aa06-0cad749c1683",
            "source": "xccdf_org.ssgproject.content_rule_accounts_passwords_pam_faillock_deny",
            "target": "oval:ssg-accounts_passwords_pam_faillock_deny:def:1"
        },
        {
            "id": "003367ab-2d0e-4ee2-8e04-a8d724c00b4f",
            "source": "oval:ssg-accounts_passwords_pam_faillock_deny:def:1",
            "target": "oval:ssg-test_accounts_passwords_pam_faillock_preauth_silent_system-auth:tst:1"
        },
        {
            "id": "d89082e6-4f27-4c1f-a1c2-faf6e59a49a0",
            "source": "oval:ssg-accounts_passwords_pam_faillock_deny:def:1",
            "target": "oval:ssg-test_accounts_passwords_pam_faillock_account_phase_system-auth:tst:1"
        },
        {
            "id": "a5b2dce5-35de-4060-b499-05dd517c993d",
            "source": "oval:ssg-accounts_passwords_pam_faillock_deny:def:1",
            "target": "oval:ssg-test_accounts_passwords_pam_faillock_preauth_silent_password-auth:tst:1"
        },
        {
            "id": "f62a2828-ed80-4f0d-8c1a-2fd6da231d58",
            "source": "oval:ssg-accounts_passwords_pam_faillock_deny:def:1",
            "target": "oval:ssg-test_accounts_passwords_pam_faillock_account_phase_password-auth:tst:1"
        },
        {
            "id": "436845ff-994c-4026-adc5-0841a2a61e51",
            "source": "oval:ssg-accounts_passwords_pam_faillock_deny:def:1",
            "target": "b2eae097-2c22-4c0b-8796-4b76e9b1a8c0"
        },
        {
            "id": "466ef345-9f61-4d70-8f0a-c0a3257cc253",
            "source": "b2eae097-2c22-4c0b-8796-4b76e9b1a8c0",
            "target": "ece33afa-c675-4a43-9366-f946181937f4"
        },
        {
            "id": "2bed2247-8155-4a2e-b75a-35d5839d9db4",
            "source": "ece33afa-c675-4a43-9366-f946181937f4",
            "target": "oval:ssg-test_accounts_passwords_pam_faillock_numeric_default_check_system-auth:tst:1"
        },
        {
            "id": "be4e6a91-b874-4082-b077-ff74e286c91d",
            "source": "ece33afa-c675-4a43-9366-f946181937f4",
            "target": "oval:ssg-test_accounts_passwords_pam_faillock_authfail_deny_system-auth:tst:1"
        },
        {
            "id": "29b9563c-2f8f-4554-8159-102ec4897ac1",
            "source": "b2eae097-2c22-4c0b-8796-4b76e9b1a8c0",
            "target": "c157ad0e-3326-4ae4-88d4-14a9bf7e6a84"
        },
        {
            "id": "7d06f894-071e-4383-96e8-934513eb857c",
            "source": "c157ad0e-3326-4ae4-88d4-14a9bf7e6a84",
            "target": "oval:ssg-test_accounts_passwords_pam_faillock_numeric_default_check_password-auth:tst:1"
        },
        {
            "id": "e4c5ee00-5736-4b67-b19d-43472a5d6768",
            "source": "c157ad0e-3326-4ae4-88d4-14a9bf7e6a84",
            "target": "oval:ssg-test_accounts_passwords_pam_faillock_authfail_deny_password-auth:tst:1"
        }
        ]
        }
    src = 'data/ssg-fedora-ds-arf.xml'
    rule_id = 'xccdf_org.ssgproject.content_rule_accounts_passwords_pam_faillock_deny'
    
    oval_tree = graph.oval_graph.build_nodes_form_xml(src, rule_id)
    if oval_tree.node_id == rule_id:
        out_data = oval_tree.to_sigma_dict(0, 0)
        for i in range(len(out_data['nodes'])):
            assert out_data['nodes'][i]['label']==test_data['nodes'][i]['label']
            assert out_data['nodes'][i]['text']==test_data['nodes'][i]['text']
            assert out_data['nodes'][i]['url']==test_data['nodes'][i]['url']


def test_transformation_tree_to_Json_for_SigmaJs_with_duplicated_test():
    test_data = {
        "nodes": [
        {
            "id": "xccdf_org.ssgproject.content_rule_disable_host_auth",
            "label": "and",
            "url": "null",
            "text": "null",
            "title": "xccdf_org.ssgproject.content_rule_disable_host_auth",
            "x": -17,
            "y": 0,
            "size": 3,
            "color": "#00ff00"
        },
        {
            "id": "oval:ssg-disable_host_auth:def:1",
            "label": "or",
            "url": "null",
            "text": "null",
            "title": "oval:ssg-disable_host_auth:def:1",
            "x": -17,
            "y": 1,
            "size": 3,
            "color": "#00ff00"
        },
        {
            "id": "b688b097-7f93-4d38-be83-f8aee611a7ab",
            "label": "and",
            "url": "null",
            "text": "null",
            "title": "b688b097-7f93-4d38-be83-f8aee611a7ab",
            "x": -15,
            "y": 3,
            "size": 3,
            "color": "#ff0000"
        },
        {
            "id": "71e748eb-4f25-481d-8e03-d8b4b18c8cb3",
            "label": "or",
            "url": "null",
            "text": "null",
            "title": "71e748eb-4f25-481d-8e03-d8b4b18c8cb3",
            "x": -13,
            "y": 5,
            "size": 3,
            "color": "#00ff00"
        },
        {
            "id": "oval:ssg-test_sshd_not_required:tst:1",
            "label": "false",
            "url": "null",
            "text": "null",
            "title": "oval:ssg-test_sshd_not_required:tst:1",
            "x": -11,
            "y": 7,
            "size": 3,
            "color": "#ff0000"
        },
        {
            "id": "70d25e1d-3ac9-4f5a-8f86-1ad46b13ce09",
            "label": "and",
            "url": "null",
            "text": "null",
            "title": "70d25e1d-3ac9-4f5a-8f86-1ad46b13ce09",
            "x": -9,
            "y": 7,
            "size": 3,
            "color": "#00ff00"
        },
        {
            "id": "d4ebfbf0-acec-41b7-83be-e98665b6f645",
            "label": "and",
            "url": "null",
            "text": "null",
            "title": "d4ebfbf0-acec-41b7-83be-e98665b6f645",
            "x": -8,
            "y": 5,
            "size": 3,
            "color": "#ff0000"
        },
        {
            "id": "oval:ssg-test_package_openssh-server_removed:tst:1",
            "label": "false",
            "url": "null",
            "text": "null",
            "title": "oval:ssg-test_package_openssh-server_removed:tst:1",
            "x": -6,
            "y": 7,
            "size": 3,
            "color": "#ff0000"
        },
        {
            "id": "fddd65d1-ec4d-4b8f-95d9-45eac3a8d502",
            "label": "and",
            "url": "null",
            "text": "null",
            "title": "fddd65d1-ec4d-4b8f-95d9-45eac3a8d502",
            "x": -7,
            "y": 3,
            "size": 3,
            "color": "#00ff00"
        },
        {
            "id": "bb5da04b-9b2f-4e54-b89f-8c871c404e87",
            "label": "or",
            "url": "null",
            "text": "null",
            "title": "bb5da04b-9b2f-4e54-b89f-8c871c404e87",
            "x": -5,
            "y": 5,
            "size": 3,
            "color": "#00ff00"
        },
        {
            "id": "oval:ssg-test_sshd_required:tst:1",
            "label": "false",
            "url": "null",
            "text": "null",
            "title": "oval:ssg-test_sshd_required:tst:1",
            "x": -3,
            "y": 7,
            "size": 3,
            "color": "#ff0000"
        },
        {
            "id": "20886ece-396f-45fe-992a-563623f35b9b",
            "label": "and",
            "url": "null",
            "text": "null",
            "title": "20886ece-396f-45fe-992a-563623f35b9b",
            "x": -1,
            "y": 7,
            "size": 3,
            "color": "#00ff00"
        },
        {
            "id": "fc1496fd-1097-4bed-8651-f8d7a3b82e3b",
            "label": "and",
            "url": "null",
            "text": "null",
            "title": "fc1496fd-1097-4bed-8651-f8d7a3b82e3b",
            "x": 0,
            "y": 5,
            "size": 3,
            "color": "#00ff00"
        },
        {
            "id": "oval:ssg-test_package_openssh-server_installed:tst:1",
            "label": "true",
            "url": "null",
            "text": "null",
            "title": "oval:ssg-test_package_openssh-server_installed:tst:1",
            "x": 2,
            "y": 7,
            "size": 3,
            "color": "#00ff00"
        },
        {
            "id": "oval:ssg-test_sshd_hostbasedauthentication:tst:1",
            "label": "true",
            "url": "null",
            "text": "null",
            "title": "oval:ssg-test_sshd_hostbasedauthentication:tst:1",
            "x": 3,
            "y": 5,
            "size": 3,
            "color": "#00ff00"
        },
        {
            "id": "oval:ssg-test_sshd_requirement_unset:tst:1",
            "label": "true",
            "url": "null",
            "text": "null",
            "title": "oval:ssg-test_sshd_requirement_unset:tst:1",
            "x": -7,
            "y": 9,
            "size": 3,
            "color": "#00ff00"
        }
        ],
        "edges": [
        {
            "id": "6fa59d60-26e4-439c-be15-0b1b2d69c1e3",
            "source": "xccdf_org.ssgproject.content_rule_disable_host_auth",
            "target": "oval:ssg-disable_host_auth:def:1"
        },
        {
            "id": "79b0a3ff-5102-4c20-a625-a5cdecad378d",
            "source": "oval:ssg-disable_host_auth:def:1",
            "target": "b688b097-7f93-4d38-be83-f8aee611a7ab"
        },
        {
            "id": "5fa8e26a-06a6-4ac9-948d-a7875c6476c7",
            "source": "b688b097-7f93-4d38-be83-f8aee611a7ab",
            "target": "71e748eb-4f25-481d-8e03-d8b4b18c8cb3"
        },
        {
            "id": "b93d6a68-bfca-4baf-9261-15569db9a0b7",
            "source": "71e748eb-4f25-481d-8e03-d8b4b18c8cb3",
            "target": "oval:ssg-test_sshd_not_required:tst:1"
        },
        {
            "id": "b292dd59-38b7-4a82-b437-714b4aabd51a",
            "source": "71e748eb-4f25-481d-8e03-d8b4b18c8cb3",
            "target": "70d25e1d-3ac9-4f5a-8f86-1ad46b13ce09"
        },
        {
            "id": "1895c211-8af2-476d-9a30-db25e5057507",
            "source": "70d25e1d-3ac9-4f5a-8f86-1ad46b13ce09",
            "target": "oval:ssg-test_sshd_requirement_unset:tst:1"
        },
        {
            "id": "aa0316a5-f0ce-44b3-bf79-1459b1cca894",
            "source": "b688b097-7f93-4d38-be83-f8aee611a7ab",
            "target": "d4ebfbf0-acec-41b7-83be-e98665b6f645"
        },
        {
            "id": "42d2ecb9-b45e-4d20-ac92-75f9612f992f",
            "source": "d4ebfbf0-acec-41b7-83be-e98665b6f645",
            "target": "oval:ssg-test_package_openssh-server_removed:tst:1"
        },
        {
            "id": "c4cc7923-02b4-4277-8adb-aa792211faa8",
            "source": "oval:ssg-disable_host_auth:def:1",
            "target": "fddd65d1-ec4d-4b8f-95d9-45eac3a8d502"
        },
        {
            "id": "b648737a-5082-4231-9790-5db1e51df8f9",
            "source": "fddd65d1-ec4d-4b8f-95d9-45eac3a8d502",
            "target": "bb5da04b-9b2f-4e54-b89f-8c871c404e87"
        },
        {
            "id": "13f25b40-7410-4311-9f05-7a28a28e4511",
            "source": "bb5da04b-9b2f-4e54-b89f-8c871c404e87",
            "target": "oval:ssg-test_sshd_required:tst:1"
        },
        {
            "id": "db8a73d8-aecb-4f84-b325-c1799a49af14",
            "source": "bb5da04b-9b2f-4e54-b89f-8c871c404e87",
            "target": "20886ece-396f-45fe-992a-563623f35b9b"
        },
        {
            "id": "28ec9594-32c7-4ee2-9296-ebe728cc88be",
            "source": "20886ece-396f-45fe-992a-563623f35b9b",
            "target": "oval:ssg-test_sshd_requirement_unset:tst:1"
        },
        {
            "id": "5350c294-9036-497a-bea5-2dbd47502c34",
            "source": "fddd65d1-ec4d-4b8f-95d9-45eac3a8d502",
            "target": "fc1496fd-1097-4bed-8651-f8d7a3b82e3b"
        },
        {
            "id": "94492e77-6089-44d6-95d0-ff61421112a4",
            "source": "fc1496fd-1097-4bed-8651-f8d7a3b82e3b",
            "target": "oval:ssg-test_package_openssh-server_installed:tst:1"
        },
        {
            "id": "ae8a5250-93ca-4143-9812-8847dc8fac82",
            "source": "fddd65d1-ec4d-4b8f-95d9-45eac3a8d502",
            "target": "oval:ssg-test_sshd_hostbasedauthentication:tst:1"
        }
        ]
        }    
    src = 'data/ssg-fedora-ds-arf.xml'
    rule_id = 'xccdf_org.ssgproject.content_rule_disable_host_auth'

    oval_tree = graph.oval_graph.build_nodes_form_xml(src, rule_id)
    
    if oval_tree.node_id == rule_id:
        out_data = oval_tree.to_sigma_dict(0, 0)
        for i in range(len(out_data['nodes'])):
            assert out_data['nodes'][i]['label']==test_data['nodes'][i]['label']
            assert out_data['nodes'][i]['text']==test_data['nodes'][i]['text']
            assert out_data['nodes'][i]['url']==test_data['nodes'][i]['url']


def test_and_or_eq_zero():
    assert graph.evaluate.and_or_eq_zero('and',results_counts) == False
    assert graph.evaluate.and_or_eq_zero('or',results_counts) == False  
    assert graph.evaluate.and_or_eq_zero('xor',results_counts) == None  


def test_get_def_id_by_rule_id():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    _dir = os.path.dirname(os.path.realpath(__file__))
    FIXTURE_DIR = py.path.local(_dir) / src

    parser = graph.xml_parser.xml_parser(str(FIXTURE_DIR))
    
    with pytest.raises(ValueError) as e:
        parser.get_def_id_by_rule_id('hello')
    assert str(
        e.value) == 'err- 404 rule not found!'
