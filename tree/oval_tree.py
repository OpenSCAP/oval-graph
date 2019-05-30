from lxml import etree as ET

'''
This module contains methods and classes for
constructing and controlling an oval tree.
'''


class OvalNode(object):
    '''
    The OvalNode object is one node of oval tree.

    Args:
        node_id (str|int): identifies node
        input_node_type (str): type of node (value or operator)
        input_value (str): value of node
        children ([OvalNode]): array of children of node

    Attributes:
        node_id (str): id of node
        node_type (str): type node
        value (str): value of node for operator and,
        or, one etc... and for value true, false, error etc...
        children ([OvalNode]): children of node
    '''

    def __init__(self, node_id, input_node_type, input_value, children=None):
        self.node_id = node_id
        value = input_value.lower()
        node_type = input_node_type.lower()
        if node_type == "value" or node_type == "operator":
            self.node_type = node_type
        else:
            raise ValueError("err- unknown type")
        allowed_operators = [
            "or",
            "and",
            "one",
            "xor"]
        allowed_values = [
            "true",
            "false",
            "error",
            "unknown",
            "noteval",
            "notappl"]
        if self.node_type == "value":
            if value in allowed_values:
                self.value = value
            else:
                raise ValueError("err- unknown value")
        if self.node_type == "operator":
            if value in allowed_operators:
                self.value = value
            else:
                raise ValueError("err- unknown operator")
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)
        else:
            if self.node_type == "operator":
                raise ValueError('err- OR, XOR, ONE, AND have child!')

    def __repr__(self):
        return self.value

    def add_child(self, node):
        if self.node_type == "operator":
            assert isinstance(node, OvalNode)
            self.children.append(node)
        else:
            self.children = None
            raise ValueError(
                "err- true, false, error, unknown. noteval, notappl have not child!")

    def evaluate_tree(self):
        result = {
            'true_cnt': 0,
            'false_cnt': 0,
            'error_cnt': 0,
            'unknown_cnt': 0,
            'noteval_cnt': 0,
            'notappl_cnt': 0
        }

        for child in self.children:
            if child.value == 'true':
                result['true_cnt'] += 1
            elif child.value == 'false':
                result['false_cnt'] += 1
            elif child.value == 'error':
                result['error_cnt'] += 1
            elif child.value == 'unknown':
                result['unknown_cnt'] += 1
            elif child.value == 'noteval':
                result['noteval_cnt'] += 1
            elif child.value == 'notappl':
                result['notappl_cnt'] += 1
            else:
                if self.node_type == "operator":
                    result[child.evaluate_tree() + "_cnt"] += 1

        if result['notappl_cnt'] > 0\
                and self._noteval_eq_zero(result)\
                and self._false_eq_zero(result)\
                and self._error_eq_zero(result)\
                and self._unknown_eq_zero(result)\
                and self._true_eq_zero(result):
            return "notappl"
        else:
            if self.value == "or":
                return self._oval_operator_or(result)
            elif self.value == "and":
                return self._oval_operator_and(result)
            elif self.value == "one":
                return self._oval_operator_one(result)
            elif self.value == "xor":
                return self._oval_operator_xor(result)

    def tree_to_dict(self):
        if not self.children:
            return {
                'node_id': self.node_id,
                'type': self.node_type,
                'value': self.value,
                'child': None
            }
        return {
            'node_id': self.node_id,
            'type': self.node_type,
            'value': self.value,
            'child': [child.tree_to_dict() for child in self.children]
        }

    def find_node_with_ID(self, node_id):
        if self.node_id == node_id:
            return self
        else:
            for child in self.children:
                if child.node_id == node_id:
                    return child
            for child in self.children:
                if child.children != []:
                    return child.find_node_with_ID(node_id)

    def add_to_tree(self, node_id, newNode):
        self.find_node_with_ID(node_id).add_child(newNode)

    def change_tree_value(self, node_id, value):
        self.find_node_with_ID(node_id).value = value

    # ----Function for evaluation----

    def _oval_operator_and(self, result):
        out_result = None
        if self._false_eq_zero(result)\
                and self._true_greater_zero(result)\
                and self._error_unknown_noteval_eq_zero(result):
            out_result = 'true'
        elif self._false_greater_zero(result):
            out_result = 'false'
        elif self._false_eq_zero(result)\
                and self._error_greater_zero(result):
            out_result = 'error'
        elif self._false_eq_zero(result)\
                and self._error_unknown_eq_zero(result):
            out_result = 'unknown'
        elif self._false_eq_zero(result)\
                and self._error_unknown_eq_noteval_greater_zero(result):
            out_result = 'noteval'
        else:
            out_result = None
        return out_result

    def _oval_operator_one(self, result):
        out_result = None
        if result['true_cnt'] == 1\
                and result['false_cnt'] >= 0\
                and self._error_eq_zero(result)\
                and self._unknown_eq_zero(result)\
                and self._noteval_eq_zero(result)\
                and result['notappl_cnt'] >= 0:
            out_result = 'true'
        elif result['true_cnt'] >= 2\
                and result['false_cnt'] >= 0\
                and result['error_cnt'] >= 0\
                and result['unknown_cnt'] >= 0\
                and result['noteval_cnt'] >= 0\
                and result['notappl_cnt'] >= 0:
            out_result = 'false'
        elif self._true_eq_zero(result)\
                and result['false_cnt'] >= 0\
                and self._error_eq_zero(result)\
                and self._unknown_eq_zero(result)\
                and self._noteval_eq_zero(result)\
                and result['notappl_cnt'] >= 0:
            out_result = 'false'
        elif result['true_cnt'] < 2\
                and result['false_cnt'] >= 0\
                and self._error_greater_zero(result)\
                and result['unknown_cnt'] >= 0\
                and result['noteval_cnt'] >= 0\
                and result['notappl_cnt'] >= 0:
            out_result = 'error'
        elif result['true_cnt'] < 2\
                and result['false_cnt'] >= 0\
                and self._error_eq_zero(result)\
                and result['unknown_cnt'] >= 1\
                and result['noteval_cnt'] >= 0\
                and result['notappl_cnt'] >= 0:
            out_result = 'unknown'
        elif result['true_cnt'] < 2\
                and result['false_cnt'] >= 0\
                and self._error_eq_zero(result)\
                and self._unknown_eq_zero(result)\
                and self._noteval_greater_zero(result)\
                and result['notappl_cnt'] >= 0:
            out_result = 'noteval'
        else:
            out_result = None
        return out_result

    def _oval_operator_or(self, result):
        out_result = None
        if self._true_greater_zero(result):
            out_result = 'true'
        elif self._true_eq_zero(result)\
                and self._false_greater_zero(result)\
                and self._error_unknown_noteval_eq_zero(result):
            out_result = 'false'
        elif self._true_eq_zero(result)\
                and self._error_greater_zero(result):
            out_result = 'error'
        elif self._true_eq_zero(result)\
                and self._error_unknown_eq_zero(result):
            out_result = 'unknown'
        elif self._true_eq_zero(result)\
                and self._error_unknown_eq_noteval_greater_zero(result):
            out_result = 'noteval'
        else:
            out_result = None
        return out_result

    def _oval_operator_xor(self, result):
        out_result = None
        if (result['true_cnt'] % 2) == 1\
                and self._error_eq_zero(result)\
                and self._unknown_eq_zero(result)\
                and self._noteval_eq_zero(result):
            out_result = 'true'
        elif (result['true_cnt'] % 2) == 0\
                and self._error_eq_zero(result)\
                and self._unknown_eq_zero(result)\
                and self._noteval_eq_zero(result):
            out_result = 'false'
        elif self._error_greater_zero(result):
            out_result = 'error'
        elif self._error_eq_zero(result)\
                and self._unknown_greater_zero(result):
            out_result = 'unknown'
        elif self._error_eq_zero(result)\
                and self._unknown_eq_zero(result)\
                and self._noteval_greater_zero(result):
            out_result = 'noteval'
        else:
            out_result = None
        return out_result

    def _noteval_eq_zero(self, result):
        if result['noteval_cnt'] == 0:
            return True
        return False

    def _false_eq_zero(self, result):
        if result['false_cnt'] == 0:
            return True
        return False

    def _error_eq_zero(self, result):
        if result['error_cnt'] == 0:
            return True
        return False

    def _unknown_eq_zero(self, result):
        if result['unknown_cnt'] == 0:
            return True
        return False

    def _true_eq_zero(self, result):
        if result['true_cnt'] == 0:
            return True
        return False

    def _true_greater_zero(self, result):
        if result['true_cnt'] > 0:
            return True
        return False

    def _false_greater_zero(self, result):
        if result['false_cnt'] > 0:
            return True
        return False

    def _error_greater_zero(self, result):
        if result['error_cnt'] > 0:
            return True
        return False

    def _unknown_greater_zero(self, result):
        if result['unknown_cnt'] > 0:
            return True
        return False

    def _noteval_greater_zero(self, result):
        if result['noteval_cnt'] > 0:
            return True
        return False

    def _error_unknown_noteval_eq_zero(self, result):
        if self._error_eq_zero(result)\
                and self._unknown_eq_zero(result)\
                and self._noteval_eq_zero(result):
            return True
        return False

    def _error_unknown_eq_noteval_greater_zero(self, result):
        if self._error_eq_zero(result)\
                and self._unknown_eq_zero(result)\
                and self._noteval_greater_zero(result):
            return True
        return False

    def _error_unknown_eq_zero(self, result):
        if self._error_eq_zero(result)\
                and self._unknown_greater_zero(result):
            return True
        return False


