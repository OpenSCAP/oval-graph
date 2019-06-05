import tree.oval_tree
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
    t = tree.oval_tree.OvalNode(
        1, "value", "true", [
            tree.oval_tree.OvalNode(
                2, "operator", "and", [
                    tree.oval_tree.OvalNode(
                        3, "value", "true")])])
    return


def treeOnlyOr():
    """
        or
    """
    Tree = tree.oval_tree.OvalNode(1, "operator", 'or')
    return


def treeOnlyAnd():
    """
        and
    """
    Tree = tree.oval_tree.OvalNode(1, "operator", 'and')
    return


def treeWithBadValueOfOperator():
    Tree = tree.oval_tree.OvalNode(1, "operator", 'nad')
    return


def treeWithBadValueOfValue():
    Tree = tree.oval_tree.OvalNode(1, "value", 'and')
    return


def treeWithBadType():
    Tree = tree.oval_tree.OvalNode(1, "auto", 'and')
    return

# normal trees


def test_UPPERCASETree():
    t = tree.oval_tree.OvalNode(
        1, "OPERATOR", "AND", [
            tree.oval_tree.OvalNode(
                2, "VALUE", "TRUE",), tree.oval_tree.OvalNode(
                3, "VALUE", "NOTAPPL")])

# AND operator


def test_ANDTreeTrue():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'and', [
        tree.oval_tree.OvalNode(2, 'value', "true"),
        tree.oval_tree.OvalNode(3, 'value', "true"),
        tree.oval_tree.OvalNode(4, 'value', "notappl")
    ]
    )

    any_test_treeEvaluation(Tree, "true")


def test_ANDTreeFalse():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'and', [
        tree.oval_tree.OvalNode(2, 'value', "false"),
        tree.oval_tree.OvalNode(3, 'value', "false"),

        tree.oval_tree.OvalNode(4, 'value', "true"),
        tree.oval_tree.OvalNode(5, 'value', "error"),
        tree.oval_tree.OvalNode(6, 'value', "unknown"),
        tree.oval_tree.OvalNode(7, 'value', "noteval"),
        tree.oval_tree.OvalNode(8, 'value', "notappl")
    ]
    )

    any_test_treeEvaluation(Tree, "false")


def test_ANDTreeError():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'and', [
                tree.oval_tree.OvalNode(2, 'value', "error"),
                tree.oval_tree.OvalNode(3, 'value', "error"),
                tree.oval_tree.OvalNode(4, 'value', "true"),
                tree.oval_tree.OvalNode(5, 'value', "unknown"),
                tree.oval_tree.OvalNode(6, 'value', "noteval"),
                tree.oval_tree.OvalNode(7, 'value', "notappl"),
                tree.oval_tree.OvalNode(8, 'value', "error")
                ])

    any_test_treeEvaluation(Tree, "error")


def test_ANDTreeUnknown():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'and', [
                tree.oval_tree.OvalNode(2, 'value', "unknown"),
                tree.oval_tree.OvalNode(3, 'value', "unknown"),
                tree.oval_tree.OvalNode(4, 'value', "true"),
                tree.oval_tree.OvalNode(5, 'value', "unknown"),
                tree.oval_tree.OvalNode(6, 'value', "noteval"),
                tree.oval_tree.OvalNode(7, 'value', "notappl"),
                tree.oval_tree.OvalNode(8, 'value', "notappl")
                ]
                )

    any_test_treeEvaluation(Tree, "unknown")


def test_ANDTreeNoteval():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'and', [
                tree.oval_tree.OvalNode(2, 'value', "noteval"),
                tree.oval_tree.OvalNode(3, 'value', "noteval"),
                tree.oval_tree.OvalNode(4, 'value', "true"),
                tree.oval_tree.OvalNode(5, 'value', "true"),
                tree.oval_tree.OvalNode(6, 'value', "noteval"),
                tree.oval_tree.OvalNode(7, 'value', "notappl"),
                tree.oval_tree.OvalNode(8, 'value', "notappl")
                ]
                )

    any_test_treeEvaluation(Tree, "noteval")


def test_ANDTreeNotappl():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'and', [
        tree.oval_tree.OvalNode(2, 'value', "notappl"),
        tree.oval_tree.OvalNode(3, 'value', "notappl"),
        tree.oval_tree.OvalNode(4, 'value', "notappl")
    ]
    )

    any_test_treeEvaluation(Tree, "notappl")

# ONE operator


def test_ONETreeTrue():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'one', [
        tree.oval_tree.OvalNode(2, 'value', "true"),
        tree.oval_tree.OvalNode(3, 'value', "false"),
        tree.oval_tree.OvalNode(4, 'value', "notappl"),
        tree.oval_tree.OvalNode(5, 'value', "false")
    ]
    )

    any_test_treeEvaluation(Tree, "true")


