import tree.oval_tree
import uuid
#import collections
from lxml import etree as ET

def _xml_dict_to_node(dict_of_definition):
    children = []
    for child in dict_of_definition['node']:
        if 'operator' in child and 'id':
            children.append(_xml_dict_to_node(child))
        else:
            children.append(
                tree.oval_tree.OvalNode(child['value_id'], 'value', child['value'])
            )

    if 'id' in dict_of_definition:
        children[0].node_id = dict_of_definition['id']
        return children[0]
    else:
        return tree.oval_tree.OvalNode(
            str(uuid.uuid4()),
            'operator',
            dict_of_definition['operator'],
            children
        )


def xml_dict_of_rule_to_node(rule):
    dict_of_definition = rule['definition']
    return tree.oval_tree.OvalNode(
        rule['rule_id'],
        'operator',
        'and',
        [_xml_dict_to_node(dict_of_definition)]
    )

# Function for build dict form XML


def _build_node(tree):
    node = dict(operator=tree.get('operator'), node=[])
    for child in tree:
        if child.get('operator') is not None:
            node['node'].append(_build_node(child))
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
        test['node'].append(_build_node(tree))
    return test


def clean_definitions(definitions, used_rules):
    out = []
    for definition in definitions['definitions']:
        for rule in used_rules:
            rule_id, def_id = rule.items()
            if def_id[1] == definition['id']:
                out.append(dict(rule_id=rule_id[1], definition=definition))
    return dict(scan="none", rules=out)


def parse_data_to_dict(trees_data, used_rules):
    scan = dict(scan="none", definitions=[])
    for i in trees_data:
        scan['definitions'].append(build_tree(i))
    return clean_definitions(_fill_extend_definition(scan), used_rules)


# Function for remove extend definitions from dict


def find_definition_by_id(scan, id):
    for definition in scan['definitions']:
        if definition['id'] == id:
            return _operator_as_child(definition['node'][0], scan)


def _fill_extend_definition(scan):
    out = dict(scan="none", definitions=[])
    for definition in scan['definitions']:
        nodes = []
        for value in definition['node']:
            nodes.append(_operator_as_child(value, scan))
        out['definitions'].append(dict(id=definition['id'], node=nodes))
    return out


def _operator_as_child(value, scan):
    out = dict(operator=value['operator'], node=[])
    for child in value['node']:
        if 'operator' in child:
            out['node'].append(_operator_as_child(child, scan))
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


def _get_root_of_XML(src):
    tree = ET.parse(src)
    return tree.getroot()


def get_data_form_xml(src):
    root = _get_root_of_XML(src)

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


def get_used_rules(src):
    root = _get_root_of_XML(src)

    testResults = root.find(
        './/{http://checklists.nist.gov/xccdf/1.2}TestResult')
    ruleResults = testResults.findall(
        './/{http://checklists.nist.gov/xccdf/1.2}rule-result')

    rules = []
    for ruleResult in ruleResults:
        for res in ruleResult:
            if res.text == "fail" or res.text == "pass":
                idk = ruleResult.get('idref')
                for res in ruleResult:
                    for r in res:
                        if r.get('href') == '#oval0':
                            rules.append(
                                dict(
                                    id_rule=idk,
                                    id_def=r.get('name')))
    return rules
