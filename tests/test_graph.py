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

results_counts1 = {
    'true_cnt': 3,
    'false_cnt': 3,
    'error_cnt': 3,
    'unknown_cnt': 0,
    'noteval_cnt': -1,
    'notappl_cnt': 3
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
                        {'node_id': 2, 'type': 'value',
                            'value': "false", 'child': None},
                        {'node_id': 3, 'type': 'operator', 'value': "xor", 'child': [
                            {'node_id': 4, 'type': 'value',
                                'value': "true", 'child': None},
                            {'node_id': 5, 'type': 'operator', 'value': "one", 'child': [
                                {'node_id': 6, 'type': 'value',
                                    'value': "noteval", 'child': None},
                                {'node_id': 7, 'type': 'value',
                                    'value': "true", 'child': None},
                                {'node_id': 8, 'type': 'value',
                                    'value': "notappl", 'child': None}
                            ]},
                            {'node_id': 9, 'type': 'value', 'value': "error", 'child': None}]},
                        {'node_id': 10, 'type': 'operator', 'value': 'or', 'child': [
                            {'node_id': 11, 'type': 'value',
                                'value': "unknown", 'child': None},
                            {'node_id': 12, 'type': 'value',
                                'value': "true", 'child': None}
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
                               'child': None},
                              {'node_id': 3,
                               'type': 'value',
                               'value': "true",
                               'child': None},
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
    assert graph.evaluate.greater_zero(results_counts, 'noteval_cnt') == False


def test_false_smaller_then_two():
    assert graph.evaluate.smaller_than_two(
        results_counts1, 'true_cnt') == False


def test_false_eq_or_greater_zero_unknown_noteval_notappl():
    assert graph.evaluate.eq_or_greater_zero_unknown_noteval_notappl(
        results_counts1) == False


def test_false_error_unknown_eq_noteval_greater_zero():
    assert graph.evaluate.error_unknown_eq_noteval_greater_zero(
        results_counts) == False


def any_test_parsing_and_evaluate_scan_rule(src, rule_id, result):
    _dir = os.path.dirname(os.path.realpath(__file__))
    FIXTURE_DIR = py.path.local(_dir) / src

    oval_tree = graph.oval_graph.build_nodes_form_xml(
        str(FIXTURE_DIR), rule_id)
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


def any_test_create_node_dict_for_sigmaJs(Tree, out):

    assert Tree._create_node(0, 0) == out


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
    Tree = get_simple_tree()
    any_test_create_node_dict_for_sigmaJs(Tree, out)


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
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'and', [
        graph.oval_graph.OvalNode(2, 'value', "true")
    ]
    )

    any_test_create_node_dict_for_sigmaJs(Tree, out)


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
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'and', [
        graph.oval_graph.OvalNode(2, 'value', "noteval")
    ]
    )

    any_test_create_node_dict_for_sigmaJs(Tree, out)


def test_create_node_dict_for_sigmaJs_3():
    out = {
        'color': '#ff0000',
        'id': 1,
        'label': '1',
        'size': 3,
        'text': 'null',
        'url': 'null',
        'title': 1,
        'x': 0,
        'y': 0
    }
    Tree = graph.oval_graph.OvalNode(1, 'value', 'false')

    any_test_create_node_dict_for_sigmaJs(Tree, out)


def test_create_node_dict_for_sigmaJs_4():
    out = {
        'color': '#00ff00',
        'id': 1,
        'label': '1',
        'size': 3,
        'text': 'null',
        'url': 'null',
        'title': 1,
        'x': 0,
        'y': 0
    }
    Tree = graph.oval_graph.OvalNode(1, 'value', 'true')

    any_test_create_node_dict_for_sigmaJs(Tree, out)


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
    Tree = graph.oval_graph.OvalNode(1, 'value', 'error')

    any_test_create_node_dict_for_sigmaJs(Tree, out)


def test_create_edge_dict_for_sigmaJs():
    print(get_simple_tree()._create_edge(1, 2))
    out = {
        'id': 'random_ID',
        'source': 1,
        'target': 2
    }

    assert get_simple_tree()._create_edge(1, 2)['source'] == out['source']
    assert get_simple_tree()._create_edge(1, 2)['target'] == out['target']