def dict_to_tree(dict_of_tree):
    if dict_of_tree["child"] is None:
        return OvalNode(
            dict_of_tree["node_id"],
            dict_of_tree["type"],
            dict_of_tree["value"])
    return OvalNode(
        dict_of_tree["node_id"],
        dict_of_tree["type"],
        dict_of_tree["value"],
        [dict_to_tree(i) for i in dict_of_tree["child"]])

# Help function for transfer XML definition to OVAL_TREE


def xml_dict_to_node(dict_of_definition, sub_node_id):
    children = []
    for child in dict_of_definition['node']:
        if 'operator' in child and 'id':
            sub_node_id = sub_node_id + 1
            children.append(xml_dict_to_node(child, sub_node_id))
        else:
            if child['value'] == 'not evaluated':
                children.append(
                    OvalNode(child['value_id'], 'value', 'noteval')
                )
            else:
                children.append(
                    OvalNode(child['value_id'], 'value', child['value'])
                )

    if 'id' in dict_of_definition:
        children[0].node_id = dict_of_definition['id']
        return children[0]
    else:
        return OvalNode(
            sub_node_id,
            'operator',
            dict_of_definition['operator'],
            children
        )

# Function for build dict form XML


def build_node(tree):
    node = dict(operator=tree.get('operator'), node=[])
    for child in tree:
        if child.get('operator') is not None:
            node['node'].append(build_node(child))
        else:
            if child.get('definition_ref') is not None:
                node['node'].append(
                    dict(extend_definition=child.get('definition_ref')))
            else:
                node['node'].append(
                    dict(
                        value_id=child.get('test_ref'),
                        value=child.get('result')))
    return node


