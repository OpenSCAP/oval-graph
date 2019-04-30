import operator

class operatorTree(object):
    def __init__(self,id, value='root', children=None):
        self.id=id
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
            return {'id': self.id,'value': self.value,'child': None }
        else:
            return {'id': self.id,'value': self.value,'child': [i.treeToDict() for i in self.children] }    
        
    def renderTree(self, img = None):
        #str(self.name)+"\n\t"+ [str(item.renderTree)+"\n\t" for item in self.children]
        #text="{}\n\t".format(self.name) + item.renderTree for item in self.children
        return True

def dictToTree(dict):
    if dict["child"] is None :
        return operatorTree(dict["id"], dict["value"])
    else:
        return operatorTree(dict["id"], dict["value"], [ dictToTree(i) for i in dict["child"]])

def findNodeWithID(tree, id):
    if tree.id == id:
        return tree
    else:
        for i in tree.children:
            if i.id == id:
                return i
        for i in tree.children:
            if i.children != []:
               return findNodeWithID(i,id)

def addToTree(tree,id,newNode):
    findNodeWithID(tree, id).add_child(newNode)

def ChangeTreeValue(tree,id,value):
    findNodeWithID(tree, id).value = value