def test_create_array_of_ids_form_tree():
    array = get_simple_tree().create_list_of_id()
    assert array == [1, 2, 3, 4, 5, 6]


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
    test_data = {'nodes': [
        {
            'id': 'xccdf_org.ssgproject.content_rule_accounts_passwords_pam_faillock_deny',
            'label': 'and',
            'url': 'null',
            'text': 'null',
            'title': 'xccdf_org.ssgproject.content_rule_accounts_passwords_pam_faillock_deny',
            'x': -13,
            'y': 0,
            'size': 3,
            'color': '#ff0000'},
        {'id': 'oval:ssg-accounts_passwords_pam_faillock_deny:def:1',
         'label': 'and',
         'url': 'null',
         'text': 'null',
         'title': 'oval:ssg-accounts_passwords_pam_faillock_deny:def:1',
         'x': -13,
         'y': 1,
         'size': 3,
         'color': '#ff0000'},
        {'id': 'oval:ssg-test_accounts_passwords_pam_faillock_preauth_silent_system-auth:tst:1',
         'label': 'test_accounts_passwords_pam_faillock_preauth_silent_system-auth',
         'url': 'null',
         'text': 'null',
         'title': 'oval:ssg-test_accounts_passwords_pam_faillock_preauth_silent_system-auth:tst:1',
         'x': -11,
         'y': 3,
         'size': 3,
         'color': '#ff0000'},
        {'id': 'oval:ssg-test_accounts_passwords_pam_faillock_account_phase_system-auth:tst:1',
         'label': 'test_accounts_passwords_pam_faillock_account_phase_system-auth',
         'url': 'null',
         'text': 'null',
         'title': 'oval:ssg-test_accounts_passwords_pam_faillock_account_phase_system-auth:tst:1',
         'x': -9,
         'y': 3,
         'size': 3,
         'color': '#ff0000'},
        {'id': 'oval:ssg-test_accounts_passwords_pam_faillock_preauth_silent_password-auth:tst:1',
         'label': 'test_accounts_passwords_pam_faillock_preauth_silent_password-auth',
         'url': 'null',
         'text': 'null',
         'title': 'oval:ssg-test_accounts_passwords_pam_faillock_preauth_silent_password-auth:tst:1',
         'x': -7,
         'y': 3,
         'size': 3,
         'color': '#ff0000'},
        {'id': 'oval:ssg-test_accounts_passwords_pam_faillock_account_phase_password-auth:tst:1',
         'label': 'test_accounts_passwords_pam_faillock_account_phase_password-auth',
         'url': 'null',
         'text': 'null',
         'title': 'oval:ssg-test_accounts_passwords_pam_faillock_account_phase_password-auth:tst:1',
         'x': -5,
         'y': 3,
         'size': 3,
         'color': '#ff0000'},
        {'id': 'debcac8c-00b4-49f7-ac9d-0b3634c6f42a',
         'label': 'and',
         'url': 'null',
         'text': 'null',
         'title': 'debcac8c-00b4-49f7-ac9d-0b3634c6f42a',
         'x': -3,
         'y': 3,
         'size': 3,
         'color': '#ff0000'},
        {'id': '6ae09564-8357-48ac-8756-7e93d1a76d17',
         'label': 'or',
         'url': 'null',
         'text': 'null',
         'title': '6ae09564-8357-48ac-8756-7e93d1a76d17',
         'x': -1,
         'y': 5,
         'size': 3,
         'color': '#ff0000'},
        {'id': 'oval:ssg-test_accounts_passwords_pam_faillock_numeric_default_check_system-auth:tst:1',
         'label': 'test_accounts_passwords_pam_faillock_numeric_default_check_system-auth',
         'url': 'null',
         'text': 'null',
         'title': 'oval:ssg-test_accounts_passwords_pam_faillock_numeric_default_check_system-auth:tst:1',
         'x': 1,
         'y': 7,
         'size': 3,
         'color': '#ff0000'},
        {'id': 'oval:ssg-test_accounts_passwords_pam_faillock_authfail_deny_system-auth:tst:1',
         'label': 'test_accounts_passwords_pam_faillock_authfail_deny_system-auth',
         'url': 'null',
         'text': 'null',
         'title': 'oval:ssg-test_accounts_passwords_pam_faillock_authfail_deny_system-auth:tst:1',
         'x': 3,
         'y': 7,
         'size': 3,
         'color': '#ff0000'},
        {'id': '85e05733-2ad9-4388-808e-df7f4a6e1af1',
         'label': 'or',
         'url': 'null',
         'text': 'null',
         'title': '85e05733-2ad9-4388-808e-df7f4a6e1af1',
         'x': 3,
         'y': 5,
         'size': 3,
         'color': '#ff0000'},
        {'id': 'oval:ssg-test_accounts_passwords_pam_faillock_numeric_default_check_password-auth:tst:1',
         'label': 'test_accounts_passwords_pam_faillock_numeric_default_check_password-auth',
         'url': 'null',
         'text': 'null',
         'title': 'oval:ssg-test_accounts_passwords_pam_faillock_numeric_default_check_password-auth:tst:1',
         'x': 5,
         'y': 7,
         'size': 3,
         'color': '#ff0000'},
        {'id': 'oval:ssg-test_accounts_passwords_pam_faillock_authfail_deny_password-auth:tst:1',
         'label': 'test_accounts_passwords_pam_faillock_authfail_deny_password-auth',
         'url': 'null',
         'text': 'null',
         'title': 'oval:ssg-test_accounts_passwords_pam_faillock_authfail_deny_password-auth:tst:1',
         'x': 7,
         'y': 7,
         'size': 3,
         'color': '#ff0000'}],
        'edges': [{'id': '794b350c-d6dd-41cf-8d7a-b52b1e14d895',
                   'source': 'xccdf_org.ssgproject.content_rule_accounts_passwords_pam_faillock_deny',
                   'target': 'oval:ssg-accounts_passwords_pam_faillock_deny:def:1'},
                  {'id': '078b88db-bec0-41cd-80fb-ed06cfeee800',
                   'source': 'oval:ssg-accounts_passwords_pam_faillock_deny:def:1',
                   'target': 'oval:ssg-test_accounts_passwords_pam_faillock_preauth_silent_system-auth:tst:1'},
                  {'id': '99061b30-6d6b-4129-99f2-14a87b40171a',
                   'source': 'oval:ssg-accounts_passwords_pam_faillock_deny:def:1',
                   'target': 'oval:ssg-test_accounts_passwords_pam_faillock_account_phase_system-auth:tst:1'},
                  {'id': '59b04168-2747-485b-a17e-008c35b411ab',
                   'source': 'oval:ssg-accounts_passwords_pam_faillock_deny:def:1',
                   'target': 'oval:ssg-test_accounts_passwords_pam_faillock_preauth_silent_password-auth:tst:1'},
                  {'id': '84be8e5f-7005-477c-8cec-0e8dad87c940',
                   'source': 'oval:ssg-accounts_passwords_pam_faillock_deny:def:1',
                   'target': 'oval:ssg-test_accounts_passwords_pam_faillock_account_phase_password-auth:tst:1'},
                  {'id': '4b6990be-94a5-4f0e-b423-19e2147e856d',
                   'source': 'oval:ssg-accounts_passwords_pam_faillock_deny:def:1',
                   'target': 'debcac8c-00b4-49f7-ac9d-0b3634c6f42a'},
                  {'id': 'c9d4ef13-7444-40d2-b18e-f6f68dce7e9d',
                   'source': 'debcac8c-00b4-49f7-ac9d-0b3634c6f42a',
                   'target': '6ae09564-8357-48ac-8756-7e93d1a76d17'},
                  {'id': '89e28ab1-fc71-42f6-837f-7835d9609034',
                   'source': '6ae09564-8357-48ac-8756-7e93d1a76d17',
                   'target': 'oval:ssg-test_accounts_passwords_pam_faillock_numeric_default_check_system-auth:tst:1'},
                  {'id': '194ee0ab-c1e7-4ccf-ab8c-71ac28112e7a',
                   'source': '6ae09564-8357-48ac-8756-7e93d1a76d17',
                   'target': 'oval:ssg-test_accounts_passwords_pam_faillock_authfail_deny_system-auth:tst:1'},
                  {'id': '79f062b0-db9c-4ad9-9b46-86dc9222f7e9',
                   'source': 'debcac8c-00b4-49f7-ac9d-0b3634c6f42a',
                   'target': '85e05733-2ad9-4388-808e-df7f4a6e1af1'},
                  {'id': '043ac902-5962-407c-bdd6-d7cb71438a44',
                   'source': '85e05733-2ad9-4388-808e-df7f4a6e1af1',
                   'target': 'oval:ssg-test_accounts_passwords_pam_faillock_numeric_default_check_password-auth:tst:1'},
                  {'id': '0c0aa354-8da5-4d43-980d-187e20852b34',
                   'source': '85e05733-2ad9-4388-808e-df7f4a6e1af1',
                   'target': 'oval:ssg-test_accounts_passwords_pam_faillock_authfail_deny_password-auth:tst:1'}]}
    src = 'data/ssg-fedora-ds-arf.xml'
    rule_id = 'xccdf_org.ssgproject.content_rule_accounts_passwords_pam_faillock_deny'

    oval_tree = graph.oval_graph.build_nodes_form_xml(src, rule_id)
    if oval_tree.node_id == rule_id:
        out_data = oval_tree.to_sigma_dict(0, 0)
        for i in range(len(out_data['nodes'])):
            assert out_data['nodes'][i]['label'] == test_data['nodes'][i]['label']
            assert out_data['nodes'][i]['text'] == test_data['nodes'][i]['text']
            assert out_data['nodes'][i]['url'] == test_data['nodes'][i]['url']


