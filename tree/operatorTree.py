import operator

class operatorTree(object):
    def __init__(self,node_id, value='root', children=None):
        self.node_id=node_id
        self.value = value
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)
        else:
            if self.value == "or" or self.value=="and":
                raise ValueError('err- OR or AND have child!')
    
    def __repr__(self):
        return self.value

    def add_child(self, node):
        if self.value == "or" or self.value=="and":
            assert isinstance(node,operatorTree)
            self.children.append(node)
        else:
            self.children = None
            raise ValueError("err- True or False have not child!")

    def evaluateTree(self):
        operators = {
            "or": any,
            "and": all,
        }
        evaluator = operators[self.value]
        return evaluator(i.evaluateTree() if type(i.value) is not bool else i.value for i in self.children)

    def treeToDict(self):
        if not self.children:
            return {'node_id': self.node_id,'value': self.value,'child': None }
        else:
            return {'node_id': self.node_id,'value': self.value,'child': [i.treeToDict() for i in self.children] }    
        
    def renderTree(self, img = None):
        #str(self.name)+"\n\t"+ [str(item.renderTree)+"\n\t" for item in self.children]
        #text="{}\n\t".format(self.name) + item.renderTree for item in self.children
        return True

def dictToTree(dictOfTree):
    if dictOfTree["child"] is None :
        return operatorTree(dictOfTree["node_id"], dictOfTree["value"])
    else:
        return operatorTree(dictOfTree["node_id"], dictOfTree["value"], [ dictToTree(i) for i in dictOfTree["child"]])

def findNodeWithID(tree, node_id):
    if tree.node_id == node_id:
        return tree
    else:
        for child in tree.children:
            if child.node_id == node_id:
                return child
        for child in tree.children:
            if child.children != []:
               return findNodeWithID(child,node_id)

def addToTree(tree,node_id,newNode):
    findNodeWithID(tree, node_id).add_child(newNode)

def ChangeTreeValue(tree,node_id,value):
    findNodeWithID(tree, node_id).value = value