import sys
import traceback

from .command_line_client.arf_to_html import ArfToHtml
from .command_line_client.arf_to_json import ArfToJson
from .command_line_client.json_to_html import JsonToHtml

CRED = '\033[91m'
CEND = '\033[0m'


def print_where_is_saved_result(results_src):
    if results_src:
        print("Results are saved:", file=sys.stderr)
        for src in results_src:
            print(src, file=sys.stderr)


def print_detail_traceback_if_verbose(args):
    if any(arg in args for arg in ("-v", "--verbose")):
        traceback.print_exc()


def arf_to_graph(args=None):
    try:
        main(ArfToHtml(args))
    except Exception as error:
        print_detail_traceback_if_verbose(args)
        print((CRED + 'Error: {}' + CEND).format(error))


def arf_to_json(args=None):
    try:
        main(ArfToJson(args))
    except Exception as error:
        print_detail_traceback_if_verbose(args)
        print((CRED + 'Error: {}' + CEND).format(error))


def json_to_graph(args=None):
    try:
        main(JsonToHtml(args))
    except Exception as error:
        print_detail_traceback_if_verbose(args)
        print((CRED + 'Error: {}' + CEND).format(error))


def main(client):
    results_src = []
    rules = client.search_rules_id()
    if len(rules) > 1:
        answers = client.run_gui_and_return_answers()
        if answers is not None:
            results_src = client.prepare_data(answers)
    else:
        results_src = client.prepare_data({'rules': [rules[0]]})
    if client.arg.verbose:
        print_where_is_saved_result(results_src)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser_arf_to_graph = subparsers.add_parser(
        'arf-to-graph', help='Executes the arf-to-graph command.')
    parser_arf_to_graph.set_defaults(command=arf_to_graph)

    parser_arf_to_json = subparsers.add_parser(
        'arf-to-json', help='Executes the arf-to-json command.')
    parser_arf_to_json.set_defaults(command=arf_to_json)

    parser_json_to_graph = subparsers.add_parser(
        'json-to-graph', help='Executes the json-to-graph command.')
    parser_json_to_graph.set_defaults(command=json_to_graph)

    args, command_args = parser.parse_known_args()
    args.command(command_args)