def test_transformation_tree_to_Json_for_SigmaJs_with_duplicated_test():
    test_data = {'nodes': [{'id': 'xccdf_org.ssgproject.content_rule_disable_host_auth',
                            'label': 'and',
                            'url': 'null',
                            'text': 'null',
                            'title': 'xccdf_org.ssgproject.content_rule_disable_host_auth',
                            'x': -17,
                            'y': 0,
                            'size': 3,
                            'color': '#00ff00'},
                           {'id': 'oval:ssg-disable_host_auth:def:1',
                            'label': 'or',
                            'url': 'null',
                            'text': 'null',
                            'title': 'oval:ssg-disable_host_auth:def:1',
                            'x': -17,
                            'y': 1,
                            'size': 3,
                            'color': '#00ff00'},
                           {'id': '22ec5137-0406-41a1-871d-3f8e103b9bdb',
                            'label': 'and',
                            'url': 'null',
                            'text': 'null',
                            'title': '22ec5137-0406-41a1-871d-3f8e103b9bdb',
                            'x': -15,
                            'y': 3,
                            'size': 3,
                            'color': '#ff0000'},
                           {'id': '25e0a4f1-5a54-48cf-95d5-8eea945ac7e2',
                            'label': 'or',
                            'url': 'null',
                            'text': 'null',
                            'title': '25e0a4f1-5a54-48cf-95d5-8eea945ac7e2',
                            'x': -13,
                            'y': 5,
                            'size': 3,
                            'color': '#00ff00'},
                           {'id': 'oval:ssg-test_sshd_not_required:tst:1',
                            'label': 'test_sshd_not_required',
                            'url': 'null',
                            'text': 'null',
                            'title': 'oval:ssg-test_sshd_not_required:tst:1',
                            'x': -11,
                            'y': 7,
                            'size': 3,
                            'color': '#ff0000'},
                           {'id': '37db2c90-8fd2-41d1-b87d-ccbe6c8212a9',
                            'label': 'and',
                            'url': 'null',
                            'text': 'null',
                            'title': '37db2c90-8fd2-41d1-b87d-ccbe6c8212a9',
                            'x': -9,
                            'y': 7,
                            'size': 3,
                            'color': '#00ff00'},
                           {'id': '11c91596-51f3-44c1-8d99-d67c50559038',
                            'label': 'and',
                            'url': 'null',
                            'text': 'null',
                            'title': '11c91596-51f3-44c1-8d99-d67c50559038',
                            'x': -8,
                            'y': 5,
                            'size': 3,
                            'color': '#ff0000'},
                           {'id': 'oval:ssg-test_package_openssh-server_removed:tst:1',
                            'label': 'test_package_openssh-server_removed',
                            'url': 'null',
                            'text': 'null',
                            'title': 'oval:ssg-test_package_openssh-server_removed:tst:1',
                            'x': -6,
                            'y': 7,
                            'size': 3,
                            'color': '#ff0000'},
                           {'id': '42c9a387-08a6-4767-a25e-9eabb43b8ae4',
                            'label': 'and',
                            'url': 'null',
                            'text': 'null',
                            'title': '42c9a387-08a6-4767-a25e-9eabb43b8ae4',
                            'x': -7,
                            'y': 3,
                            'size': 3,
                            'color': '#00ff00'},
                           {'id': '89cf4075-0f24-442b-ab01-0bb93d5a19a0',
                            'label': 'or',
                            'url': 'null',
                            'text': 'null',
                            'title': '89cf4075-0f24-442b-ab01-0bb93d5a19a0',
                            'x': -5,
                            'y': 5,
                            'size': 3,
                            'color': '#00ff00'},
                           {'id': 'oval:ssg-test_sshd_required:tst:1',
                            'label': 'test_sshd_required',
                            'url': 'null',
                            'text': 'null',
                            'title': 'oval:ssg-test_sshd_required:tst:1',
                            'x': -3,
                            'y': 7,
                            'size': 3,
                            'color': '#ff0000'},
                           {'id': '10126dbc-be9c-49ce-b071-ab92c2b8a0df',
                            'label': 'and',
                            'url': 'null',
                            'text': 'null',
                            'title': '10126dbc-be9c-49ce-b071-ab92c2b8a0df',
                            'x': -1,
                            'y': 7,
                            'size': 3,
                            'color': '#00ff00'},
                           {'id': '7a6dd54f-4e6c-4057-8c94-6598ee992c89',
                            'label': 'and',
                            'url': 'null',
                            'text': 'null',
                            'title': '7a6dd54f-4e6c-4057-8c94-6598ee992c89',
                            'x': 0,
                            'y': 5,
                            'size': 3,
                            'color': '#00ff00'},
                           {'id': 'oval:ssg-test_package_openssh-server_installed:tst:1',
                            'label': 'test_package_openssh-server_installed',
                            'url': 'null',
                            'text': 'null',
                            'title': 'oval:ssg-test_package_openssh-server_installed:tst:1',
                            'x': 2,
                            'y': 7,
                            'size': 3,
                            'color': '#00ff00'},
                           {'id': 'oval:ssg-test_sshd_hostbasedauthentication:tst:1',
                            'label': 'test_sshd_hostbasedauthentication',
                            'url': 'null',
                            'text': 'null',
                            'title': 'oval:ssg-test_sshd_hostbasedauthentication:tst:1',
                            'x': 3,
                            'y': 5,
                            'size': 3,
                            'color': '#00ff00'},
                           {'id': 'oval:ssg-test_sshd_requirement_unset:tst:1',
                            'label': 'test_sshd_requirement_unset',
                            'url': 'null',
                            'text': 'null',
                            'title': 'oval:ssg-test_sshd_requirement_unset:tst:1',
                            'x': -7,
                            'y': 9,
                            'size': 3,
                            'color': '#00ff00'}],
                 'edges': [{'id': 'f89168c8-7e46-44f0-8a52-04b0af6330f1',
                            'source': 'xccdf_org.ssgproject.content_rule_disable_host_auth',
                            'target': 'oval:ssg-disable_host_auth:def:1'},
                           {'id': '0237cfd3-642e-484e-80be-c53788cc0585',
                            'source': 'oval:ssg-disable_host_auth:def:1',
                            'target': '22ec5137-0406-41a1-871d-3f8e103b9bdb'},
                           {'id': 'f2be3ac1-51f8-4fb3-b836-2fc2426460cd',
                            'source': '22ec5137-0406-41a1-871d-3f8e103b9bdb',
                            'target': '25e0a4f1-5a54-48cf-95d5-8eea945ac7e2'},
                           {'id': '71292795-3b1d-48b4-ba37-0bc1821272c4',
                            'source': '25e0a4f1-5a54-48cf-95d5-8eea945ac7e2',
                            'target': 'oval:ssg-test_sshd_not_required:tst:1'},
                           {'id': '70cf0ff2-0b42-47a7-b0c0-a8b4cacb33db',
                            'source': '25e0a4f1-5a54-48cf-95d5-8eea945ac7e2',
                            'target': '37db2c90-8fd2-41d1-b87d-ccbe6c8212a9'},
                           {'id': '7d6f1fb2-081d-4d86-97a4-9f2292699f25',
                            'source': '37db2c90-8fd2-41d1-b87d-ccbe6c8212a9',
                            'target': 'oval:ssg-test_sshd_requirement_unset:tst:1'},
                           {'id': 'f147b183-f8b7-4ee7-9410-224d6d41f55b',
                            'source': '22ec5137-0406-41a1-871d-3f8e103b9bdb',
                            'target': '11c91596-51f3-44c1-8d99-d67c50559038'},
                           {'id': '458a4e10-69ed-4f6c-a2f4-47ba6dde7905',
                            'source': '11c91596-51f3-44c1-8d99-d67c50559038',
                            'target': 'oval:ssg-test_package_openssh-server_removed:tst:1'},
                           {'id': 'a43d4c25-b1a9-4fe1-ad49-4698b0f5bec7',
                            'source': 'oval:ssg-disable_host_auth:def:1',
                            'target': '42c9a387-08a6-4767-a25e-9eabb43b8ae4'},
                           {'id': '25919b3f-a28a-4e70-ae72-f58aa8457da3',
                            'source': '42c9a387-08a6-4767-a25e-9eabb43b8ae4',
                            'target': '89cf4075-0f24-442b-ab01-0bb93d5a19a0'},
                           {'id': '368263c5-35e2-4bac-b851-dafc737dc4fb',
                            'source': '89cf4075-0f24-442b-ab01-0bb93d5a19a0',
                            'target': 'oval:ssg-test_sshd_required:tst:1'},
                           {'id': 'bd9006b7-f09d-4a78-a3d0-7a4f4420fe01',
                            'source': '89cf4075-0f24-442b-ab01-0bb93d5a19a0',
                            'target': '10126dbc-be9c-49ce-b071-ab92c2b8a0df'},
                           {'id': '094d0dd8-ce8d-4d0a-b502-020a4d2525f6',
                            'source': '10126dbc-be9c-49ce-b071-ab92c2b8a0df',
                            'target': 'oval:ssg-test_sshd_requirement_unset:tst:1'},
                           {'id': '62057baa-2eb8-41d8-b74b-584d69092aca',
                            'source': '42c9a387-08a6-4767-a25e-9eabb43b8ae4',
                            'target': '7a6dd54f-4e6c-4057-8c94-6598ee992c89'},
                           {'id': 'b4abd067-d93c-465c-95c6-d29d38b4ddf0',
                            'source': '7a6dd54f-4e6c-4057-8c94-6598ee992c89',
                            'target': 'oval:ssg-test_package_openssh-server_installed:tst:1'},
                           {'id': '4c5b3aa0-0b1f-411e-b4ca-badf7dd7ab69',
                            'source': '42c9a387-08a6-4767-a25e-9eabb43b8ae4',
                            'target': 'oval:ssg-test_sshd_hostbasedauthentication:tst:1'}]}

    src = 'data/ssg-fedora-ds-arf.xml'
    rule_id = 'xccdf_org.ssgproject.content_rule_disable_host_auth'

    oval_tree = graph.oval_graph.build_nodes_form_xml(src, rule_id)

    if oval_tree.node_id == rule_id:
        out_data = oval_tree.to_sigma_dict(0, 0)
        print(out_data)
        for i in range(len(out_data['nodes'])):
            assert out_data['nodes'][i]['label'] == test_data['nodes'][i]['label']
            assert out_data['nodes'][i]['text'] == test_data['nodes'][i]['text']
            assert out_data['nodes'][i]['url'] == test_data['nodes'][i]['url']


def test_and_or_eq_zero():
    assert graph.evaluate.and_or_eq_zero('and', results_counts) == False
    assert graph.evaluate.and_or_eq_zero('or', results_counts) == False
    assert graph.evaluate.and_or_eq_zero('xor', results_counts) is None


def test_get_def_id_by_rule_id():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    _dir = os.path.dirname(os.path.realpath(__file__))
    FIXTURE_DIR = py.path.local(_dir) / src

    parser = graph.xml_parser.xml_parser(str(FIXTURE_DIR))

    with pytest.raises(ValueError) as e:
        parser.get_def_id_by_rule_id('hello')
    assert str(
        e.value) == 'err- 404 rule not found!'
