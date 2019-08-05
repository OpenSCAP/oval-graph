import graph.oval_graph
import pytest
import tests.any_test_help


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

    test_data_src = 'test_data/bigOvalTree.json'
    dict_of_tree = tests.any_test_help.any_get_test_data_json(test_data_src)
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

    test_data_src = 'test_data/add_to_tree.json'
    dict_of_tree = tests.any_test_help.any_get_test_data_json(test_data_src)

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
