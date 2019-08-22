import graph.client
import sys


def main():
    client = graph.client.client(sys.argv[1:])
    answers = client.run_gui_and_return_answers()
    if answers is None:
        print("You haven't got installed PyInquirer lib. "
              "Please copy id rule with you want use and put it in command")
    else:
        client.prepare_graphs(answers)


if __name__ == '__main__':
    main()
