import operator

class operatorTree(object):
    def __init__(self, name='root', children=None):
        self.name = name
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)
    
    def __repr__(self):
        return self.name

    def add_child(self, node):
        if self.name == "or" or self.name=="and":
            assert isinstance(node,operatorTree)
            self.children.append(node)
        else:
            print("err- True or False have not child!")

    def evaluateTree(self):
        operator = self.name
        tests = self.children
        operators = {
            "or": any,
            "and": all,
        }
        evaluator = operators[operator]
        return evaluator(i.evaluateTree() if type(i.name) is not bool else i.name for i in tests)

    def treeToDict(self):
        return {'name': self.name,'child': [i.treeToDict() for i in self.children]}

    def renderTree(self, img = None):
        #str(self.name)+"\n\t"+ [str(item.renderTree)+"\n\t" for item in self.children]
        #text="{}\n\t".format(self.name) + item.renderTree for item in self.children
        return True


def dictToTree(dict):
    pass