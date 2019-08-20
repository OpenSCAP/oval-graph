import argparse
import graph.client_gui

def parse_arguments():
    parser = argparse.ArgumentParser(description='Client for visualization scanned rule from Security scan.')

    parser.add_argument("source_filename", help='ARF scan file')
    parser.add_argument("rule_name", help='Rule ID to be visualized. You can input part of ID rule.')
    parser.set_defaults(func=run)

    args = parser.parse_args()

    return args


def run(args):
    client=graph.client_gui.clientGui(args)    
    answers=client.get_answers()
    client.show_rules(answers)
    
arg = parse_arguments()
arg.func(arg)
