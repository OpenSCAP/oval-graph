'''
    Modules for create node IDs and parsing xml
'''
import uuid
import os

from lxml import etree as ET

from .oval_node import OvalNode

ns = {
    'XMLSchema': 'http://oval.mitre.org/XMLSchema/oval-results-5',
    'xccdf': 'http://checklists.nist.gov/xccdf/1.2',
    'arf': 'http://scap.nist.gov/schema/asset-reporting-format/1.1',
    'oval-definitions': 'http://oval.mitre.org/XMLSchema/oval-definitions-5',
    'scap': 'http://scap.nist.gov/schema/scap/source/1.2',
}


class XmlParser():
    def __init__(self, src):
        self.src = src
        self.tree = ET.parse(self.src)
        self.root = self.tree.getroot()
        if not self.validate(
                'schemas/arf/1.1/asset-reporting-format_1.1.0.xsd'):
            raise ValueError("err- This is not arf report file.")
        self.used_rules = self._get_used_rules()
        self.notselected_rules = self._get_notselected_rules()
        self.scan_definitions = self._get_scan()

    def get_src(self, src):
        _dir = os.path.dirname(os.path.realpath(__file__))
        FIXTURE_DIR = os.path.join(_dir, src)
        return str(FIXTURE_DIR)

    def validate(self, xsd_path):
        xsd_path = self.get_src(xsd_path)
        xmlschema_doc = ET.parse(xsd_path)
        xmlschema = ET.XMLSchema(xmlschema_doc)

        xml_doc = self.tree
        result = xmlschema.validate(xml_doc)

        return result

    def get_data(self, href):
        report_data = None
        reports = self.root.find('.//arf:reports', ns)
        for report in reports:
            if "#" + str(report.get("id")) == href:
                report_data = report

        trees_data = report_data.find(
            ('.//XMLSchema:oval_results/XMLSchema:results/'
             'XMLSchema:system/XMLSchema:definitions'), ns)
        return trees_data

    def _get_used_rules(self):
        rulesResults = self.root.findall(
            './/xccdf:TestResult/xccdf:rule-result', ns)
        rules = []
        for ruleResult in rulesResults:
            result = ruleResult.find('.//xccdf:result', ns)
            if result.text != "notselected":
                check_content_ref = ruleResult.find(
                    './/xccdf:check/xccdf:check-content-ref', ns)
                if check_content_ref is not None:
                    rules.append(dict(
                        id_rule=ruleResult.get('idref'),
                        id_def=check_content_ref.attrib.get('name'),
                        href=check_content_ref.attrib.get('href'),
                        result=result.text,
                    ))
        return rules

    def _get_notselected_rules(self):
        rulesResults = self.root.findall(
            './/xccdf:TestResult/xccdf:rule-result', ns)
        rules = []
        for ruleResult in rulesResults:
            result = ruleResult.find('.//xccdf:result', ns)
            if result.text == "notselected":
                rules.append(dict(id_rule=ruleResult.get('idref')))
        return rules

    def _get_scan(self):
        scan = dict(definitions=[])
        for i in self.get_data(self.used_rules[0]['href']):
            scan['definitions'].append(self.build_graph(i))
        self.insert_comments(scan)
        return self._fill_extend_definition(scan)

    def parse_data_to_dict(self, rule_id):
        for definition in self.scan_definitions['definitions']:
            if self.get_def_id_by_rule_id(rule_id) == definition['id']:
                return dict(rule_id=rule_id, definition=definition)

    def _xml_dict_to_node(self, dict_of_definition):
        children = []
        for child in dict_of_definition['node']:
            if 'operator' in child and 'id':
                children.append(self._xml_dict_to_node(child))
            else:
                children.append(
                    OvalNode(
                        child['value_id'],
                        'value',
                        child['value'],
                        child['negate'],
                        child['comment'],
                        child['tag']
                    ))

        if 'id' in dict_of_definition:
            children[0].node_id = dict_of_definition['id']
            return children[0]
        else:
            return OvalNode(
                str(uuid.uuid4()),
                'operator',
                dict_of_definition['operator'],
                dict_of_definition['negate'],
                dict_of_definition['comment'],
                dict_of_definition['tag'],
                children,
            )

    def get_def_id_by_rule_id(self, rule_id):
        for rule in self.notselected_rules:
            if rule['id_rule'] == rule_id:
                raise ValueError(
                    'err- rule "{}" was not selected, so there are no results.'
                    .format(rule_id))
        for rule in self.used_rules:
            if rule['id_rule'] == rule_id:
                return rule['id_def']
        raise ValueError('err- 404 rule not found!')

    def get_rule_dict(self, rule_id):
        return self.parse_data_to_dict(rule_id)

    def xml_dict_of_rule_to_node(self, rule):
        dict_of_definition = rule['definition']
        return OvalNode(
            rule['rule_id'],
            'operator',
            'and',
            False,
            dict_of_definition['comment'],
            "Rule",
            [self._xml_dict_to_node(dict_of_definition)],
        )

    def get_oval_tree(self, rule_id=None):
        return self.xml_dict_of_rule_to_node(self.parse_data_to_dict(rule_id))

    def build_graph(self, tree_data):
        graph = dict(
            id=tree_data.get('definition_id'),
            node=[],
        )
        for tree in tree_data:
            negate_status = False
            if 'negate' in tree:
                negate_status = self._str_to_bool(tree.get('negate'))
            graph['negate'] = negate_status
            graph['node'].append(self._build_node(tree, "Definition"))
        return graph

    def _str_to_bool(self, s):
        if s == 'true':
            return True
        elif s == 'false':
            return False
        else:
            raise ValueError('err- negation is not bool')

    def _build_node(self, tree, tag):
        negate_status = False
        if tree.get('negate') is not None:
            negate_status = self._str_to_bool(tree.get('negate'))

        node = dict(
            operator=tree.get('operator'),
            negate=negate_status,
            result=tree.get('result'),
            comment=None,
            tag=tag,
            node=[],
        )
        for child in tree:
            if child.get('operator') is not None:
                node['node'].append(self._build_node(child, "Criteria"))
            else:
                negate_status = False
                if child.get('negate') is not None:
                    negate_status = self._str_to_bool(child.get('negate'))

                if child.get('definition_ref') is not None:
                    node['node'].append(
                        dict(
                            extend_definition=child.get('definition_ref'),
                            result=child.get('result'),
                            negate=negate_status,
                            comment=None,
                            tag="Extend definition",
                        ))
                else:
                    node['node'].append(
                        dict(
                            value_id=child.get('test_ref'),
                            value=child.get('result'),
                            negate=negate_status,
                            comment=None,
                            tag="Test",
                        ))
        return node

    def _fill_extend_definition(self, scan):
        out = dict(definitions=[])
        for definition in scan['definitions']:
            nodes = []
            for value in definition['node']:
                nodes.append(self._operator_as_child(value, scan))
            out['definitions'].append(
                dict(
                    id=definition['id'],
                    comment=definition['comment'],
                    node=nodes,
                ))
        return out

    def _operator_as_child(self, value, scan):
        out = dict(
            operator=value['operator'],
            negate=value['negate'],
            result=value['result'],
            comment=value['comment'],
            tag=value['tag'],
            node=[],
        )
        for child in value['node']:
            if 'operator' in child:
                out['node'].append(self._operator_as_child(child, scan))
            elif 'extend_definition' in child:
                out['node'].append(
                    self._find_definition_by_id(
                        scan,
                        child['extend_definition'],
                        child['negate'],
                        child['comment'],
                        child['tag'],
                    ))
            elif 'value_id' in child:
                out['node'].append(child)
            else:
                raise ValueError('error - unknown child')
        return out

    def _find_definition_by_id(self, scan, id, negate_status, comment, tag):
        for definition in scan['definitions']:
            if definition['id'] == id:
                definition['node'][0]['negate'] = negate_status
                definition['node'][0]['comment'] = comment
                definition['node'][0]['tag'] = tag
                return self._operator_as_child(definition['node'][0], scan)

    def create_dict_form_criteria(self, criteria, description):
        comments = dict(
            operator='AND' if criteria.get('operator') is None else criteria.get('operator'),
            comment=description if criteria.get('comment') is None else criteria.get('comment'),
            node=[],
        )
        for criterion in criteria:
            if criterion.get('operator'):
                comments['node'].append(
                    self.create_dict_form_criteria(criterion, None))
            else:
                if criterion.get('definition_ref'):
                    comments['node'].append(
                        dict(
                            extend_definition=criterion.get('definition_ref'),
                            comment=criterion.get('comment'),
                        ))
                else:
                    comments['node'].append(
                        dict(
                            value_id=criterion.get('test_ref'),
                            comment=criterion.get('comment'),
                        ))
        return comments

    def _prepare_definition_comments(self):
        oval_definitions = self.root.find(
            './/arf:report-requests/arf:report-request/'
            'arf:content/scap:data-stream-collection/'
            'scap:component/oval-definitions:oval_definitions/'
            'oval-definitions:definitions', ns)
        definitions = []
        for definition in oval_definitions:
            comment_definition = dict(
                id=definition.get('id'), comment=None, node=[])
            title = definition.find(
                './/oval-definitions:metadata/oval-definitions:title', ns)
            description = definition.find(
                './/oval-definitions:metadata/oval-definitions:description', ns)
            comment_definition['comment'] = title.text
            criteria = definition.find('.//oval-definitions:criteria', ns)
            comment_definition['node'].append(
                self.create_dict_form_criteria(criteria, description.text))
            definitions.append(comment_definition)
        return definitions

    def recursive_help_fill_comments(self, comments, nodes):
        out = nodes
        out['comment'] = comments['comment']
        for node, comment in zip(out['node'], comments['node']):
            node['comment'] = comment['comment']
            if 'operator' in node:
                self.recursive_help_fill_comments(comment, node)

    def fill_comment(self, comment_definition, data_definition):
        comments = comment_definition['node'][0]
        nodes = data_definition['node'][0]
        data_definition['comment'] = comment_definition['comment']
        self.recursive_help_fill_comments(comments, nodes)

    def insert_comments(self, data):
        comment_definitions = self._prepare_definition_comments()
        for data_definition in data['definitions']:
            for comment_definition in comment_definitions:
                if comment_definition['id'] == data_definition['id']:
                    self.fill_comment(comment_definition, data_definition)
