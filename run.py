import tree.oval_tree
import pprint
import json
import argparse
import webbrowser
    

def parse_arguments():
    parser = argparse.ArgumentParser(description='client')
   
    parser.add_argument("source_filename",help='arf scan file')
    #parser.add_argument("out_filename",help='out json file')
    parser.add_argument("rule_name",help='Name of rule form scan')
    parser.set_defaults(func=run)
    
    
    args = parser.parse_args()

    return args

def run(args):
    oval_trees_array = tree.oval_tree.xml_to_tree(args.source_filename)
    f = open('html_interpreter/data/data.js', "w+")
    #f = open(args.out_filename, "w+")
            
    for oval_tree in oval_trees_array:
        if oval_tree.node_id == args.rule_name:
            f.write("var data_json =" + str(json.dumps(oval_tree.to_sigma_dict(0,0), sort_keys=False, indent=4) + ";"))
        elif "." == args.rule_name:
            f.write(json.dumps(oval_tree.to_sigma_dict(0,0), sort_keys=False, indent=4))
    f.close()
    
    webbrowser.get('firefox').open_new_tab('html_interpreter/index.html')


arg = parse_arguments()
arg.func(arg)