def test_ONETreeFalse():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'one', [
        tree.oval_tree.OvalNode(2, 'value', "true"),
        tree.oval_tree.OvalNode(3, 'value', "true"),

        tree.oval_tree.OvalNode(4, 'value', "false"),
        tree.oval_tree.OvalNode(5, 'value', "error"),
        tree.oval_tree.OvalNode(6, 'value', "unknown"),
        tree.oval_tree.OvalNode(7, 'value', "noteval"),
        tree.oval_tree.OvalNode(8, 'value', "notappl")
    ]
    )

    any_test_treeEvaluation(Tree, "false")


def test_ONETreeFalse1():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'one', [
        tree.oval_tree.OvalNode(2, 'value', "false"),
        tree.oval_tree.OvalNode(3, 'value', "false"),
        tree.oval_tree.OvalNode(4, 'value', "notappl")
    ]
    )

    any_test_treeEvaluation(Tree, "false")


def test_ONETreeError():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'one', [
                tree.oval_tree.OvalNode(2, 'value', "error"),
                tree.oval_tree.OvalNode(3, 'value', "error"),
                tree.oval_tree.OvalNode(4, 'value', "true"),
                tree.oval_tree.OvalNode(5, 'value', "unknown"),
                tree.oval_tree.OvalNode(6, 'value', "noteval"),
                tree.oval_tree.OvalNode(7, 'value', "notappl"),
                tree.oval_tree.OvalNode(8, 'value', "false")
                ]
                )

    any_test_treeEvaluation(Tree, "error")


def test_ONETreeUnknown():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'one', [
                tree.oval_tree.OvalNode(2, 'value', "unknown"),
                tree.oval_tree.OvalNode(3, 'value', "unknown"),
                tree.oval_tree.OvalNode(4, 'value', "true"),
                tree.oval_tree.OvalNode(5, 'value', "unknown"),
                tree.oval_tree.OvalNode(6, 'value', "noteval"),
                tree.oval_tree.OvalNode(7, 'value', "notappl"),
                tree.oval_tree.OvalNode(8, 'value', "false")
                ])

    any_test_treeEvaluation(Tree, "unknown")


def test_ONETreeNoteval():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'one', [
                tree.oval_tree.OvalNode(2, 'value', "noteval"),
                tree.oval_tree.OvalNode(3, 'value', "noteval"),
                tree.oval_tree.OvalNode(4, 'value', "true"),
                tree.oval_tree.OvalNode(5, 'value', "false"),
                tree.oval_tree.OvalNode(6, 'value', "noteval"),
                tree.oval_tree.OvalNode(7, 'value', "notappl"),
                tree.oval_tree.OvalNode(8, 'value', "notappl")
                ]
                )

    any_test_treeEvaluation(Tree, "noteval")


def test_ONETreeNotappl():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'one', [
        tree.oval_tree.OvalNode(2, 'value', "notappl"),
        tree.oval_tree.OvalNode(3, 'value', "notappl"),
        tree.oval_tree.OvalNode(4, 'value', "notappl")
    ]
    )

    any_test_treeEvaluation(Tree, "notappl")

# OR operator


def test_ORTreeTrue():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'or', [
        tree.oval_tree.OvalNode(2, 'value', "true"),
        tree.oval_tree.OvalNode(3, 'value', "false"),

        tree.oval_tree.OvalNode(4, 'value', "true"),
        tree.oval_tree.OvalNode(5, 'value', "error"),
        tree.oval_tree.OvalNode(6, 'value', "unknown"),
        tree.oval_tree.OvalNode(7, 'value', "noteval"),
        tree.oval_tree.OvalNode(8, 'value', "notappl")
    ]
    )

    any_test_treeEvaluation(Tree, "true")


def test_ORTreeFalse():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'or', [
        tree.oval_tree.OvalNode(2, 'value', "false"),
        tree.oval_tree.OvalNode(3, 'value', "false"),
        tree.oval_tree.OvalNode(4, 'value', "notappl")
    ]
    )

    any_test_treeEvaluation(Tree, "false")


def test_ORTreeError():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'or', [
                tree.oval_tree.OvalNode(2, 'value', "error"),
                tree.oval_tree.OvalNode(3, 'value', "error"),
                tree.oval_tree.OvalNode(4, 'value', "false"),
                tree.oval_tree.OvalNode(5, 'value', "unknown"),
                tree.oval_tree.OvalNode(6, 'value', "noteval"),
                tree.oval_tree.OvalNode(7, 'value', "notappl"),
                tree.oval_tree.OvalNode(8, 'value', "error")
                ]
                )

    any_test_treeEvaluation(Tree, "error")


