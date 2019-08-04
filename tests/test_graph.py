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
            'x': 0,
            'y': 0,
            'size': 3,
            'color': '#ff0000'},
        {
            'id': 'oval:ssg-accounts_passwords_pam_faillock_deny:def:1',
            'label': 'and',
            'url': 'null',
            'text': 'null',
            'title': 'oval:ssg-accounts_passwords_pam_faillock_deny:def:1',
            'x': 0,
            'y': 1,
            'size': 3,
            'color': '#ff0000'},
        {
            'id': 'oval:ssg-test_accounts_passwords_pam_faillock_preauth_silent_system-auth:tst:1',
            'label': 'accounts_passwords_pam_faillock_preauth_silent_system-auth',
            'url': 'null',
            'text': 'null',
            'title': 'oval:ssg-test_accounts_passwords_pam_faillock_preauth_silent_system-auth:tst:1',
            'x': -4,
            'y': 2.36,
            'size': 3,
            'color': '#ff0000'},
        {
            'id': 'oval:ssg-test_accounts_passwords_pam_faillock_account_phase_system-auth:tst:1',
            'label': 'accounts_passwords_pam_faillock_account_phase_system-auth',
            'url': 'null',
            'text': 'null',
            'title': 'oval:ssg-test_accounts_passwords_pam_faillock_account_phase_system-auth:tst:1',
            'x': -2,
            'y': 2.7199999999999998,
            'size': 3,
            'color': '#ff0000'},
       {
           'id': 'oval:ssg-test_accounts_passwords_pam_faillock_preauth_silent_password-auth:tst:1',
            'label': 'accounts_passwords_pam_faillock_preauth_silent_password-auth',
            'url': 'null',
            'text': 'null',
            'title': 'oval:ssg-test_accounts_passwords_pam_faillock_preauth_silent_password-auth:tst:1',
            'x': 0,
            'y': 3.08,
            'size': 3,
            'color': '#ff0000'},
        {
            'id': 'oval:ssg-test_accounts_passwords_pam_faillock_account_phase_password-auth:tst:1',
            'label': 'accounts_passwords_pam_faillock_account_phase_password-auth',
            'url': 'null',
            'text': 'null',
            'title': 'oval:ssg-test_accounts_passwords_pam_faillock_account_phase_password-auth:tst:1',
            'x': 2,
            'y': 3.44,
            'size': 3,
            'color': '#ff0000'},
        {
            'id': '53d15de4-262b-469f-8df6-dd93d8d9a2de',
            'label': 'and',
            'url': 'null',
            'text': 'null',
            'title': '53d15de4-262b-469f-8df6-dd93d8d9a2de',
            'x': 4,
            'y': 3.8,
            'size': 3,
            'color': '#ff0000'},
        {
            'id': '551bbfca-b55f-4b67-a6ca-fefa9a886ec8',
            'label': 'or',
            'url': 'null',
            'text': 'null',
            'title': '551bbfca-b55f-4b67-a6ca-fefa9a886ec8',
            'x': -2,
            'y': 4.1,
            'size': 3,
            'color': '#ff0000'},
        {
            'id': '1b9f74b8-1c58-4b09-969b-2413e9594f08',
            'label': 'or',
            'url': 'null',
            'text': 'null',
            'title': '1b9f74b8-1c58-4b09-969b-2413e9594f08',
            'x': 2,
            'y': 4.1,
            'size': 3,
            'color': '#ff0000'},
        {
            'id': 'oval:ssg-test_accounts_passwords_pam_faillock_numeric_default_check_system-auth:tst:1',
            'label': 'accounts_passwords_pam_faillock_numeric_default_check_system-auth',
            'url': 'null',
            'text': 'null',
            'title': 'oval:ssg-test_accounts_passwords_pam_faillock_numeric_default_check_system-auth:tst:1',
            'x': -4,
            'y': 4.36,
            'size': 3,
            'color': '#ff0000'},
        {
            'id': 'oval:ssg-test_accounts_passwords_pam_faillock_authfail_deny_system-auth:tst:1',
            'label': 'accounts_passwords_pam_faillock_authfail_deny_system-auth',
            'url': 'null',
            'text': 'null',
            'title': 'oval:ssg-test_accounts_passwords_pam_faillock_authfail_deny_system-auth:tst:1',
            'x': -2,
            'y': 4.72,
            'size': 3,
            'color': '#ff0000'},
        {
            'id': 'oval:ssg-test_accounts_passwords_pam_faillock_numeric_default_check_password-auth:tst:1',
            'label': 'accounts_passwords_pam_faillock_numeric_default_check_password-auth',
            'url': 'null',
            'text': 'null',
            'title': 'oval:ssg-test_accounts_passwords_pam_faillock_numeric_default_check_password-auth:tst:1',
            'x': 0,
            'y': 5.08,
            'size': 3,
            'color': '#ff0000'},
        {
            'id': 'oval:ssg-test_accounts_passwords_pam_faillock_authfail_deny_password-auth:tst:1',
            'label': 'accounts_passwords_pam_faillock_authfail_deny_password-auth',
            'url': 'null',
            'text': 'null',
            'title': 'oval:ssg-test_accounts_passwords_pam_faillock_authfail_deny_password-auth:tst:1',
            'x': 2,
            'y': 5.4399999999999995,
            'size': 3,
            'color': '#ff0000'}],
        'edges': [
        {
            'id': 'b56a7fd0-f53e-45d3-83af-bd0c4bfa87cb',
            'source': 'xccdf_org.ssgproject.content_rule_accounts_passwords_pam_faillock_deny',
            'target': 'oval:ssg-accounts_passwords_pam_faillock_deny:def:1'},
        {
            'id': '7107c6c9-b22e-4bf0-a67f-9c79f48825be',
            'source': 'oval:ssg-accounts_passwords_pam_faillock_deny:def:1',
            'target': 'oval:ssg-test_accounts_passwords_pam_faillock_preauth_silent_system-auth:tst:1'},
        {
            'id': '693179e3-2aea-4d9b-b021-65488993e39a',
            'source': 'oval:ssg-accounts_passwords_pam_faillock_deny:def:1',
            'target': 'oval:ssg-test_accounts_passwords_pam_faillock_account_phase_system-auth:tst:1'},
        {
            'id': 'd179dff2-9c03-4455-a59e-6fb2ad15cdf4',
            'source': 'oval:ssg-accounts_passwords_pam_faillock_deny:def:1',
            'target': 'oval:ssg-test_accounts_passwords_pam_faillock_preauth_silent_password-auth:tst:1'},
        {
            'id': '792c8d34-84f5-49c7-be98-965a977466ac',
            'source': 'oval:ssg-accounts_passwords_pam_faillock_deny:def:1',
            'target': 'oval:ssg-test_accounts_passwords_pam_faillock_account_phase_password-auth:tst:1'},
        {
            'id': 'd8eee053-a0f6-4a73-8867-f17ffbc4b095',
            'source': 'oval:ssg-accounts_passwords_pam_faillock_deny:def:1',
            'target': '53d15de4-262b-469f-8df6-dd93d8d9a2de'},
        {
            'id': 'ff763a4b-2a9f-4f72-be96-f8cc0dcbdfbf',
            'source': '53d15de4-262b-469f-8df6-dd93d8d9a2de',
            'target': '551bbfca-b55f-4b67-a6ca-fefa9a886ec8'},
        {
            'id': 'dfdfcb00-97aa-4280-bc16-7f82c151373e',
            'source': '551bbfca-b55f-4b67-a6ca-fefa9a886ec8',
            'target': 'oval:ssg-test_accounts_passwords_pam_faillock_numeric_default_check_system-auth:tst:1'},
        {
            'id': '05e35e95-f42a-419b-acd8-dff9726956f8',
            'source': '551bbfca-b55f-4b67-a6ca-fefa9a886ec8',
            'target': 'oval:ssg-test_accounts_passwords_pam_faillock_authfail_deny_system-auth:tst:1'},
        {
            'id': 'ddbc2340-bbc1-4a0f-be9f-2a4884b40408',
            'source': '53d15de4-262b-469f-8df6-dd93d8d9a2de',
            'target': '1b9f74b8-1c58-4b09-969b-2413e9594f08'},
        {
            'id': 'b973e01b-33f6-4a75-a2b1-c3b478ef4890',
            'source': '1b9f74b8-1c58-4b09-969b-2413e9594f08',
            'target': 'oval:ssg-test_accounts_passwords_pam_faillock_numeric_default_check_password-auth:tst:1'},
        {
            'id': '6acd02b8-7c44-49c4-8040-94f0305721d6',
            'source': '1b9f74b8-1c58-4b09-969b-2413e9594f08',
            'target': 'oval:ssg-test_accounts_passwords_pam_faillock_authfail_deny_password-auth:tst:1'}]}

    src = 'data/ssg-fedora-ds-arf.xml'
    rule_id = 'xccdf_org.ssgproject.content_rule_accounts_passwords_pam_faillock_deny'

    oval_tree = graph.oval_graph.build_nodes_form_xml(src, rule_id)
    if oval_tree.node_id == rule_id:
        out_data = oval_tree.to_sigma_dict(0, 0)
        print(out_data)
        for i in range(len(out_data['nodes'])):
            assert out_data['nodes'][i]['label'] == test_data['nodes'][i]['label']
            assert out_data['nodes'][i]['text'] == test_data['nodes'][i]['text']
            assert out_data['nodes'][i]['url'] == test_data['nodes'][i]['url']


