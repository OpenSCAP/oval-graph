import graph.oval_graph
import json
import argparse
import webbrowser


def parse_arguments():
    parser = argparse.ArgumentParser(description='client')

    parser.add_argument("source_filename", help='arf scan file')
    parser.add_argument("rule_name", help='Name of rule form scan')
    parser.set_defaults(func=run)

    args = parser.parse_args()

    return args


def run(args):
    try:
        oval_tree = graph.oval_graph.build_nodes_form_xml(
            args.source_filename, args.rule_name)
        with open('html_interpreter/data/data.js', "w+") as file:
            file.write(
                "var data_json =" + str(
                    json.dumps(
                        oval_tree.to_sigma_dict(
                            0,
                            0),
                        sort_keys=False,
                        indent=4) + ";"))

        webbrowser.get('firefox').open_new_tab('html_interpreter/index.html')
    except (RuntimeError, TypeError, NameError, ValueError) as e:
        print(e)


arg = parse_arguments()
arg.func(arg)
