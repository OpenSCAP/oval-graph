import pytest

from oval_graph.oval_node import OvalNode

import tests.any_test_help

missing_error_pattern = "Missing required argument!"

bad_value_error_pattern = (
    r'Wrong value of (negation|node_type|argument) (argument|value)(!| for (value|operator) node!)'
    )


def test_bad_tree():
    with pytest.raises(Exception, match="cannot contain any child"):
        assert bad_tree()


def test_bad_tree_only_and_no_child():
    with pytest.raises(Exception, match="must have a child"):
        assert tree_only_and()


def test_bad_tree_only_or_no_child():
    with pytest.raises(Exception, match="must have a child"):
        assert tree_only_or()


def test_bad_tree_with_bad_type_of_node():
    with pytest.raises(Exception, match=bad_value_error_pattern):
        assert tree_with_bad_type()


def test_bad_tree_with_bad_value_of_operator():
    with pytest.raises(Exception, match=bad_value_error_pattern):
        assert tree_with_bad_value_of_operator()


def test_bad_tree_with_bad_value_of_value():
    with pytest.raises(Exception, match=bad_value_error_pattern):
        assert tree_with_bad_value_of_value()


def test_bad_tree_with_bad_value_of_negation():
    with pytest.raises(Exception, match=bad_value_error_pattern):
        assert tree_with_bad_value_of_negation()


def test_bad_tree_with_miss_id_argument():
    with pytest.raises(Exception, match=missing_error_pattern):
        assert miss_id_argument()


def test_bad_tree_with_miss_value_argument():
    with pytest.raises(Exception, match=missing_error_pattern):
        assert miss_value_argument()


# degenered trees


def miss_id_argument():
    tree = OvalNode(
        node_type='operator',
        value='and',
        children=[
            OvalNode(
                node_id=2,
                node_type='value',
                value="false",
            ),
        ]
    )
    return


def miss_value_argument():
    tree = OvalNode(
        node_id=1,
        node_type='operator',
        children=[
            OvalNode(
                node_id=2,
                node_type='value',
                value="false",
            ),
        ]
    )
    return


def bad_tree():
    """
         t
         |
        and
         |
         t
    """
    t = OvalNode(
        node_id=1,
        node_type="value",
        value="true",
        children=[
            OvalNode(
                node_id=2,
                node_type="operator",
                value="and",
                children=[
                    OvalNode(
                        node_id=3,
                        node_type="value",
                        value="true",
                    ),
                ]
            ),
        ]
    )
    return


def tree_only_or():
    """
        or
    """
    tree = OvalNode(
        node_id=1,
        node_type="operator",
        value='or',
    )
    return


def tree_only_and():
    """
        and
    """
    tree = OvalNode(
        node_id=1,
        node_type="operator",
        value='and',
    )
    return


def tree_with_bad_value_of_operator():
    tree = OvalNode(
        node_id=1,
        node_type="operator",
        value='nad',
    )
    return


def tree_with_bad_value_of_value():
    tree = OvalNode(
        node_id=1,
        node_type="value",
        value='and',
    )
    return


def tree_with_bad_type():
    tree = OvalNode(
        node_id=1,
        node_type="car",
        value='and',
    )
    return


def tree_with_bad_value_of_negation():
    tree = OvalNode(
        node_id=1,
        node_type="operator",
        value="true",
        children=[
            OvalNode(
                node_id=2,
                node_type="value",
                value='true',
                negation="random_string",
            )
        ]
    )
    return

# normal trees


def test_UPPERCASETree():
    t = OvalNode(
        node_id=1,
        node_type="OPERATOR",
        value="AND",
        children=[
            OvalNode(
                node_id=2,
                node_type="VALUE",
                value="TRUE",
            ),
            OvalNode(
                node_id=3,
                node_type="VALUE",
                value="NOTAPPL",
            ),
        ]
    )
    return


