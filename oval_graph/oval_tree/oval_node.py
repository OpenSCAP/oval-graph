from collections import Counter

from .oval_result import OvalResult

ALLOWED_VALUES = ("true", "false", "error", "unknown", "noteval", "notappl")
ALLOWED_OPERATORS = ("or", "and", "one", "xor")
EMPTY_RESULT = {
    "number_of_true": 0,
    "number_of_false": 0,
    "number_of_error": 0,
    "number_of_unknown": 0,
    "number_of_noteval": 0,
    "number_of_notappl": 0
}


class OvalNode():
    """The Oval Node object is one node of the OVAL tree.
       The graphic representation of the OVAL tree is the OVAL graph.

    Attributes:
        node_id (str): id of node
        node_type (str): type node
        value (str): value of node for operator and, or, one etc... and for value true,
        false, error etc...
        negation (bool): value indicating whether the node is negated
        comment (str): some comment about node
        tag (str): tag specifies if the node represents OVAL test,
        OVAL definition or XCCDF rule
        test_result_details (dict|None): information about test
        children ([OvalNode]): children of node
    """

    def __init__(self, node_id, node_type, value, **kwargs):
        """This metode construct OvalNode and validate values of parameteres.

        Required args:
            node_id (str|int): identifies node
            node_type (str): type of node (value or operator)
            value (str): value of node

        Optional args:
            negation (bool): value indicating whether the node is negated (empty eq False)
            comment (str): text about node (empty eq None)
            tag (str): tag specifies if the node represents OVAL test,
            OVAL definition or XCCDF rule (empty eq None)
            test_result_details (dict|None): information about test (empty eq None)
            children ([OvalNode]): array of children of node (empty eq empty array)

        Raises:
            TypeError, ValueError
        """
        self.node_id = node_id
        self.node_type = self._validate_type(node_type)
        self.value = self._validate_value(self.node_type, value)

        self._check_missing_children_for_operator(
            kwargs.get('children', None))
        self.negation = self._validate_negation(
            kwargs.get('negation', False))

        self.comment = kwargs.get('comment', None)
        self.tag = kwargs.get('tag', None)
        self.test_result_details = kwargs.get('test_result_details', None)

        input_children = kwargs.get('children', None)
        self.children = []
        if input_children:
            for child in input_children:
                self.add_child(child)

    @staticmethod
    def _validate_negation(input_negation):
        if not isinstance(input_negation, bool):
            raise TypeError("Wrong value of negation argument!")
        return input_negation

    @staticmethod
    def _validate_type(input_node_type):
        node_type = input_node_type.lower()
        if node_type not in ("value", "operator"):
            raise TypeError("Wrong value of node_type argument!")
        return node_type

    @staticmethod
    def _validate_value(input_node_type, input_value):
        value = input_value.lower()

        if input_node_type == "value" and value not in ALLOWED_VALUES:
            raise TypeError(
                "Wrong value of argument value for value node!")

        if input_node_type == "operator" and value not in ALLOWED_OPERATORS:
            raise TypeError(
                "Wrong value of argument value for operator node!")

        return value

    def _check_missing_children_for_operator(self, children):
        if children is None and self.node_type == "operator":
            raise ValueError(
                "The operator node must have a child!")

    def __repr__(self):
        return self.value

    def add_child(self, node):
        if self.node_type == "operator":
            assert isinstance(node, OvalNode)
            self.children.append(node)
            return
        raise ValueError(
            "The value node cannot contain any child!")

    def _get_result_counts(self):
        result = Counter(EMPTY_RESULT)
        for child in self.children:
            if child.value == "true" and not child.negation:
                result["number_of_true"] += 1
            elif child.value == "true" and child.negation:
                result["number_of_false"] += 1
            elif child.value == "false" and not child.negation:
                result["number_of_false"] += 1
            elif child.value == "false" and child.negation:
                result["number_of_true"] += 1
            else:
                if child.node_type == "operator":
                    result["number_of_" + child.evaluate_tree()] += 1
                else:
                    result["number_of_" + child.value] += 1
        return result

    def evaluate_tree(self):
        results_counts = self._get_result_counts()
        oval_result = OvalResult(**results_counts)
        out_result = None
        if oval_result.is_notapp_result():
            out_result = "notappl"
        else:
            if self.value == "or":
                out_result = oval_result.eval_operator_or()
            elif self.value == "and":
                out_result = oval_result.eval_operator_and()
            elif self.value == "one":
                out_result = oval_result.eval_operator_one()
            elif self.value == "xor":
                out_result = oval_result.eval_operator_xor()

        if out_result == "true" and self.negation:
            out_result = "false"
        elif out_result == "false" and self.negation:
            out_result = "true"

        return out_result

    def find_node_with_id(self, node_id):
        if self.node_id == node_id:
            return self
        for child in self.children:
            tmp_node = child.find_node_with_id(node_id)
            if tmp_node is not None:
                return tmp_node
        return None

    def add_child_to_node(self, node_id, new_node):
        node = self.find_node_with_id(node_id)
        if node is not None:
            node.add_child(new_node)
            return True
        return False

    def change_value_of_node(self, node_id, value):
        node = self.find_node_with_id(node_id)
        if node is not None:
            self._validate_value(node.node_type, value)
            node.value = value
            return True
        return False