def test_ORTreeUnknown():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'or', [
                tree.oval_tree.OvalNode(2, 'value', "unknown"),
                tree.oval_tree.OvalNode(3, 'value', "unknown"),
                tree.oval_tree.OvalNode(4, 'value', "false"),
                tree.oval_tree.OvalNode(5, 'value', "unknown"),
                tree.oval_tree.OvalNode(6, 'value', "noteval"),
                tree.oval_tree.OvalNode(7, 'value', "notappl"),
                tree.oval_tree.OvalNode(8, 'value', "notappl")
                ]
                )

    any_test_treeEvaluation(Tree, "unknown")


def test_ORTreeNoteval():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'or', [
                tree.oval_tree.OvalNode(2, 'value', "noteval"),
                tree.oval_tree.OvalNode(3, 'value', "noteval"),
                tree.oval_tree.OvalNode(4, 'value', "false"),
                tree.oval_tree.OvalNode(5, 'value', "false"),
                tree.oval_tree.OvalNode(6, 'value', "noteval"),
                tree.oval_tree.OvalNode(7, 'value', "notappl"),
                tree.oval_tree.OvalNode(8, 'value', "notappl")
                ]
                )

    any_test_treeEvaluation(Tree, "noteval")


def test_ORTreeNotappl():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'or', [
        tree.oval_tree.OvalNode(2, 'value', "notappl"),
        tree.oval_tree.OvalNode(3, 'value', "notappl"),
        tree.oval_tree.OvalNode(4, 'value', "notappl")
    ]
    )

    any_test_treeEvaluation(Tree, "notappl")

# XOR operator


def test_XORTreeTrue():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'xor', [
        tree.oval_tree.OvalNode(2, 'value', "true"),
        tree.oval_tree.OvalNode(3, 'value', "false"),

        tree.oval_tree.OvalNode(4, 'value', "false"),
        tree.oval_tree.OvalNode(5, 'value', "false"),
        tree.oval_tree.OvalNode(6, 'value', "true"),
        tree.oval_tree.OvalNode(7, 'value', "true"),
        tree.oval_tree.OvalNode(8, 'value', "notappl")
    ]
    )

    any_test_treeEvaluation(Tree, "true")


def test_XORTreeFalse():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'xor', [
        tree.oval_tree.OvalNode(2, 'value', "true"),
        tree.oval_tree.OvalNode(3, 'value', "false"),

        tree.oval_tree.OvalNode(4, 'value', "false"),
        tree.oval_tree.OvalNode(5, 'value', "true"),
        tree.oval_tree.OvalNode(6, 'value', "true"),
        tree.oval_tree.OvalNode(7, 'value', "true"),
        tree.oval_tree.OvalNode(8, 'value', "notappl")
    ]
    )

    any_test_treeEvaluation(Tree, "false")


def test_XORTreeError():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'xor', [
                tree.oval_tree.OvalNode(2, 'value', "error"),
                tree.oval_tree.OvalNode(3, 'value', "error"),
                tree.oval_tree.OvalNode(4, 'value', "true"),
                tree.oval_tree.OvalNode(5, 'value', "unknown"),
                tree.oval_tree.OvalNode(6, 'value', "noteval"),
                tree.oval_tree.OvalNode(7, 'value', "notappl"),
                tree.oval_tree.OvalNode(8, 'value', "false")
                ]
                )

    any_test_treeEvaluation(Tree, "error")


def test_xORTreeUnknown():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'xor', [
                tree.oval_tree.OvalNode(2, 'value', "unknown"),
                tree.oval_tree.OvalNode(3, 'value', "unknown"),
                tree.oval_tree.OvalNode(4, 'value', "true"),
                tree.oval_tree.OvalNode(5, 'value', "unknown"),
                tree.oval_tree.OvalNode(6, 'value', "noteval"),
                tree.oval_tree.OvalNode(7, 'value', "notappl"),
                tree.oval_tree.OvalNode(8, 'value', "notappl")
                ]
                )

    any_test_treeEvaluation(Tree, "unknown")


def test_XORTreeNoteval():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'xor', [
                tree.oval_tree.OvalNode(2, 'value', "noteval"),
                tree.oval_tree.OvalNode(3, 'value', "noteval"),
                tree.oval_tree.OvalNode(4, 'value', "true"),
                tree.oval_tree.OvalNode(5, 'value', "true"),
                tree.oval_tree.OvalNode(6, 'value', "noteval"),
                tree.oval_tree.OvalNode(7, 'value', "notappl"),
                tree.oval_tree.OvalNode(8, 'value', "notappl")
                ]
                )

    any_test_treeEvaluation(Tree, "noteval")


