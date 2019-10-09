import oval_graph.client
import sys


def main():
    client = oval_graph.client.client(sys.argv[1:])
    rules = client.search_rules_id()
    if len(rules) > 1:
        answers = client.run_gui_and_return_answers()
        if answers is None:
            print("You haven't got installed inquirer lib. "
                  "Please copy id rule with you want use and put it in command")
        else:
            client.prepare_data(answers)
    else:
        client.prepare_data({'rules': [rules[0]['id_rule']]})


if __name__ == '__main__':
    main()
