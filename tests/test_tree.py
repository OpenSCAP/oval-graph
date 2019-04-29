import tree.operatorTree
import os
import pytest

def test_bad_tree():
    with pytest.raises(ValueError) as e:
        bad_tree()
    assert str(e.value) == 'err- True or False have not child!' 

    with pytest.raises(ValueError) as e:
        treeOnlyAnd()
    assert str(e.value) == 'err- OR or AND have child!' 

    with pytest.raises(ValueError) as e:
        treeOnlyOr()
    assert str(e.value) == 'err- OR or AND have child!' 

#degenered trees 
def bad_tree():
    """
         t
         |
        and
         |
         t
    """
    t = tree.operatorTree.operatorTree(1,True,[tree.operatorTree.operatorTree(2,"and",[tree.operatorTree.operatorTree(3,True)])])
    
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
                 tree.operatorTree.operatorTree(2,False)
                ]
        )
    
    dict={'id': 1,'name': 'and',
            'child': [
                {'id': 2,'name': False, 'child': None }
            ]
        }

    any_test_treeEvaluation(Tree, False)
    any_test_renderTree(Tree)
    any_test_treeToDict(Tree,dict)
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
                 tree.operatorTree.operatorTree(2,False),
                 tree.operatorTree.operatorTree(3,False),
                 tree.operatorTree.operatorTree(4,'or', [
                             tree.operatorTree.operatorTree(5,False),
                             tree.operatorTree.operatorTree(6,False)
                            ]
                     )
                ]
        )
    
    dict={'id': 1,'name': 'and',
            'child': [
                {'id': 2,'name': False, 'child': None}, 
                {'id': 3,'name': False, 'child': None}, 
                {'id': 4,'name': 'or', 'child': [
                                {'id': 5,'name': False, 'child': None},
                                {'id': 6,'name': False, 'child': None}
                            ]
                }
            ]
        }

    any_test_treeEvaluation(Tree, False)
    any_test_renderTree(Tree)
    any_test_treeToDict(Tree,dict)
    find_any_node(Tree,5)

def test_treeIdeal():
    """
        and
        /|\
       t t or
          / \
         f   t
    """
    Tree = tree.operatorTree.operatorTree(1,'and', [
                 tree.operatorTree.operatorTree(2,True),
                 tree.operatorTree.operatorTree(3,False),
                 tree.operatorTree.operatorTree(4,'or', [
                             tree.operatorTree.operatorTree(5,False),
                             tree.operatorTree.operatorTree(6,True)
                            ]
                     )
                ]
        )
    
    dict={'id': 1,'name': 'and',
            'child': [
                {'id': 2,'name': True, 'child': None}, 
                {'id': 3,'name': False, 'child': None}, 
                {'id': 4,'name': 'or', 'child': [
                                {'id': 5,'name': False, 'child': None},
                                {'id': 6,'name': True, 'child': None}
                            ]
                }
            ]
        }

    any_test_treeEvaluation(Tree, False)
    any_test_renderTree(Tree)
    any_test_treeToDict(Tree,dict)
    find_any_node(Tree,6)
###################################################

def any_test_treeToDict(tree,dict):
    assert tree.treeToDict() == dict

def find_any_node(Tree,id):
    findTree=tree.operatorTree.findNodeWithID(Tree, id)
    assert  findTree.id == id

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
                 tree.operatorTree.operatorTree(2,True),
                 tree.operatorTree.operatorTree(3,False),
                 tree.operatorTree.operatorTree(4,'or', [
                             tree.operatorTree.operatorTree(5,False),
                             tree.operatorTree.operatorTree(6,True)
                            ]
                     )
                ]
        )

    dict={'id': 1,'name': 'and',
            'child': [
                {'id': 2,'name': True, 'child': None}, 
                {'id': 3,'name': False, 'child': None}, 
                {'id': 4,'name': 'or', 'child': [
                                {'id': 5,'name': False, 'child': None},
                                {'id': 6,'name': True, 'child': None}
                            ]
                }
            ]
        }

    treeDict = tree.operatorTree.dictToTree(dict)
    #Je to ok?
    assert treeDict.treeToDict() == dict

def test_treeRepr():
    """
        and
         |
         f
    """
    Tree = tree.operatorTree.operatorTree(1,'and', [
                 tree.operatorTree.operatorTree(2,False)
                ]
        )
    assert str(Tree) == "and"


def test_addToTree():
    """
        and
         |
         f
    """

    dict={'id': 1,'name': 'and',
            'child': [
                {'id': 2,'name': False, 'child': None}, 
                {'id': 3,'name': True, 'child': None}, 
            ]
        }

    Tree = tree.operatorTree.operatorTree(1,'and', [
                 tree.operatorTree.operatorTree(2,False)
                ]
        )
    Tree1=tree.operatorTree.operatorTree(3,True)
    tree.operatorTree.addToTree(Tree,1,Tree1)
    assert Tree.treeToDict()==dict    

def test_ChangeValueTree():
    """
        and
        /|\
       t t or
          / \
         f   t
    """
    Tree = tree.operatorTree.operatorTree(1,'and', [
                 tree.operatorTree.operatorTree(2,True),
                 tree.operatorTree.operatorTree(3,False),
                 tree.operatorTree.operatorTree(4,'or', [
                             tree.operatorTree.operatorTree(5,False),
                             tree.operatorTree.operatorTree(6,True)
                            ]
                     )
                ]
        )
    
    tree.operatorTree.ChangeTreeValue(Tree,3,True)
    any_test_treeEvaluation(Tree, True)
    


