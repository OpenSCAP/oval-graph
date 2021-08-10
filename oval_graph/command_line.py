"""
    This file contains entry points for commands
"""

import traceback

from .command_line_client.arf_to_html import ArfToHtml
from .command_line_client.arf_to_json import ArfToJson
from .command_line_client.json_to_html import JsonToHtml
from .exceptions import NotTestedRule

C_RED = '\033[91m'
C_END = '\033[0m'
ERRORS = (ValueError, TypeError, ResourceWarning, NotTestedRule, OSError)


def arf_to_graph(params=None):
    catch_errors(ArfToHtml, params)


def arf_to_json(params=None):
    catch_errors(ArfToJson, params)


def json_to_graph(params=None):
    catch_errors(JsonToHtml, params)


def catch_errors(client_class, params):
    client = client_class(params)
    try:
        main(client)
    except ERRORS as error:
        if client.verbose:
            traceback.print_exc()
        print('{}Error: {}{}'.format(C_RED, error, C_END))


def main(client):
    client.load_file()
    rules = client.search_rules_id()
    if len(rules) > 1:
        answers = client.run_gui_and_return_answers()
        if answers is not None:
            return client.prepare_data(answers)
    return client.prepare_data({'rules': [rules[0]]})


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