def test_bigOvalTree():
    tree = OvalNode(
        node_id=1,
        node_type='operator',
        value='and',
        children=[
            OvalNode(
                node_id=2,
                node_type='value',
                value="false",
            ),
            OvalNode(
                node_id=3,
                node_type='operator',
                value="xor",
                children=[
                    OvalNode(
                        node_id=4,
                        node_type='value',
                        value='true',
                    ),
                    OvalNode(
                        node_id=5,
                        node_type='operator',
                        value='one',
                        children=[
                            OvalNode(
                                node_id=6,
                                node_type='value',
                                value='noteval',
                            ),
                            OvalNode(
                                node_id=7,
                                node_type='value',
                                value='true',
                            ),
                            OvalNode(
                                node_id=8,
                                node_type='value',
                                value='notappl',
                            ),
                        ]
                    ),
                    OvalNode(
                        node_id=9,
                        node_type='value',
                        value='error',
                    ),
                ]
            ),
            OvalNode(
                node_id=10,
                node_type='operator',
                value='or',
                children=[
                    OvalNode(
                        node_id=11,
                        node_type='value',
                        value="unknown",
                    ),
                    OvalNode(
                        node_id=12,
                        node_type='value',
                        value="true",
                    ),
                ]
            ),
        ]
    )

    test_data_src = 'test_data/bigOvalTree.json'
    dict_of_tree = tests.any_test_help.any_get_test_data_json(test_data_src)
    tests.any_test_help.any_test_treeEvaluation_with_tree(tree, "false")
    tests.any_test_help.any_test_tree_to_dict_of_tree(tree, dict_of_tree)
    tests.any_test_help.find_any_node(tree, 5)
    tests.any_test_help.any_test_dict_to_tree(dict_of_tree)

###################################################


def get_and_false_tree():
    """
        and
         |
         f
    """
    return OvalNode(
        node_id=1,
        node_type='operator',
        value='and',
        children=[
            OvalNode(
                node_id=2,
                node_type='value',
                value="false",
            ),
        ]
    )


def test_treeRepr():
    assert str(get_and_false_tree()) == "and"


def test_add_to_tree():
    test_data_src = 'test_data/add_to_tree.json'
    dict_of_tree = tests.any_test_help.any_get_test_data_json(test_data_src)

    tree = get_and_false_tree()
    tree1 = OvalNode(
        node_id=3,
        node_type='value',
        value="true",
    )
    tree.add_to_tree(1, tree1)
    assert tree.save_tree_to_dict() == dict_of_tree


def test_ChangeValueTree():
    """
        and
        /|\
       t t or
          / \
         f   t
    """
    Tree = OvalNode(
        node_id=1,
        node_type='operator',
        value='and',
        children=[
            OvalNode(
                node_id=2,
                node_type='value',
                value="true",
            ),
            OvalNode(
                node_id=3,
                node_type='value',
                value="false",
            ),
            OvalNode(
                node_id=4,
                node_type='operator',
                value='or',
                children=[
                    OvalNode(
                        node_id=5,
                        node_type='value',
                        value="false",
                    ),
                    OvalNode(
                        node_id=6,
                        node_type='value',
                        value="true",
                    ),
                ]
            ),
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
    tree = OvalNode(
        node_id=1,
        node_type='operator',
        value='and',
        negation=True,
        children=[
            OvalNode(
                node_id=2,
                node_type='value',
                value="false",
            ),
        ]
    )
    tests.any_test_help.any_test_treeEvaluation_with_tree(tree, "true")


def test_node_value_negate():
    """
        and
         |
         !f
    """
    tree = OvalNode(
        node_id=1,
        node_type='operator',
        value='and',
        children=[
            OvalNode(
                node_id=2,
                node_type='value',
                value="false",
                negation=True,
            ),
        ]
    )
    tests.any_test_help.any_test_treeEvaluation_with_tree(tree, "true")


def test_node_value_negate1():
    """
        and
         |
         !t
    """

    tree = OvalNode(
        node_id=1,
        node_type='operator',
        value='and',
        children=[
            OvalNode(
                node_id=2,
                node_type='value',
                value="true",
                negation=True,
            ),
        ]
    )
    tests.any_test_help.any_test_treeEvaluation_with_tree(tree, "false")
