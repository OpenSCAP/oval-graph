import graph.client
import sys 
def main():
    client=graph.client.client(sys.argv[1:])
    answers=client.get_answers()
    client.show_rules(answers)
  

if __name__ == '__main__':
    main()