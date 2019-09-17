import sys

from .client import client


def print_where_is_saved_result(results_src):
    print("Results are saved:")
    for src in results_src:
        print(src)


def main():
    client_ = client(sys.argv[1:])
    rules = client_.search_rules_id()
    if len(rules) > 1:
        answers = client_.run_gui_and_return_answers()
        if answers is None:
            print("You haven't got installed inquirer lib. "
                  "Please copy id rule with you want use and put it in command")
        else:
            results_src = client_.prepare_data(answers)
            print_where_is_saved_result(results_src)
    else:
        results_src = client_.prepare_data({'rules': [rules[0]['id_rule']]})
        print_where_is_saved_result(results_src)


if __name__ == '__main__':
    main()