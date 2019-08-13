"""
Playgrounds are scripts where i testing and preparing new things and  new futures.

parsing xml
"""

import graph.oval_graph
import pprint
import json
"""
from lxml import etree as ET


# Function for build dict


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

# Function for remove extend definition


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
            print('ERROR')
    return out

# ?????????????????????????????????????????????????????????????????????????????

def clean_definitions(definitions, used_rules):
    out = []
    for definition in definitions['definitions']:
        for rule in used_rules:
            rule_id, def_id = rule.items()
            if def_id[1] == definition['id']:
                out.append(dict(rule_id=rule_id[1],definition=definition))
    return dict(scan="none", rules=out)

def parse_data_to_dict(trees_data,used_rules):
    scan = dict(scan="none", definitions=[])
    for i in trees_data:
        scan['definitions'].append(build_tree(i))

    # save results
    if True:
        f = open("def0.txt", "w+")
        f.write(str(json.dumps(scan, sort_keys=False, indent=4)))
        f.close()

        f = open("def1.txt", "w+")
        f.write(str(json.dumps(fill_extend_definition(
            scan), sort_keys=False, indent=4)))
        f.close()

        f = open("def3.txt", "w+")
        f.write(str(json.dumps(clean_definitions(fill_extend_definition(scan),used_rules), sort_keys=False, indent=4)))
        f.close()

    return clean_definitions(fill_extend_definition(scan),used_rules)

# mine data form XML
def get_root_of_XML(src):
    tree = ET.parse(src)
    return tree.getroot()


def get_data_form_xml(src):
    root = get_root_of_XML(src)

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
    root = get_root_of_XML(src)

    testResults = root.find('.//{http://checklists.nist.gov/xccdf/1.2}TestResult')
    #print(testResults)
    ruleResults = testResults.findall('.//{http://checklists.nist.gov/xccdf/1.2}rule-result')
    
    rules = []
    for ruleResult in ruleResults:
        for res in ruleResult:
            if res.text=="fail" or res.text=="pass":
                idk = ruleResult.get('idref')
                for res in ruleResult:
                    for r in res:
                        if r.get('href')=='#oval0':
                            rules.append(dict( id_rule =  idk, id_def = r.get('name')))
    #print(rules)
    return rules

# interpret data
src = 'data/ssg-fedora-ds-arf.xml'

print(
    json.dumps(
        parse_data_to_dict(
            get_data_form_xml(src),get_used_rules(src)),
        sort_keys=False,
        indent=4))

data = parse_data_to_dict(get_data_form_xml(src),get_used_rules(src))

f = open("tree.txt", "w+")


for rule in data['rules']:
    #print(definition)
    if rule['definition']['id'] == 'oval:ssg-accounts_passwords_pam_faillock_deny:def:1':
        oval_tree = tree.oval_tree.xml_dict_of_rule_to_node(rule)
        assert oval_tree.evaluate_tree() == 'false'
        f.write(str(json.dumps(oval_tree.tree_to_dict(), sort_keys=False, indent=4)))
f.close()
"""

src = 'data/ssg-fedora-ds-arf.xml'
rule_id = 'xccdf_org.ssgproject.content_rule_disable_host_auth'
result = 'true'

test=1
if test==1:
    #rule_id = 'xccdf_org.ssgproject.content_rule_sshd_disable_rhosts'
    rule_id = 'xccdf_org.ssgproject.content_rule_disable_host_auth'
    result = 'true'
elif test==2:
    rule_id = 'xccdf_org.ssgproject.content_rule_accounts_passwords_pam_faillock_deny'
    result = 'false'
elif test==3:
    rule_id = 'xccdf_org.ssgproject.content_rule_package_sendmail_removed'
    result = 'true'
elif test==4:
    rule_id = 'xccdf_org.ssgproject.content_rule_require_singleuser_auth'
    result = 'true'


oval_trees_array = graph.oval_graph.xml_to_tree(src)
for oval_tree in oval_trees_array:
    if oval_tree.node_id == rule_id:
        assert oval_tree.evaluate_tree() == result
        f1 = open("sigmaJs.txt", "w+")
        f1.write(json.dumps(oval_tree.to_sigma_dict(0,0), sort_keys=False, indent=4))
        f1.close()

        f = open("tree.txt", "w+")
        f.write(json.dumps(oval_tree.tree_to_dict(), sort_keys=False, indent=4))
        f.close()

        f = open("html_interpreter/data.json", "w+")
        f.write(json.dumps(oval_tree.to_sigma_dict(0,0), sort_keys=False, indent=4))
        f.close()

     