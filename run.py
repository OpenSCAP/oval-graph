import graph.oval_graph
import graph.xml_parser
import json
import argparse
import webbrowser


def parse_arguments():
    parser = argparse.ArgumentParser(description='Client for visualization scanned rule from Security scan.')

    parser.add_argument("source_filename", help='ARF scan file')
    parser.add_argument("rule_name", help='Rule ID to be visualized. You can input part of ID rule.')
    parser.set_defaults(func=run)

    args = parser.parse_args()

    return args


def run(args):
    try:
        xml_parser=graph.xml_parser.xml_parser(args.source_filename)
        used_rules = xml_parser.get_used_rules()
        

        oval_tree = graph.oval_graph.build_nodes_form_xml(
            args.source_filename, args.rule_name)
        with open('html_interpreter/data.js', "w+") as file:
            file.write(
                "var data_json =" +
                str(json.dumps(oval_tree.to_sigma_dict(0, 0), sort_keys=False, indent=4) +
                    ";"))

        webbrowser.get('firefox').open_new_tab('html_interpreter/index.html')
    except (RuntimeError, TypeError, NameError, ValueError) as error:
        print(error)


arg = parse_arguments()
arg.func(arg)
