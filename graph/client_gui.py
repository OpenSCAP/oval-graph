from __future__ import print_function, unicode_literals
from pprint import pprint
from PyInquirer import style_from_dict, Token, prompt, Separator
from examples import custom_style_2
import re
import graph.xml_parser
import graph.oval_graph
import webbrowser
import json


class clientGui():
    def __init__(self, args):
        self.source_filename = args.source_filename
        self.rule_name = args.rule_name
        self.args = args
        self.xml_parser = graph.xml_parser.xml_parser(args.source_filename)

    def get_answers(self):
        rules = self.search_rules_id()
        questions = [{
            'type': 'checkbox',
            'message': 'Select rules',
            'name': 'rules',
            'choices': [
                Separator('= The Rules ID =')],
            'validate': (lambda answer: 'You must choose at least one topping.'
                         if len(answer) == 0 else True)
        }]
        for rule in rules:
            questions[0]['choices'].append(dict(name=rule['id_rule']))
        return prompt(questions, style=custom_style_2)

    def search_rules_id(self):
        rules = [
            x for x in self.xml_parser.get_used_rules() if re.search(
                self.rule_name, x['id_rule'])]
        notselected_rules = [
            x for x in self.xml_parser.get_notselected_rules() if re.search(
                self.rule_name, x['id_rule'])]
        if notselected_rules is not None and rules is None:
            raise ValueError(
                'err- rule/s "{}" was not selected, so there are no results.'
                .format(notselected_rules))
        elif notselected_rules is None and rules is None:
            raise ValueError('err- 404 rule not found!')
        else:
            return rules

    def show_rules(self, rules):
        try:
            for rule in rules['rules']:
                oval_tree = graph.oval_graph.build_nodes_form_xml(
                    self.source_filename, rule)
                with open('html_interpreter/data.js', "w+") as file:
                    file.write(
                        "var data_json =" + str(
                            json.dumps(
                                oval_tree.to_sigma_dict(0,0),
                                sort_keys=False,
                                indent=4) + ";"))
                webbrowser.get('firefox').open_new_tab(
                    'html_interpreter/index.html')
                print('Rule "{}" done!'.format(rule))
        except Exception as error:
            print('Rule: "{}" Error: "{}"'.format(rule, error))