def test_transformation_tree_to_Json_for_SigmaJs_with_duplicated_test():
    test_data = {'nodes': [
        {
            'id': 'xccdf_org.ssgproject.content_rule_disable_host_auth',
            'label': 'and',
            'url': 'null',
            'text': 'null',
            'title': 'xccdf_org.ssgproject.content_rule_disable_host_auth',
            'x': 0,
            'y': 0,
            'size': 3,
            'color': '#00ff00'},
        {
            'id': 'oval:ssg-disable_host_auth:def:1',
            'label': 'or',
            'url': 'null',
            'text': 'null',
            'title': 'oval:ssg-disable_host_auth:def:1',
            'x': 0,
            'y': 1,
            'size': 3,
            'color': '#00ff00'},
        {
            'id': '877adf97-04e6-4e2f-af1a-2b75f4b5c0ac',
            'label': 'and',
            'url': 'null',
            'text': 'null',
            'title': '877adf97-04e6-4e2f-af1a-2b75f4b5c0ac',
            'x': -2,
            'y': 2,
            'size': 3,
            'color': '#ff0000'},
        {
            'id': '5eb52597-0ad6-44b0-9df9-1782c8429962',
            'label': 'and',
            'url': 'null',
            'text': 'null',
            'title': '5eb52597-0ad6-44b0-9df9-1782c8429962',
            'x': 2,
            'y': 2,
            'size': 3,
            'color': '#00ff00'},
        {
            'id': '49024905-176a-4acd-9218-4f7966fa4f76',
            'label': 'or',
            'url': 'null',
            'text': 'null',
            'title': '49024905-176a-4acd-9218-4f7966fa4f76',
            'x': -4,
            'y': 3,
            'size': 3,
            'color': '#00ff00'},
        {
            'id': '300c4561-ca86-49db-ac8d-4c7471f2aafd',
            'label': 'and',
            'url': 'null',
            'text': 'null',
            'title': '300c4561-ca86-49db-ac8d-4c7471f2aafd',
            'x': -2,
            'y': 3,
            'size': 3,
            'color': '#ff0000'},
       {
            'id': 'a11311fb-f598-41ef-82da-80f96a4b0db3',
            'label': 'or',
            'url': 'null',
            'text': 'null',
            'title': 'a11311fb-f598-41ef-82da-80f96a4b0db3',
            'x': 0,
            'y': 3,
            'size': 3,
            'color': '#00ff00'},
        {
            'id': '5ccd4201-a08d-4c77-8593-089a30024435',
            'label': 'and',
            'url': 'null',
            'text': 'null',
            'title': '5ccd4201-a08d-4c77-8593-089a30024435',
            'x': 2,
            'y': 3,
            'size': 3,
            'color': '#00ff00'},
        {
            'id': 'oval:ssg-test_sshd_hostbasedauthentication:tst:1',
            'label': 'sshd_hostbasedauthentication',
            'url': 'null',
            'text': 'null',
            'title': 'oval:ssg-test_sshd_hostbasedauthentication:tst:1',
            'x': 4,
            'y': 3.36,
            'size': 3,
            'color': '#00ff00'},
        {
            'id': 'oval:ssg-test_sshd_not_required:tst:1',
            'label': 'sshd_not_required',
            'url': 'null',
            'text': 'null',
            'title': 'oval:ssg-test_sshd_not_required:tst:1',
            'x': -6,
            'y': 4,
            'size': 3,
            'color': '#ff0000'},
        {
            'id': 'e1a2009b-1612-4580-b72b-482873e6ba5e',
            'label': 'and',
            'url': 'null',
            'text': 'null',
            'title': 'e1a2009b-1612-4580-b72b-482873e6ba5e',
            'x': -4,
            'y': 4,
            'size': 3,
            'color': '#00ff00'},
        {
            'id': 'oval:ssg-test_package_openssh-server_removed:tst:1',
            'label': 'package_openssh-server_removed',
            'url': 'null',
            'text': 'null',
            'title': 'oval:ssg-test_package_openssh-server_removed:tst:1',
            'x': -2,
            'y': 4.36,
            'size': 3,
            'color': '#ff0000'},
        {
            'id': 'oval:ssg-test_sshd_required:tst:1',
            'label': 'sshd_required',
            'url': 'null',
            'text': 'null',
            'title': 'oval:ssg-test_sshd_required:tst:1',
            'x': 0,
            'y': 4,
            'size': 3,
            'color': '#ff0000'},
        {
            'id': '54318a01-99bb-4b72-8111-3600e99cbc64',
            'label': 'and',
            'url': 'null',
            'text': 'null',
            'title': '54318a01-99bb-4b72-8111-3600e99cbc64',
            'x': 2,
            'y': 4,
            'size': 3,
            'color': '#00ff00'},
        {
            'id': 'oval:ssg-test_package_openssh-server_installed:tst:1',
            'label': 'package_openssh-server_installed',
            'url': 'null',
            'text': 'null',
            'title': 'oval:ssg-test_package_openssh-server_installed:tst:1',
            'x': 4,
            'y': 4.36,
            'size': 3,
            'color': '#00ff00'},
        {
            'id': 'oval:ssg-test_sshd_requirement_unset:tst:1',
            'label': 'sshd_requirement_unset',
            'url': 'null',
            'text': 'null',
            'title': 'oval:ssg-test_sshd_requirement_unset:tst:1',
            'x': 0,
            'y': 5,
            'size': 3,
            'color': '#00ff00'}],
        'edges': [
            {
                'id': 'eea56f4a-7cef-4be9-b0fc-0f472e56fccf',
                'source': 'xccdf_org.ssgproject.content_rule_disable_host_auth',
                'target': 'oval:ssg-disable_host_auth:def:1'},
            {
                'id': '95d39f35-5e43-417a-9be6-fe2d534648eb',
                'source': 'oval:ssg-disable_host_auth:def:1',
                'target': '877adf97-04e6-4e2f-af1a-2b75f4b5c0ac'},
            {
                'id': '81bee78f-0040-45cd-ac6f-391d7d3b5c4b',
                'source': '877adf97-04e6-4e2f-af1a-2b75f4b5c0ac',
                'target': '49024905-176a-4acd-9218-4f7966fa4f76'},
            {
                'id': '0fa824cf-3a0b-4b2c-8142-c6a1398b8854',
                'source': '49024905-176a-4acd-9218-4f7966fa4f76',
                'target': 'oval:ssg-test_sshd_not_required:tst:1'},
            {
                'id': '2a8aeff8-c9d0-46bf-ba6f-53781a511aa6',
                'source': '49024905-176a-4acd-9218-4f7966fa4f76',
                'target': 'e1a2009b-1612-4580-b72b-482873e6ba5e'},
            {
                'id': '02bcdc1b-bdc2-4562-872b-a2f48c047b4a',
                'source': 'e1a2009b-1612-4580-b72b-482873e6ba5e',
                'target': 'oval:ssg-test_sshd_requirement_unset:tst:1'},
            {
                'id': '5a85614d-ec49-43e4-b193-e4ab9915de37',
                'source': '877adf97-04e6-4e2f-af1a-2b75f4b5c0ac',
                'target': '300c4561-ca86-49db-ac8d-4c7471f2aafd'},
            {
                'id': 'b07ceea7-fbef-4a7d-870f-7b2f732e2dc4',
                'source': '300c4561-ca86-49db-ac8d-4c7471f2aafd',
                'target': 'oval:ssg-test_package_openssh-server_removed:tst:1'},
            {
                'id': '2c82da7f-321f-4cdb-a26e-bda1e0c770eb',
                'source': 'oval:ssg-disable_host_auth:def:1',
                'target': '5eb52597-0ad6-44b0-9df9-1782c8429962'},
            {
                'id': '04e08f99-7dc4-4ec0-9f61-c095a5d31149',
                'source': '5eb52597-0ad6-44b0-9df9-1782c8429962',
                'target': 'a11311fb-f598-41ef-82da-80f96a4b0db3'},
            {
                'id': 'db01fc1a-6575-4501-8694-88799fd6aa22',
                'source': 'a11311fb-f598-41ef-82da-80f96a4b0db3',
                'target': 'oval:ssg-test_sshd_required:tst:1'},
            {
                'id': 'e781cbf0-923f-40a1-8f0d-62af77b6657e',
                'source': 'a11311fb-f598-41ef-82da-80f96a4b0db3',
                'target': '54318a01-99bb-4b72-8111-3600e99cbc64'},
            {
                'id': 'f71355af-8b58-4508-8e4a-fb643a004461',
                'source': '54318a01-99bb-4b72-8111-3600e99cbc64',
                'target': 'oval:ssg-test_sshd_requirement_unset:tst:1'},
            {
                'id': 'f1737acb-0bf9-418f-973a-4148ce971d80',
                'source': '5eb52597-0ad6-44b0-9df9-1782c8429962',
                'target': '5ccd4201-a08d-4c77-8593-089a30024435'},
            {
                'id': '8218b9ac-c8f6-461b-a25e-e57c33bdb96f',
                'source': '5ccd4201-a08d-4c77-8593-089a30024435',
                'target': 'oval:ssg-test_package_openssh-server_installed:tst:1'},
            {
                'id': '6d357f2f-2b98-44f1-a8ae-f7f7d4accaf2',
                'source': '5eb52597-0ad6-44b0-9df9-1782c8429962',
                'target': 'oval:ssg-test_sshd_hostbasedauthentication:tst:1'}]}

    src = 'data/ssg-fedora-ds-arf.xml'
    rule_id = 'xccdf_org.ssgproject.content_rule_disable_host_auth'

    oval_tree = graph.oval_graph.build_nodes_form_xml(src, rule_id)

    if oval_tree.node_id == rule_id:
        out_data = oval_tree.to_sigma_dict(0, 0)
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
