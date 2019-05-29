import tree.oval_tree
from lxml import etree as ET
import pprint
import json
pp = pprint.PrettyPrinter(indent=4)

#Function for interpreting data
def build_node(tree):
    node=dict(operator=tree.get('operator'),children=[])
    #print('OPERATOR: ', tree.get('operator'), tree.get('result'))
    for child in tree:
        if child.get('operator') is not None:
            node['children'].append(build_node(child))
        else:
            if child.get('definition_ref') is not None:
                    #print("extend_definition: ", child.get('result'))
                    node['children'].append(dict(extend_definition = child.get('definition_ref')))
            else:
                node['children'].append(dict(value_id=child.get('test_ref'),value=child.get('result')))
                #print('subTEST RES:',child.get('result'))
    return node

def build_tree(tree_data):
    test = dict(id=tree_data.get('definition_id'),tree=[])

    #print('TEST NAME: ', tree_data.get('definition_id'))
    for tree in tree_data:
        test['tree'].append(build_node(tree))
    
    #print(" ")
    return test

def fill_extend_definition(scan):
    definitions=scan['definitions']
    trees={}
    out=dict(scan="none", definitions=[])
    for definition in scan['definitions']:
        #print(definition['id'])
        for value in definition['tree']:
            print(json.dumps(value,sort_keys=False, indent=4))
            trees.append(operator_as_child(value,scan))
            #break
        out['definitions']=dict(id=definition['id'],tree=trees)
        #print(definition['tree'][0]['children'])

def operator_as_child(value):
    out=dict(operator=value['operator'],children=[])
    for child in value['children']:
        #print(child['extend_definition'])
        
        if 'operator' in child:
            operator_as_child(child)
        else:
            if 'extend_definition' in child:
                print(json.dumps(child,sort_keys=False, indent=4))
            
           

def run(trees_data):
    scan=dict(scan="none", definitions=[])
    for i in trees_data:
        scan['definitions'].append(build_tree(i))
    fill_extend_definition(scan)
    #print (json.dumps(scan,sort_keys=False, indent=4))
    
#parse data 
def get_data_form_xml(src):
    tree = ET.parse(src)
    root = tree.getroot()

    ns = {
        'ns0': 'http://oval.mitre.org/XMLSchema/oval-results-5',
        'ns1': 'http://scap.nist.gov/schema/asset-reporting-format/1.1'
    }

    reports = root.find('.//ns1:reports', ns)
    for report in reports:
        if report.get("id") == "oval0":
            report_data = report

    trees_data = report_data.find(
        './/ns0:oval_results/ns0:results/ns0:system/ns0:definitions', ns)
    return trees_data

#interpret data
src = 'data/ssg-fedora-ds-arf.xml'
run(get_data_form_xml(src))