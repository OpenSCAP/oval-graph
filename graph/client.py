from __future__ import print_function, unicode_literals
import re
import graph.xml_parser
import graph.oval_graph
import webbrowser
import json
import argparse


class client():
    def __init__(self, args):
        self.arg = self.parse_arguments(args)
        self.source_filename = self.arg.source_filename
        self.rule_name = self.arg.rule_id
        self.xml_parser = graph.xml_parser.xml_parser(self.source_filename)

    def run_gui_and_return_answers(self):
        try:
            from PyInquirer import style_from_dict, Token, prompt, Separator
            return prompt(self.get_questions(Separator('= The Rules ID =')))
        except ImportError:
            print('== The Rules ID ==')
            for rule in self.search_rules_id():
                print(rule['id_rule'] + r'\b')
            return None

    def get_questions(self, separator):
        rules = self.search_rules_id()
        questions = [{
            'type': 'checkbox',
            'message': 'Select rule(s)',
            'name': 'rules',
            'choices': [
                separator],
            'validate': (lambda answer: 'You must choose at least one topping.'
                         if len(answer) == 0 else True)
        }]
        for rule in rules:
            questions[0]['choices'].append(dict(name=rule['id_rule']))
        return questions

    def _get_wanted_rules(self):
        return [
            x for x in self.xml_parser.get_used_rules() if re.search(
                self.rule_name, x['id_rule'])]

    def _get_wanted_not_selected_rules(self):
        return [
            x for x in self.xml_parser.get_notselected_rules() if re.search(
                self.rule_name, x['id_rule'])]

    def search_rules_id(self):
        rules = self._get_wanted_rules()
        notselected_rules = self._get_wanted_not_selected_rules()
        if len(notselected_rules) and not rules:
            raise ValueError(
                'err- rule(s) "{}" was not selected, so there are no results.'
                .format(notselected_rules[0]['id_rule']))
        elif not notselected_rules and not rules:
            raise ValueError('err- 404 rule not found!')
        else:
            return rules

    def prepare_graphs(self, rules):
        try:
            for rule in rules['rules']:
                oval_tree = graph.oval_graph.build_nodes_form_xml(
                    self.source_filename, rule).to_sigma_dict(0, 0)
                with open('html_interpreter/data.js', "w+") as file:
                    file.write("var data_json =" + str(json.dumps(
                        oval_tree,
                        sort_keys=False,
                        indent=4) + ";"))
                self.open_web_browser()
                print('Rule "{}" done!'.format(rule))
        except Exception as error:
            raise ValueError('Rule: "{}" Error: "{}"'.format(rule, error))

    def open_web_browser(self):
        try:
            webbrowser.get('firefox').open_new_tab(
                'html_interpreter/index.html')
        except BaseException:
            webbrowser.open_new_tab('html_interpreter/index.html')

    def parse_arguments(self, args):
        parser = argparse.ArgumentParser(
            description='Client for visualization scanned rule from Security scan.')

        parser.add_argument("source_filename", help='ARF scan file')
        parser.add_argument(
            "rule_id", help=(
                'Rule ID to be visualized. You can input part of ID rule or'
                'use regular expresion,but if you use in regular expresion'
                'brackets. You must put regular expression betwen quotation marks.'))

        args = parser.parse_args(args)

        return args
