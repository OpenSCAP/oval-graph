import pytest

from oval_graph.oval_tree.builder import Builder
from oval_graph.oval_tree.converter import Converter
from oval_graph.oval_tree.oval_node import OvalNode

from .get_tree import GetTree

BAD_VALUE_ERROR_PATTERN = (
    r'Wrong value of (negation|node_type|argument) (argument|value)(!| for (value|operator) node!)'
)


@pytest.mark.parametrize("get_tree, pattern", [
    (GetTree.bad_tree, "cannot contain any child"),
    (GetTree.tree_only_and, "must have a child"),
    (GetTree.tree_only_or, "must have a child"),
    (GetTree.tree_with_bad_type, BAD_VALUE_ERROR_PATTERN),
    (GetTree.tree_with_bad_value_of_operator, BAD_VALUE_ERROR_PATTERN),
    (GetTree.tree_with_bad_value_of_value, BAD_VALUE_ERROR_PATTERN),
    (GetTree.tree_with_bad_value_of_negation, BAD_VALUE_ERROR_PATTERN),
])
def test_bad_tree(get_tree, pattern):
    with pytest.raises(Exception, match=pattern):
        assert get_tree()


# normal trees


def test_uppercase_tree():
    tree = GetTree.uppercase_tree()
    assert tree.find_node_with_id(3).value == 'notappl'


def test_eval_big_tree():
    assert GetTree.big_oval_tree().evaluate_tree() == 'false'


@pytest.mark.parametrize("node_id", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
def test_find_node_with_id(node_id):
    assert GetTree.big_oval_tree().find_node_with_id(node_id).node_id == node_id


@pytest.mark.parametrize("node_id", [0, 111, 212, 432, 342, -1])
def test_bad_find_node_with_id(node_id):
    assert GetTree.big_oval_tree().find_node_with_id(node_id) is None


def test_build_and_convert_json_tree():
    test_data_src = 'test_data/bigOvalTree.json'
    dict_of_tree = GetTree.json_of_tree(test_data_src)
    treedict_of_tree = Builder.dict_to_oval_tree(dict_of_tree)
    assert Converter(treedict_of_tree).to_dict() == dict_of_tree


def test_tree_repr():
    assert str(GetTree.tree_false()) == "and"


def test_add_to_tree():
    test_data_src = 'test_data/add_to_tree.json'
    dict_of_tree = GetTree.json_of_tree(test_data_src)

    tree = GetTree.tree_false()
    tree_node = OvalNode(
        node_id=3,
        node_type='value',
        value="true",
    )
    tree.add_child_to_node(1, tree_node)
    assert Converter(tree).to_dict() == dict_of_tree


@pytest.mark.parametrize("node_id, new_value, expect_evaluation", [
    (2, "true", "false"),
    (2, "false", "false"),
    (2, "error", "false"),
    (2, "noteval", "false"),
    (2, "notappl", "false"),
    (3, "true", "true"),
    (3, "false", "false"),
    (3, "error", "error"),
    (3, "noteval", "noteval"),
    (3, "notappl", "true"),
    (5, "true", "false"),
    (5, "false", "false"),
    (5, "error", "false"),
    (5, "noteval", "false"),
    (5, "notappl", "false"),
    (6, "true", "false"),
    (6, "false", "false"),
    (6, "error", "false"),
    (6, "noteval", "false"),
    (6, "notappl", "false"),
])
def test_change_value_tree(node_id, new_value, expect_evaluation):
    """ Created tree
        and
        /|\
       t f or
          / \
         f   t
    """
    tree = GetTree.simple_tree()
    assert tree.evaluate_tree() == "false"
    assert tree.change_value_of_node(node_id, new_value) is not None
    assert tree.evaluate_tree() == expect_evaluation


def test_node_operator_negate_node_false():
    """
        !and
         |
         f
    """
    tree = GetTree.negated_operator_node_false()
    assert tree.evaluate_tree() == "true"


def test_node_operator_negate_node_true():
    """
        !and
         |
         t
    """
    tree = GetTree.negated_operator_node_true()
    assert tree.evaluate_tree() == "false"


def test_node_value_negate_node_false():
    """
        and
         |
         !f
    """
    tree = GetTree.negate_value_node_false()
    assert tree.evaluate_tree() == "true"


def test_node_value_negate_node_true():
    """
        and
         |
         !t
    """
    tree = GetTree.negate_value_node_true()
    assert tree.evaluate_tree() == "false"
