import graph.client

def main():
    client=graph.client.client()
    answers=client.get_answers()
    client.show_rules(answers)
  

if __name__ == '__main__':
    main()