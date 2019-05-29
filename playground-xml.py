import tree.oval_tree
from lxml import etree as ET
import pprint
import json

# Function for build dict


def build_node(tree):
    node = dict(operator=tree.get('operator'), children=[])
    for child in tree:
        if child.get('operator') is not None:
            node['children'].append(build_node(child))
        else:
            if child.get('definition_ref') is not None:
                node['children'].append(
                    dict(extend_definition=child.get('definition_ref')))
            else:
                node['children'].append(
                    dict(
                        value_id=child.get('test_ref'),
                        value=child.get('result')))
    return node


def build_tree(tree_data):
    test = dict(id=tree_data.get('definition_id'), tree=[])
    for tree in tree_data:
        test['tree'].append(build_node(tree))
    return test

# Function for remove extend definition


def find_definition_by_id(scan, id):
    for definition in scan['definitions']:
        if definition['id'] == id:
            return operator_as_child(definition['tree'][0], scan)


def fill_extend_definition(scan):
    definitions = scan['definitions']
    trees = []
    out = dict(scan="none", definitions=[])
    for definition in scan['definitions']:
        for value in definition['tree']:
            trees.append(operator_as_child(value, scan))
        out['definitions'].append(dict(id=definition['id'], tree=trees))
    return out


def operator_as_child(value, scan):
    out = dict(operator=value['operator'], children=[])
    for child in value['children']:
        if 'operator' in child:
            out['children'].append(operator_as_child(child, scan))
        elif 'extend_definition' in child:
            out['children'].append(
                find_definition_by_id(
                    scan, child['extend_definition']))
        elif 'value_id' in child:
            out['children'].append(child)
        else:
            print('ERROR')
    return out

# ?????????????????????????????????????????????????????????????????????????????


def parse_data_to_dict(trees_data):
    scan = dict(scan="none", definitions=[])
    for i in trees_data:
        scan['definitions'].append(build_tree(i))

    # save results
    if False:
        f = open("def0.txt", "w+")
        f.write(str(json.dumps(scan, sort_keys=False, indent=4)))
        f.close()

        f = open("def1.txt", "w+")
        f.write(str(json.dumps(fill_extend_definition(
            scan), sort_keys=False, indent=4)))
        f.close()

    return fill_extend_definition(scan)

# mine data form XML


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


# interpret data
src = 'data/ssg-fedora-ds-arf.xml'
print(
    json.dumps(
        parse_data_to_dict(
            get_data_form_xml(src)),
        sort_keys=False,
        indent=4))