def test_XORTreeNotappl():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'xor', [
        tree.oval_tree.OvalNode(2, 'value', "notappl"),
        tree.oval_tree.OvalNode(3, 'value', "notappl"),
        tree.oval_tree.OvalNode(4, 'value', "notappl")
    ]
    )

    any_test_treeEvaluation(Tree, "notappl")


def test_bigOvalTree():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'and', [
                tree.oval_tree.OvalNode(2, 'value', "false"),
                tree.oval_tree.OvalNode(3, 'operator', "xor", [
                            tree.oval_tree.OvalNode(4, 'value', 'true'),
                            tree.oval_tree.OvalNode(5, 'operator', 'one', [
                                        tree.oval_tree.OvalNode(6, 'value', 'noteval'),
                                        tree.oval_tree.OvalNode(7, 'value', 'true'), 
                                        tree.oval_tree.OvalNode(8, 'value', 'notappl')
                                        ]
                                        ),
                            tree.oval_tree.OvalNode(9, 'value', 'error')
                            ]
                            ),
                tree.oval_tree.OvalNode(10, 'operator', 'or', [
                                        tree.oval_tree.OvalNode(11, 'value', "unknown"),
                                        tree.oval_tree.OvalNode(12, 'value', "true")
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
    assert tree.tree_to_dict() == dict_of_tree


def find_any_node(Tree, node_id):
    findTree = Tree.find_node_with_ID(node_id)
    assert findTree.node_id == node_id


def any_test_treeEvaluation(tree, expect):
    assert tree.evaluate_tree() == expect


def any_test_dict_to_tree(dict_of_tree):
    treedict_of_tree = tree.oval_tree.dict_to_tree(dict_of_tree)
    assert treedict_of_tree.tree_to_dict() == dict_of_tree


def test_treeRepr():
    """
        and
         |
         f
    """
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'and', [
        tree.oval_tree.OvalNode(2, 'value', "false")
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

    Tree = tree.oval_tree.OvalNode(1, 'operator', 'and', [
        tree.oval_tree.OvalNode(2, 'value', "false")
    ]
    )
    Tree1 = tree.oval_tree.OvalNode(3, 'value', "true")
    Tree.add_to_tree(1, Tree1)
    assert Tree.tree_to_dict() == dict_of_tree


def test_ChangeValueTree():
    """
        and
        /|\
       t t or
          / \
         f   t
    """
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'and', [
        tree.oval_tree.OvalNode(2, 'value', "true"),
        tree.oval_tree.OvalNode(3, 'value', "false"),
        tree.oval_tree.OvalNode(4, 'operator', 'or', [
            tree.oval_tree.OvalNode(5, 'value', "false"),
            tree.oval_tree.OvalNode(6, 'value', "true")
        ]
        )
    ]
    )

    Tree.change_tree_value(3, "true")
    any_test_treeEvaluation(Tree, "true")


def test_bad_operator_input_and():
    Tree = tree.oval_tree.OvalNode(0, 'value', "true")
    assert Tree._oval_operator_and(results_counts) is None


def test_bad_operator_input_one():
    Tree = tree.oval_tree.OvalNode(0, 'value', "true")
    assert Tree._oval_operator_one(results_counts) is None


def test_bad_operator_input_or():
    Tree = tree.oval_tree.OvalNode(0, 'value', "true")
    assert Tree._oval_operator_or(results_counts) is None


def test_bad_operator_input_xor():
    Tree = tree.oval_tree.OvalNode(0, 'value', "true")
    assert Tree._oval_operator_xor(results_counts) is None


def test_false_noteval_greater_zero():
    Tree = tree.oval_tree.OvalNode(0, 'value', "true")
    assert Tree._noteval_greater_zero(results_counts) == False


def test_false_error_unknown_eq_noteval_greater_zero():
    Tree = tree.oval_tree.OvalNode(0, 'value', "true")
    assert Tree._error_unknown_eq_noteval_greater_zero(results_counts) == False


def any_test_parsing_and_evaluate_scan_rule(src, rule_id, result):
    _dir = os.path.dirname(os.path.realpath(__file__))
    FIXTURE_DIR = py.path.local(_dir) / src

    oval_trees_array = tree.oval_tree.xml_to_tree(str(FIXTURE_DIR))
    for oval_tree in oval_trees_array:
        if oval_tree.node_id == rule_id:
            any_test_treeEvaluation(oval_tree, result)


def get_simple_tree():
    return tree.oval_tree.OvalNode(1, 'operator', 'and', [
        tree.oval_tree.OvalNode(2, 'value', "true"),
        tree.oval_tree.OvalNode(3, 'value', "false"),
        tree.oval_tree.OvalNode(4, 'operator', 'or', [
            tree.oval_tree.OvalNode(5, 'value', "false"),
            tree.oval_tree.OvalNode(6, 'value', "true")
        ]
        )
    ]
    )

def get_dict_of_simple_tree():
    return get_simple_tree().tree_to_dict()

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
        'x': 0,
        'y': 0
    }
    Tree=tree.oval_tree.OvalNode(1, 'operator', 'and', [
                tree.oval_tree.OvalNode(2, 'value', "true")
            ]
            )

    any_test_create_node_dict_for_sigmaJs(Tree,out)

def test_create_node_dict_for_sigmaJs_2():
    out = {
        'color': '#000000',
        'id': 1,
        'label': '1 and',
        'size': 3,
        'text': 'null',
        'url': 'null',
        'x': 0,
        'y': 0
    }
    Tree=tree.oval_tree.OvalNode(1, 'operator', 'and', [
                tree.oval_tree.OvalNode(2, 'value', "noteval")
            ]
            )

    any_test_create_node_dict_for_sigmaJs(Tree,out)

def test_create_node_dict_for_sigmaJs_3():
    out = {
        'color': '#ff0000',
        'id': 1,
        'label': 1,
        'size': 3,
        'text': 'null',
        'url': 'null',
        'x': 0,
        'y': 0
    }
    Tree=tree.oval_tree.OvalNode(1, 'value', 'false')

    any_test_create_node_dict_for_sigmaJs(Tree,out)

def test_create_node_dict_for_sigmaJs_4():
    out = {
        'color': '#00ff00',
        'id': 1,
        'label': 1,
        'size': 3,
        'text': 'null',
        'url': 'null',
        'x': 0,
        'y': 0
    }
    Tree=tree.oval_tree.OvalNode(1, 'value', 'true')

    any_test_create_node_dict_for_sigmaJs(Tree,out)


def test_create_node_dict_for_sigmaJs_5():
    out = {
        'color': '#000000',
        'id': 1,
        'label': '1 error',
        'size': 3,
        'text': 'null',
        'url': 'null',
        'x': 0,
        'y': 0
    }
    Tree=tree.oval_tree.OvalNode(1, 'value', 'error')

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
                "url": 'null',
                "text": 'null',
                "x": -13,
                "y": 0,
                "size": 3,
                "color": "#ff0000"
            },
            {
                "id": "oval:ssg-accounts_passwords_pam_faillock_deny:def:1",
                "label": "and",
                "url": 'null',
                "text": 'null',
                "x": -13,
                "y": 1,
                "size": 3,
                "color": "#ff0000"
            },
            {
                "id": "oval:ssg-test_accounts_passwords_pam_faillock_preauth_silent_system-auth:tst:1",
                "label": "oval:ssg-test_accounts_passwords_pam_faillock_preauth_silent_system-auth:tst:1",
                "url": 'null',
                "text": 'null',
                "x": -11,
                "y": 3,
                "size": 3,
                "color": "#ff0000"
            },
            {
                "id": "oval:ssg-test_accounts_passwords_pam_faillock_account_phase_system-auth:tst:1",
                "label": "oval:ssg-test_accounts_passwords_pam_faillock_account_phase_system-auth:tst:1",
                "url": 'null',
                "text": 'null',
                "x": -9,
                "y": 3,
                "size": 3,
                "color": "#ff0000"
            },
            {
                "id": "oval:ssg-test_accounts_passwords_pam_faillock_preauth_silent_password-auth:tst:1",
                "label": "oval:ssg-test_accounts_passwords_pam_faillock_preauth_silent_password-auth:tst:1",
                "url": 'null',
                "text": 'null',
                "x": -7,
                "y": 3,
                "size": 3,
                "color": "#ff0000"
            },
            {
                "id": "oval:ssg-test_accounts_passwords_pam_faillock_account_phase_password-auth:tst:1",
                "label": "oval:ssg-test_accounts_passwords_pam_faillock_account_phase_password-auth:tst:1",
                "url": 'null',
                "text": 'null',
                "x": -5,
                "y": 3,
                "size": 3,
                "color": "#ff0000"
            },
            {
                "id": "6c555a8c-e00e-4dff-8cff-52ecf5e33ffa",
                "label": "and",
                "url": 'null',
                "text": 'null',
                "x": -3,
                "y": 3,
                "size": 3,
                "color": "#ff0000"
            },
            {
                "id": "fc292b8b-0cea-4322-b997-3d9676b36da3",
                "label": "or",
                "url": 'null',
                "text": 'null',
                "x": -1,
                "y": 5,
                "size": 3,
                "color": "#ff0000"
            },
            {
                "id": "oval:ssg-test_accounts_passwords_pam_faillock_numeric_default_check_system-auth:tst:1",
                "label": "oval:ssg-test_accounts_passwords_pam_faillock_numeric_default_check_system-auth:tst:1",
                "url": 'null',
                "text": 'null',
                "x": 1,
                "y": 7,
                "size": 3,
                "color": "#ff0000"
            },
            {
                "id": "oval:ssg-test_accounts_passwords_pam_faillock_authfail_deny_system-auth:tst:1",
                "label": "oval:ssg-test_accounts_passwords_pam_faillock_authfail_deny_system-auth:tst:1",
                "url": 'null',
                "text": 'null',
                "x": 3,
                "y": 7,
                "size": 3,
                "color": "#ff0000"
            },
            {
                "id": "bd64de81-238e-4b6b-8f2c-9fb98c7026bc",
                "label": "or",
                "url": 'null',
                "text": 'null',
                "x": 3,
                "y": 5,
                "size": 3,
                "color": "#ff0000"
            },
            {
                "id": "oval:ssg-test_accounts_passwords_pam_faillock_numeric_default_check_password-auth:tst:1",
                "label": "oval:ssg-test_accounts_passwords_pam_faillock_numeric_default_check_password-auth:tst:1",
                "url": 'null',
                "text": 'null',
                "x": 5,
                "y": 7,
                "size": 3,
                "color": "#ff0000"
            },
            {
                "id": "oval:ssg-test_accounts_passwords_pam_faillock_authfail_deny_password-auth:tst:1",
                "label": "oval:ssg-test_accounts_passwords_pam_faillock_authfail_deny_password-auth:tst:1",
                "url": 'null',
                "text": 'null',
                "x": 7,
                "y": 7,
                "size": 3,
                "color": "#ff0000"
            }
        ],
        "edges": [
            {
                "id": "7e89e0fa-419a-4344-80ed-7faf3edf966b",
                "source": "xccdf_org.ssgproject.content_rule_accounts_passwords_pam_faillock_deny",
                "target": "oval:ssg-accounts_passwords_pam_faillock_deny:def:1"
            },
            {
                "id": "a670a87a-d697-445b-83b1-7b6016559cea",
                "source": "oval:ssg-accounts_passwords_pam_faillock_deny:def:1",
                "target": "oval:ssg-test_accounts_passwords_pam_faillock_preauth_silent_system-auth:tst:1"
            },
            {
                "id": "d71f1872-0915-4f6e-a10b-e0556d782932",
                "source": "oval:ssg-accounts_passwords_pam_faillock_deny:def:1",
                "target": "oval:ssg-test_accounts_passwords_pam_faillock_account_phase_system-auth:tst:1"
            },
            {
                "id": "5596b215-8bcc-4137-95bc-513bff340a59",
                "source": "oval:ssg-accounts_passwords_pam_faillock_deny:def:1",
                "target": "oval:ssg-test_accounts_passwords_pam_faillock_preauth_silent_password-auth:tst:1"
            },
            {
                "id": "b2977657-394f-41aa-8d1e-032c88d7dcc4",
                "source": "oval:ssg-accounts_passwords_pam_faillock_deny:def:1",
                "target": "oval:ssg-test_accounts_passwords_pam_faillock_account_phase_password-auth:tst:1"
            },
            {
                "id": "086e7c21-e7e2-4da9-88a0-aa6e6f55b0c1",
                "source": "oval:ssg-accounts_passwords_pam_faillock_deny:def:1",
                "target": "6c555a8c-e00e-4dff-8cff-52ecf5e33ffa"
            },
            {
                "id": "2ba424ef-b5c1-4743-9785-e315fbc81a63",
                "source": "6c555a8c-e00e-4dff-8cff-52ecf5e33ffa",
                "target": "fc292b8b-0cea-4322-b997-3d9676b36da3"
            },
            {
                "id": "507d746a-50b0-4b98-9cde-749b8cc26976",
                "source": "fc292b8b-0cea-4322-b997-3d9676b36da3",
                "target": "oval:ssg-test_accounts_passwords_pam_faillock_numeric_default_check_system-auth:tst:1"
            },
            {
                "id": "b2aa01ba-07f9-44df-ac35-f1f9dcdea1c4",
                "source": "fc292b8b-0cea-4322-b997-3d9676b36da3",
                "target": "oval:ssg-test_accounts_passwords_pam_faillock_authfail_deny_system-auth:tst:1"
            },
            {
                "id": "aa731ac9-7089-4de9-9186-7ede165cc37e",
                "source": "6c555a8c-e00e-4dff-8cff-52ecf5e33ffa",
                "target": "bd64de81-238e-4b6b-8f2c-9fb98c7026bc"
            },
            {
                "id": "551725d6-4580-478f-a480-262a37ef35d5",
                "source": "bd64de81-238e-4b6b-8f2c-9fb98c7026bc",
                "target": "oval:ssg-test_accounts_passwords_pam_faillock_numeric_default_check_password-auth:tst:1"
            },
            {
                "id": "2fcc8d52-29ab-4028-8db3-c0127c996255",
                "source": "bd64de81-238e-4b6b-8f2c-9fb98c7026bc",
                "target": "oval:ssg-test_accounts_passwords_pam_faillock_authfail_deny_password-auth:tst:1"
            }
        ]
    }
    src = 'data/ssg-fedora-ds-arf.xml'
    rule_id = 'xccdf_org.ssgproject.content_rule_accounts_passwords_pam_faillock_deny'
    result = 'false'

    oval_trees_array = tree.oval_tree.xml_to_tree(src)
    for oval_tree in oval_trees_array:
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
            "x": -17,
            "y": 1,
            "size": 3,
            "color": "#00ff00"
        },
        {
            "id": "8513f7fb-818b-48cd-8d5d-cdaaf7e545ea",
            "label": "and",
            "url": "null",
            "text": "null",
            "x": -15,
            "y": 3,
            "size": 3,
            "color": "#ff0000"
        },
        {
            "id": "fcd586ce-b8bd-41e0-857d-04a315d0094e",
            "label": "or",
            "url": "null",
            "text": "null",
            "x": -13,
            "y": 5,
            "size": 3,
            "color": "#00ff00"
        },
        {
            "id": "oval:ssg-test_sshd_not_required:tst:1",
            "label": "oval:ssg-test_sshd_not_required:tst:1",
            "url": "null",
            "text": "null",
            "x": -11,
            "y": 7,
            "size": 3,
            "color": "#ff0000"
        },
        {
            "id": "7cbc49a3-771f-4ca5-81c2-376b72cf3625",
            "label": "and",
            "url": "null",
            "text": "null",
            "x": -9,
            "y": 7,
            "size": 3,
            "color": "#00ff00"
        },
        {
            "id": "b0f1acf9-a7f1-456f-827f-20d2f3ce48ca",
            "label": "and",
            "url": "null",
            "text": "null",
            "x": -8,
            "y": 5,
            "size": 3,
            "color": "#ff0000"
        },
        {
            "id": "oval:ssg-test_package_openssh-server_removed:tst:1",
            "label": "oval:ssg-test_package_openssh-server_removed:tst:1",
            "url": "null",
            "text": "null",
            "x": -6,
            "y": 7,
            "size": 3,
            "color": "#ff0000"
        },
        {
            "id": "c7d8b917-4172-4538-91f9-af31b5231f32",
            "label": "and",
            "url": "null",
            "text": "null",
            "x": -7,
            "y": 3,
            "size": 3,
            "color": "#00ff00"
        },
        {
            "id": "f03f128f-20e7-471c-aabe-43789463b4d8",
            "label": "or",
            "url": "null",
            "text": "null",
            "x": -5,
            "y": 5,
            "size": 3,
            "color": "#00ff00"
        },
        {
            "id": "oval:ssg-test_sshd_required:tst:1",
            "label": "oval:ssg-test_sshd_required:tst:1",
            "url": "null",
            "text": "null",
            "x": -3,
            "y": 7,
            "size": 3,
            "color": "#ff0000"
        },
        {
            "id": "448cf546-ec52-4787-b51b-2c57791c1d78",
            "label": "and",
            "url": "null",
            "text": "null",
            "x": -1,
            "y": 7,
            "size": 3,
            "color": "#00ff00"
        },
        {
            "id": "95bd04f6-999f-4276-b483-07acdb12c2f8",
            "label": "and",
            "url": "null",
            "text": "null",
            "x": 0,
            "y": 5,
            "size": 3,
            "color": "#00ff00"
        },
        {
            "id": "oval:ssg-test_package_openssh-server_installed:tst:1",
            "label": "oval:ssg-test_package_openssh-server_installed:tst:1",
            "url": "null",
            "text": "null",
            "x": 2,
            "y": 7,
            "size": 3,
            "color": "#00ff00"
        },
        {
            "id": "oval:ssg-test_sshd_hostbasedauthentication:tst:1",
            "label": "oval:ssg-test_sshd_hostbasedauthentication:tst:1",
            "url": "null",
            "text": "null",
            "x": 3,
            "y": 5,
            "size": 3,
            "color": "#00ff00"
        },
        {
            "id": "oval:ssg-test_sshd_requirement_unset:tst:1",
            "label": "oval:ssg-test_sshd_requirement_unset:tst:1",
            "url": "null",
            "text": "null",
            "x": -7,
            "y": 9,
            "size": 3,
            "color": "#00ff00"
        }
        ],
        "edges": [
        {
            "id": "3703f50e-3d80-465a-afa2-74829833bd5d",
            "source": "xccdf_org.ssgproject.content_rule_disable_host_auth",
            "target": "oval:ssg-disable_host_auth:def:1"
        },
        {
            "id": "7aed4e8d-f5ee-45b0-97ec-46023ed5898a",
            "source": "oval:ssg-disable_host_auth:def:1",
            "target": "8513f7fb-818b-48cd-8d5d-cdaaf7e545ea"
        },
        {
            "id": "507843c4-e8e7-4947-99d2-46524e10cc6a",
            "source": "8513f7fb-818b-48cd-8d5d-cdaaf7e545ea",
            "target": "fcd586ce-b8bd-41e0-857d-04a315d0094e"
        },
        {
            "id": "643b9c1e-bc5c-4bf9-89b3-8acde2941ec1",
            "source": "fcd586ce-b8bd-41e0-857d-04a315d0094e",
            "target": "oval:ssg-test_sshd_not_required:tst:1"
        },
        {
            "id": "4094fe3e-5a81-451d-a4d1-97f930843940",
            "source": "fcd586ce-b8bd-41e0-857d-04a315d0094e",
            "target": "7cbc49a3-771f-4ca5-81c2-376b72cf3625"
        },
        {
            "id": "0b1c78c6-f359-4b54-9a2e-e8010db012cb",
            "source": "7cbc49a3-771f-4ca5-81c2-376b72cf3625",
            "target": "oval:ssg-test_sshd_requirement_unset:tst:1"
        },
        {
            "id": "a401bdf3-d549-4707-9f42-c9961ead9469",
            "source": "8513f7fb-818b-48cd-8d5d-cdaaf7e545ea",
            "target": "b0f1acf9-a7f1-456f-827f-20d2f3ce48ca"
        },
        {
            "id": "de062e4a-6b70-45d6-b46f-587ba1a87828",
            "source": "b0f1acf9-a7f1-456f-827f-20d2f3ce48ca",
            "target": "oval:ssg-test_package_openssh-server_removed:tst:1"
        },
        {
            "id": "7d033520-af48-4a8a-9c4e-290999d8673b",
            "source": "oval:ssg-disable_host_auth:def:1",
            "target": "c7d8b917-4172-4538-91f9-af31b5231f32"
        },
        {
            "id": "db167681-d0f3-47d7-a508-a74fd14e3e24",
            "source": "c7d8b917-4172-4538-91f9-af31b5231f32",
            "target": "f03f128f-20e7-471c-aabe-43789463b4d8"
        },
        {
            "id": "40751914-dae4-4676-8669-19da58543c55",
            "source": "f03f128f-20e7-471c-aabe-43789463b4d8",
            "target": "oval:ssg-test_sshd_required:tst:1"
        },
        {
            "id": "8f7ecaf6-527e-45ea-9963-be87910914ba",
            "source": "f03f128f-20e7-471c-aabe-43789463b4d8",
            "target": "448cf546-ec52-4787-b51b-2c57791c1d78"
        },
        {
            "id": "a8515a07-3710-4eda-b00b-65ec1cf442fd",
            "source": "448cf546-ec52-4787-b51b-2c57791c1d78",
            "target": "oval:ssg-test_sshd_requirement_unset:tst:1"
        },
        {
            "id": "425ef02f-ab95-4586-8fb7-e7fa4b34aaef",
            "source": "c7d8b917-4172-4538-91f9-af31b5231f32",
            "target": "95bd04f6-999f-4276-b483-07acdb12c2f8"
        },
        {
            "id": "2dc39bd1-ff25-4881-bc7b-698e95a7c4a3",
            "source": "95bd04f6-999f-4276-b483-07acdb12c2f8",
            "target": "oval:ssg-test_package_openssh-server_installed:tst:1"
        },
        {
            "id": "25d5aabd-f14a-405a-a372-f7a5b48c8911",
            "source": "c7d8b917-4172-4538-91f9-af31b5231f32",
            "target": "oval:ssg-test_sshd_hostbasedauthentication:tst:1"
        }
        ]
        }
    src = 'data/ssg-fedora-ds-arf.xml'
    rule_id = 'xccdf_org.ssgproject.content_rule_disable_host_auth'
    result = 'true'

    oval_trees_array = tree.oval_tree.xml_to_tree(src)
    for oval_tree in oval_trees_array:
        if oval_tree.node_id == rule_id:
            out_data = oval_tree.to_sigma_dict(0, 0)
            for i in range(len(out_data['nodes'])):
                assert out_data['nodes'][i]['label']==test_data['nodes'][i]['label']
                assert out_data['nodes'][i]['text']==test_data['nodes'][i]['text']
                assert out_data['nodes'][i]['url']==test_data['nodes'][i]['url']
