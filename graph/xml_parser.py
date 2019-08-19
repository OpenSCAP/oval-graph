'''
    Modules for create node IDs and parsing xml
'''

from lxml import etree as ET
import uuid
import graph.oval_graph


class xml_parser():
    def __init__(self, src):
        self.src = src
        self.tree = ET.parse(self.src)
        self.root = self.tree.getroot()
        if not self.validate(
                './schemas/arf/1.1/asset-reporting-format_1.1.0.xsd'):
            raise ValueError("err- This is not arf report file.")

    def validate(self, xsd_path):
        xmlschema_doc = ET.parse(xsd_path)
        xmlschema = ET.XMLSchema(xmlschema_doc)

        xml_doc = self.tree
        result = xmlschema.validate(xml_doc)

        return result

    def get_data(self, href):
        ns = {
            'ns0': 'http://oval.mitre.org/XMLSchema/oval-results-5',
            'ns1': 'http://scap.nist.gov/schema/asset-reporting-format/1.1'
        }

        report_data = None
        reports = self.root.find('.//ns1:reports', ns)
        for report in reports:
            if "#" + str(report.get("id")) == href:
                report_data = report

        trees_data = report_data.find(
            './/ns0:oval_results/ns0:results/ns0:system/ns0:definitions', ns)
        return trees_data

    def get_used_rules(self):
        ns = {
            'ns0': 'http://checklists.nist.gov/xccdf/1.2',
        }
        rulesResults = self.root.findall(
            './/ns0:TestResult/ns0:rule-result', ns)
        rules = []
        for ruleResult in rulesResults:
            result = ruleResult.find('.//ns0:result', ns)
            if result.text != "notselected":
                check_content_ref = ruleResult.find(
                    './/ns0:check/ns0:check-content-ref', ns)
                if check_content_ref is not None:
                    rules.append(dict(
                        id_rule=ruleResult.get('idref'),
                        id_def=check_content_ref.attrib.get('name'),
                        href=check_content_ref.attrib.get('href'),
                        result=result.text))
        return rules

    def get_notselected_rules(self):
        ns = {
            'ns0': 'http://checklists.nist.gov/xccdf/1.2',
        }
        rulesResults = self.root.findall(
            './/ns0:TestResult/ns0:rule-result', ns)
        rules = []
        for ruleResult in rulesResults:
            result = ruleResult.find('.//ns0:result', ns)
            if result.text == "notselected":
                rules.append(dict(id_rule=ruleResult.get('idref')))
        return rules

    def parse_data_to_dict(self, rule_id):
        scan = dict(definitions=[])
        used_rules = self.get_used_rules()
        for i in self.get_data(used_rules[0]['href']):
            scan['definitions'].append(self.build_graph(i))
        definitions = self._fill_extend_definition(scan)
        for definition in definitions['definitions']:
            if self.get_def_id_by_rule_id(rule_id) == definition['id']:
                return dict(rule_id=rule_id, definition=definition)

    def _xml_dict_to_node(self, dict_of_definition):
        children = []
        for child in dict_of_definition['node']:
            if 'operator' in child and 'id':
                children.append(self._xml_dict_to_node(child))
            else:
                children.append(
                    graph.oval_graph.OvalNode(
                        child['value_id'],
                        'value',
                        child['value'],
                        child['negate']))

        if 'id' in dict_of_definition:
            children[0].node_id = dict_of_definition['id']
            return children[0]
        else:
            return graph.oval_graph.OvalNode(
                str(uuid.uuid4()),
                'operator',
                dict_of_definition['operator'],
                dict_of_definition['negate'],
                children
            )

    def get_def_id_by_rule_id(self, rule_id):
        used_rules = self.get_used_rules()
        notselected_rules = self.get_notselected_rules()
        for rule in notselected_rules:
            if rule['id_rule'] == rule_id:
                raise ValueError(
                    'err- rule "{}" was not selected, so there are no results.'
                    .format(rule_id))
        for rule in used_rules:
            if rule['id_rule'] == rule_id:
                return rule['id_def']
        raise ValueError('err- 404 rule not found!')

    def get_rule_dict(self, rule_id):
        return self.parse_data_to_dict(rule_id)

    def xml_dict_of_rule_to_node(self, rule):
        dict_of_definition = rule['definition']
        return graph.oval_graph.OvalNode(
            rule['rule_id'],
            'operator',
            'and',
            False,
            [self._xml_dict_to_node(dict_of_definition)]
        )

    def get_oval_graph(self, rule_id=None):
        return self.xml_dict_of_rule_to_node(self.parse_data_to_dict(rule_id))

    def build_graph(self, tree_data):
        graph = dict(
            id=tree_data.get('definition_id'),
            node=[])
        for tree in tree_data:
            negate_status = False
            if tree.get('negate') is not None:
                negate_status = self._str_to_bool(tree.get('negate'))
            graph['negate'] = negate_status
            graph['node'].append(self._build_node(tree))
        return graph

    def _str_to_bool(self, s):
        if s == 'true':
            return True
        elif s == 'false':
            return False
        else:
            raise ValueError('err- negation is not bool')

    def _build_node(self, tree):
        negate_status = False
        if tree.get('negate') is not None:
            negate_status = self._str_to_bool(tree.get('negate'))

        node = dict(
            operator=tree.get('operator'),
            negate=negate_status,
            result=tree.get('result'),
            node=[])
        for child in tree:
            if child.get('operator') is not None:
                node['node'].append(self._build_node(child))
            else:
                negate_status = False
                if child.get('negate') is not None:
                    negate_status = self._str_to_bool(child.get('negate'))

                if child.get('definition_ref') is not None:
                    node['node'].append(
                        dict(
                            extend_definition=child.get('definition_ref'),
                            result=child.get('result'),
                            negate=negate_status))
                else:
                    node['node'].append(
                        dict(
                            value_id=child.get('test_ref'),
                            value=child.get('result'),
                            negate=negate_status))
        return node

    def _fill_extend_definition(self, scan):
        out = dict(definitions=[])
        for definition in scan['definitions']:
            nodes = []
            for value in definition['node']:
                nodes.append(self._operator_as_child(value, scan))
            out['definitions'].append(dict(id=definition['id'], node=nodes))
        return out

    def _operator_as_child(self, value, scan):
        out = dict(
            operator=value['operator'],
            negate=value['negate'],
            result=value['negate'],
            node=[])
        for child in value['node']:
            if 'operator' in child:
                out['node'].append(self._operator_as_child(child, scan))
            elif 'extend_definition' in child:
                out['node'].append(
                    self._find_definition_by_id(
                        scan, child['extend_definition'], child['negate']))
            elif 'value_id' in child:
                out['node'].append(child)
            else:
                raise ValueError('error - unknown child')
        return out

    def _find_definition_by_id(self, scan, id, negate_status):
        for definition in scan['definitions']:
            if definition['id'] == id:
                definition['node'][0]['negate'] = negate_status
                return self._operator_as_child(definition['node'][0], scan)
