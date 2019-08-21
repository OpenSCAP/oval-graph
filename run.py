import graph.client
import sys 
def main():
    client=graph.client.client(sys.argv[1:])
    answers=client.run_gui_and_return_answers()
    client.show_graphs(answers)
  

if __name__ == '__main__':
    main()