def build_tree(tree_data):
    test = dict(id=tree_data.get('definition_id'), node=[])
    for tree in tree_data:
        test['node'].append(build_node(tree))
    return test


def parse_data_to_dict(trees_data):
    scan = dict(scan="none", definitions=[])
    for i in trees_data:
        scan['definitions'].append(build_tree(i))
    return fill_extend_definition(scan)


# Function for remove extend definitions from dict


def find_definition_by_id(scan, id):
    for definition in scan['definitions']:
        if definition['id'] == id:
            return operator_as_child(definition['node'][0], scan)


def fill_extend_definition(scan):
    definitions = scan['definitions']
    out = dict(scan="none", definitions=[])
    for definition in scan['definitions']:
        nodes = []
        for value in definition['node']:
            nodes.append(operator_as_child(value, scan))
        out['definitions'].append(dict(id=definition['id'], node=nodes))
    return out


def operator_as_child(value, scan):
    out = dict(operator=value['operator'], node=[])
    for child in value['node']:
        if 'operator' in child:
            out['node'].append(operator_as_child(child, scan))
        elif 'extend_definition' in child:
            out['node'].append(
                find_definition_by_id(
                    scan, child['extend_definition']))
        elif 'value_id' in child:
            out['node'].append(child)
        else:
            raise ValueError('error - unknown child')
    return out


# Mine data form XML


def get_data_form_xml(src):
    tree = ET.parse(src)
    root = tree.getroot()

    ns = {
        'ns0': 'http://oval.mitre.org/XMLSchema/oval-results-5',
        'ns1': 'http://scap.nist.gov/schema/asset-reporting-format/1.1'
    }

    report_data = None
    reports = root.find('.//ns1:reports', ns)
    for report in reports:
        if report.get("id") == "oval0":
            report_data = report

    trees_data = report_data.find(
        './/ns0:oval_results/ns0:results/ns0:system/ns0:definitions', ns)
    return trees_data

# Function for transfer XML to OVAL_TREE


def xml_to_tree(xml_src):
    data = parse_data_to_dict(get_data_form_xml(xml_src))
    out = []
    for definition in data['definitions']:
        out.append(xml_dict_to_node(definition, 0))
    return out
