import graph.oval_graph
import pytest
import tests.any_test_help


def test_bad_tree():
    with pytest.raises(ValueError) as e:
        bad_tree()
    assert str(
        e.value) == 'err- true, false, error, unknown. noteval, notappl have not child!'

    with pytest.raises(ValueError) as e:
        tree_only_and()
    assert str(e.value) == 'err- OR, XOR, ONE, AND have child!'

    with pytest.raises(ValueError) as e:
        tree_only_or()
    assert str(e.value) == 'err- OR, XOR, ONE, AND have child!'

    with pytest.raises(ValueError) as e:
        tree_with_bad_type()
    assert str(e.value) == 'err- unknown type'

    with pytest.raises(ValueError) as e:
        tree_with_bad_value_of_operator()
    assert str(e.value) == 'err- unknown operator'

    with pytest.raises(ValueError) as e:
        tree_with_bad_value_of_value()
    assert str(e.value) == 'err- unknown value'

    with pytest.raises(ValueError) as e:
        tree_with_bad_value_of_negation()
    assert str(e.value) == 'err- negation si bool (only True or False)'

# degenered trees


def bad_tree():
    """
         t
         |
        and
         |
         t
    """
    t = graph.oval_graph.OvalNode(
        1, "value", "true", False, [
            graph.oval_graph.OvalNode(
                2, "operator", "and", False, [
                    graph.oval_graph.OvalNode(
                        3, "value", "true", False)])])
    return


def tree_only_or():
    """
        or
    """
    Tree = graph.oval_graph.OvalNode(1, "operator", 'or', False)
    return


def tree_only_and():
    """
        and
    """
    Tree = graph.oval_graph.OvalNode(1, "operator", 'and', False)
    return


def tree_with_bad_value_of_operator():
    Tree = graph.oval_graph.OvalNode(1, "operator", 'nad', False)
    return


def tree_with_bad_value_of_value():
    Tree = graph.oval_graph.OvalNode(1, "value", 'and', False)
    return


def tree_with_bad_type():
    Tree = graph.oval_graph.OvalNode(1, "auto", 'and', False)
    return


def tree_with_bad_value_of_negation():
    Tree = graph.oval_graph.OvalNode(1, "value", 'true', "negovane_auto")
    return

# normal trees


def test_UPPERCASETree():
    t = graph.oval_graph.OvalNode(
        1, "OPERATOR", "AND", False, [
            graph.oval_graph.OvalNode(
                2, "VALUE", "TRUE", False), graph.oval_graph.OvalNode(
                3, "VALUE", "NOTAPPL", False)])


def test_bigOvalTree():
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'and', False, [
        graph.oval_graph.OvalNode(2, 'value', "false", False),
        graph.oval_graph.OvalNode(3, 'operator', "xor", False, [
            graph.oval_graph.OvalNode(4, 'value', 'true', False),
            graph.oval_graph.OvalNode(5, 'operator', 'one', False, [
                graph.oval_graph.OvalNode(6, 'value', 'noteval', False),
                graph.oval_graph.OvalNode(7, 'value', 'true', False),
                graph.oval_graph.OvalNode(8, 'value', 'notappl', False)
            ]
            ),
            graph.oval_graph.OvalNode(9, 'value', 'error', False)
        ]
        ),
        graph.oval_graph.OvalNode(10, 'operator', 'or', False, [
            graph.oval_graph.OvalNode(11, 'value', "unknown", False),
            graph.oval_graph.OvalNode(12, 'value', "true", False)
        ]
        )
    ]
    )

    test_data_src = 'test_data/bigOvalTree.json'
    dict_of_tree = tests.any_test_help.any_get_test_data_json(test_data_src)
    tests.any_test_help.any_test_treeEvaluation_with_tree(Tree, "false")
    tests.any_test_help.any_test_tree_to_dict_of_tree(Tree, dict_of_tree)
    tests.any_test_help.find_any_node(Tree, 5)
    tests.any_test_help.any_test_dict_to_tree(dict_of_tree)

###################################################


def test_treeRepr():
    """
        and
         |
         f
    """
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'and', False, [
        graph.oval_graph.OvalNode(2, 'value', "false", False)
    ]
    )
    assert str(Tree) == "and"


def test_add_to_tree():
    """
        and
         |
         f
    """

    test_data_src = 'test_data/add_to_tree.json'
    dict_of_tree = tests.any_test_help.any_get_test_data_json(test_data_src)

    Tree = graph.oval_graph.OvalNode(1, 'operator', 'and', False, [
        graph.oval_graph.OvalNode(2, 'value', "false", False)
    ]
    )
    Tree1 = graph.oval_graph.OvalNode(3, 'value', "true", False)
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
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'and', False, [
        graph.oval_graph.OvalNode(2, 'value', "true", False),
        graph.oval_graph.OvalNode(3, 'value', "false", False),
        graph.oval_graph.OvalNode(4, 'operator', 'or', False, [
            graph.oval_graph.OvalNode(5, 'value', "false", False),
            graph.oval_graph.OvalNode(6, 'value', "true", False)
        ]
        )
    ]
    )

    Tree.change_tree_value(3, "true")
    tests.any_test_help.any_test_treeEvaluation_with_tree(Tree, "true")


def test_node_operator_negate():
    """
        !and
         |
         f
    """
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'and', True, [
        graph.oval_graph.OvalNode(2, 'value', "false", False)
    ]
    )
    tests.any_test_help.any_test_treeEvaluation_with_tree(Tree, "true")


def test_node_operator_negate1():
    """
        and
         |
         t
    """
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'and', False, [
        graph.oval_graph.OvalNode(2, 'value', "true", False)
    ]
    )
    tests.any_test_help.any_test_treeEvaluation_with_tree(Tree, "true")


def test_node_value_negate():
    """
        and
         |
         !f
    """
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'and', False, [
        graph.oval_graph.OvalNode(2, 'value', "false", True)
    ]
    )
    tests.any_test_help.any_test_treeEvaluation_with_tree(Tree, "true")


def test_node_value_negate1():
    """
        and
         |
         !t
    """
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'and', False, [
        graph.oval_graph.OvalNode(2, 'value', "true", True)
    ]
    )
    tests.any_test_help.any_test_treeEvaluation_with_tree(Tree, "false")
