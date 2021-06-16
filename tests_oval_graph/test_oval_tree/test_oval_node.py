import json
import os

import pytest

from oval_graph.oval_tree.builder import Builder
from oval_graph.oval_tree.converter import Converter
from oval_graph.oval_tree.oval_node import OvalNode

BAD_VALUE_ERROR_PATTERN = (
    r'Wrong value of (negation|node_type|argument) (argument|value)(!| for (value|operator) node!)'
)

# Degenered trees


def get_bad_tree():
    """
         t
         |
        and
         |
         t
    """
    return OvalNode(
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


def get_tree_only_or():
    """
        or
    """
    return OvalNode(
        node_id=1,
        node_type="operator",
        value='or',
    )


def get_tree_only_and():
    """
        and
    """
    return OvalNode(
        node_id=1,
        node_type="operator",
        value='and',
    )


def get_tree_with_bad_value_of_operator():
    return OvalNode(
        node_id=1,
        node_type="operator",
        value='nad',
    )


def get_tree_with_bad_value_of_value():
    return OvalNode(
        node_id=1,
        node_type="value",
        value='and',
    )


def get_tree_with_bad_type():
    return OvalNode(
        node_id=1,
        node_type="car",
        value='and',
    )


def get_tree_with_bad_value_of_negation():
    return OvalNode(
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


@pytest.mark.parametrize("get_tree, pattern", [
    (get_bad_tree, "cannot contain any child"),
    (get_tree_only_and, "must have a child"),
    (get_tree_only_or, "must have a child"),
    (get_tree_with_bad_type, BAD_VALUE_ERROR_PATTERN),
    (get_tree_with_bad_value_of_operator, BAD_VALUE_ERROR_PATTERN),
    (get_tree_with_bad_value_of_value, BAD_VALUE_ERROR_PATTERN),
    (get_tree_with_bad_value_of_negation, BAD_VALUE_ERROR_PATTERN),
])
def test_bad_tree(get_tree, pattern):
    with pytest.raises(Exception, match=pattern):
        assert get_tree()


# normal trees


def test_uppercase_tree():
    OvalNode(
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


def get_big_oval_tree():
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


def test_eval_big_tree():
    assert get_big_oval_tree().evaluate_tree() == 'false'


# fix 11, 12 ids
@pytest.mark.parametrize("node_id", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
def test_find_node_with_id(node_id):
    assert get_big_oval_tree().find_node_with_id(node_id).node_id == node_id


@pytest.mark.parametrize("node_id", [0, 111, 212, 432, 342, -1])
def test_bad_find_node_with_id(node_id):
    assert get_big_oval_tree().find_node_with_id(node_id) is None


def test_build_and_convert_json_tree():
    test_data_src = 'test_data/bigOvalTree.json'
    dict_of_tree = get_test_data_json(test_data_src)
    treedict_of_tree = Builder.dict_to_oval_tree(dict_of_tree)
    assert Converter(treedict_of_tree).to_dict() == dict_of_tree


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


def test_tree_repr():
    assert str(get_and_false_tree()) == "and"


def get_test_data_json(src):
    top_patch = os.path.dirname(os.path.realpath(__file__))
    patch = os.path.join(top_patch, src)
    with open(patch, 'r') as file_:
        return json.load(file_)


def test_add_to_tree():
    test_data_src = 'test_data/add_to_tree.json'
    dict_of_tree = get_test_data_json(test_data_src)

    tree = get_and_false_tree()
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
    tree = OvalNode(
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
    assert tree.evaluate_tree() == "false"
    assert tree.change_value_of_node(node_id, new_value) is not None
    assert tree.evaluate_tree() == expect_evaluation


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
    assert tree.evaluate_tree() == "true"


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
    assert tree.evaluate_tree() == "true"


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
    assert tree.evaluate_tree() == "false"
