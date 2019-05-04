import tree.operatorTree
import os
import pytest

def test_bad_tree():
    with pytest.raises(ValueError) as e:
        bad_tree()
    assert str(e.value) == 'err- true, false, error, unknown. noteval, notappl have not child!' 

    with pytest.raises(ValueError) as e:
        treeOnlyAnd()
    assert str(e.value) == 'err- OR, XOR, ONE, AND have child!' 

    with pytest.raises(ValueError) as e:
        treeOnlyOr()
    assert str(e.value) == 'err- OR, XOR, ONE, AND have child!' 

#degenered trees 
def bad_tree():
    """
         t
         |
        and
         |
         t
    """
    t = tree.operatorTree.operatorTree(1,"true",[tree.operatorTree.operatorTree(2,"and",[tree.operatorTree.operatorTree(3,"true")])])
    
def treeOnlyOr():
    """
        or
    """
    Tree = tree.operatorTree.operatorTree(1,'or')

def treeOnlyAnd():
    """
        and
    """
    Tree = tree.operatorTree.operatorTree(1,'and')

#normal trees
def test_treeAndFalse():
    """
        and
         |
         f
    """
    Tree = tree.operatorTree.operatorTree(1,'and', [
                 tree.operatorTree.operatorTree(2,"false")
                ]
        )
    
    dictOfTree={'node_id': 1,'value': 'and',
            'child': [
                {'node_id': 2,'value': "false", 'child': None }
            ]
        }

    any_test_treeEvaluation(Tree, "false")
    any_test_renderTree(Tree)
    any_test_treeTodictOfTree(Tree,dictOfTree)
    find_any_node(Tree,1)

def test_treeAllFalse():
    """
        and
        /|\
       f f or
          / \
         f   f
    """
    Tree = tree.operatorTree.operatorTree(1,'and', [
                 tree.operatorTree.operatorTree(2,"false"),
                 tree.operatorTree.operatorTree(3,"false"),
                 tree.operatorTree.operatorTree(4,'or', [
                             tree.operatorTree.operatorTree(5,"false"),
                             tree.operatorTree.operatorTree(6,"false")
                            ]
                     )
                ]
        )
    
    dictOfTree={'node_id': 1,'value': 'and',
            'child': [
                {'node_id': 2,'value': "false", 'child': None}, 
                {'node_id': 3,'value': "false", 'child': None}, 
                {'node_id': 4,'value': 'or', 'child': [
                                {'node_id': 5,'value': "false", 'child': None},
                                {'node_id': 6,'value': "false", 'child': None}
                            ]
                }
            ]
        }

    any_test_treeEvaluation(Tree, "false")
    any_test_renderTree(Tree)
    any_test_treeTodictOfTree(Tree,dictOfTree)
    find_any_node(Tree,5)

def test_treenode_ideal():
    """
        and
        /|\
       t t or
          / \
         f   t
    """
    Tree = tree.operatorTree.operatorTree(1,'and', [
                 tree.operatorTree.operatorTree(2,"true"),
                 tree.operatorTree.operatorTree(3,"false"),
                 tree.operatorTree.operatorTree(4,'or', [
                             tree.operatorTree.operatorTree(5,"false"),
                             tree.operatorTree.operatorTree(6,"true")
                            ]
                     )
                ]
        )
    
    dictOfTree={'node_id': 1,'value': 'and',
            'child': [
                {'node_id': 2,'value': "true", 'child': None}, 
                {'node_id': 3,'value': "false", 'child': None}, 
                {'node_id': 4,'value': 'or', 'child': [
                                {'node_id': 5,'value': "false", 'child': None},
                                {'node_id': 6,'value': "true", 'child': None}
                            ]
                }
            ]
        }

    any_test_treeEvaluation(Tree, "false")
    any_test_renderTree(Tree)
    any_test_treeTodictOfTree(Tree,dictOfTree)
    find_any_node(Tree,6)
###################################################

def any_test_treeTodictOfTree(tree,dictOfTree):
    assert tree.treeToDict() == dictOfTree

def find_any_node(Tree,node_id):
    findTree=tree.operatorTree.findNodeWithID(Tree, node_id)
    assert  findTree.node_id == node_id

def any_test_renderTree(tree,img =None):
    assert tree.renderTree(img)

def any_test_treeEvaluation(tree,expect):
    assert tree.evaluateTree() == expect

def test_dictToTree():
    """
        and
        /|\
       t t or
          / \
         f   t
    """
    Tree = tree.operatorTree.operatorTree(1,'and', [
                 tree.operatorTree.operatorTree(2,"true"),
                 tree.operatorTree.operatorTree(3,"false"),
                 tree.operatorTree.operatorTree(4,'or', [
                             tree.operatorTree.operatorTree(5,"false"),
                             tree.operatorTree.operatorTree(6,"true")
                            ]
                     )
                ]
        )

    dictOfTree={'node_id': 1,'value': 'and',
            'child': [
                {'node_id': 2,'value': "true", 'child': None}, 
                {'node_id': 3,'value': "false", 'child': None}, 
                {'node_id': 4,'value': 'or', 'child': [
                                {'node_id': 5,'value': "false", 'child': None},
                                {'node_id': 6,'value': "true", 'child': None}
                            ]
                }
            ]
        }

    treedictOfTree = tree.operatorTree.dictToTree(dictOfTree)
    #Je to ok?
    assert treedictOfTree.treeToDict() == dictOfTree

def test_treeRepr():
    """
        and
         |
         f
    """
    Tree = tree.operatorTree.operatorTree(1,'and', [
                 tree.operatorTree.operatorTree(2,"false")
                ]
        )
    assert str(Tree) == "and"


def test_addToTree():
    """
        and
         |
         f
    """

    dictOfTree={'node_id': 1,'value': 'and',
            'child': [
                {'node_id': 2,'value': "false", 'child': None}, 
                {'node_id': 3,'value': "true", 'child': None}, 
            ]
        }

    Tree = tree.operatorTree.operatorTree(1,'and', [
                 tree.operatorTree.operatorTree(2,"false")
                ]
        )
    Tree1=tree.operatorTree.operatorTree(3,"true")
    tree.operatorTree.addToTree(Tree,1,Tree1)
    assert Tree.treeToDict()==dictOfTree    

def test_ChangeValueTree():
    """
        and
        /|\
       t t or
          / \
         f   t
    """
    Tree = tree.operatorTree.operatorTree(1,'and', [
                 tree.operatorTree.operatorTree(2,"true"),
                 tree.operatorTree.operatorTree(3,"false"),
                 tree.operatorTree.operatorTree(4,'or', [
                             tree.operatorTree.operatorTree(5,"false"),
                             tree.operatorTree.operatorTree(6,"true")
                            ]
                     )
                ]
        )
    
    tree.operatorTree.ChangeTreeValue(Tree,3,"true")
    any_test_treeEvaluation(Tree, "true")
