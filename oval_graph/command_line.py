import sys

from .arf_to_html import ArfToHtml
from .arf_to_json import ArfToJson
from .json_to_html import JsonToHtml

CRED = '\033[91m'
CEND = '\033[0m'


def print_where_is_saved_result(results_src):
    if results_src:
        print("Results are saved:")
        for src in results_src:
            print(src)


def arf_to_graph(args=None):
    try:
        if args is not None:
            main(ArfToHtml(args))
        else:
            main(ArfToHtml(sys.argv[1:]))
    except Exception as error:
        print((CRED + 'Error: {}' + CEND).format(error))


def arf_to_json(args=None):
    try:
        if args is not None:
            main(ArfToJson(args))
        else:
            main(ArfToJson(sys.argv[1:]))
    except Exception as error:
        print((CRED + 'Error: {}' + CEND).format(error))


def json_to_graph(args=None):
    try:
        if args is not None:
            main(JsonToHtml(args))
        else:
            main(JsonToHtml(sys.argv[1:]))
    except Exception as error:
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
    print_where_is_saved_result(results_src)


if __name__ == '__main__':
    if sys.argv[1] == "arf-to-graph":
        arf_to_graph(sys.argv[2:])
    elif sys.argv[1] == "arf-to-json":
        arf_to_json(sys.argv[2:])
    elif sys.argv[1] == "json-to-graph":
        json_to_graph(sys.argv[2:])
    else:
        print("err- Bad command!")
