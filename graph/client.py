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
        self.remove_pass_tests = self.arg.remove_pass_tests
        self.show_fail_rules = self.arg.show_fail_rules
        self.show_not_selected_rules = self.arg.show_not_selected_rules
        self.off_webbrowser = self.arg.off_web_browser
        self.source_filename = self.arg.source_filename
        self.tree = self.arg.tree
        self.rule_name = self.arg.rule_id
        self.xml_parser = graph.xml_parser.xml_parser(self.source_filename)
        if self.tree:
            self.src_html_interpreter='tree_html_interpreter/index.html'
        else: 
            self.src_html_interpreter='graph_html_interpreter/index.html'
        if self.remove_pass_tests:
            raise NotImplementedError('Not implemented!')

    def run_gui_and_return_answers(self):
        try:
            from PyInquirer import style_from_dict, Token, prompt, Separator
            return prompt(
                self.get_questions(
                    Separator('= The Rules IDs ='),
                    Separator('= The not selected rule IDs =')))
        except ImportError:
            print('== The Rule IDs ==')
            rules = self.search_rules_id()
            if self.show_fail_rules:
                rules = self.get_only_fail_rule(rules)
            for rule in rules:
                print(rule['id_rule'] + r'\b')
            if self.show_not_selected_rules:
                print('== The not selected rule IDs ==')
                for rule in self._get_wanted_not_selected_rules():
                    print(rule['id_rule'] + '(Not selected)')
            return None

    def get_questions(
            self,
            separator_rule_ids,
            separator_not_selected_rule_ids):
        rules = self.search_rules_id()
        if self.show_fail_rules:
            rules = self.get_only_fail_rule(rules)
        questions = [{
            'type': 'checkbox',
            'message': 'Select rule(s)',
            'name': 'rules',
            'choices': [separator_rule_ids]
        }]
        for rule in rules:
            questions[0]['choices'].append(dict(name=rule['id_rule']))
        if self.show_not_selected_rules:
            questions[0]['choices'].append(separator_not_selected_rule_ids)
            for rule in self._get_wanted_not_selected_rules():
                questions[0]['choices'].append(
                    dict(name=rule['id_rule'], disabled='Not selected'))
        return questions

    def get_only_fail_rule(self, rules):
        return list(filter(lambda rule: rule['result'] == 'fail', rules))

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
                ('err- rule(s) "{}" was not selected, '
                 'so there are no results. The rule is'
                 ' "notselected" because it'
                 " wasn't a part of the executed profile"
                 " and therefore it wasn't evaluated "
                 "during the scan.")
                .format(notselected_rules[0]['id_rule']))
        elif not notselected_rules and not rules:
            raise ValueError('err- 404 rule not found!')
        else:
            return rules

    def prepare_data(self, rules):
        try:
            for rule in rules['rules']:
                if self.tree:
                    oval_tree = graph.oval_graph.build_nodes_form_xml(
                        self.source_filename, rule).to_JsTree_dict()
                    with open('tree_html_interpreter/data.js', "w+") as file:
                        file.write("var data_json =" + str(json.dumps(
                            oval_tree,
                            sort_keys=False,
                            indent=4) + ";"))
                else:
                    oval_tree = graph.oval_graph.build_nodes_form_xml(
                        self.source_filename, rule).to_sigma_dict(0, 0)
                    with open('graph_html_interpreter/data.js', "w+") as file:
                        file.write("var data_json =" + str(json.dumps(
                            oval_tree,
                            sort_keys=False,
                            indent=4) + ";"))
                self.open_web_browser()
                print('Rule "{}" done!'.format(rule))
        except Exception as error:
            raise ValueError('Rule: "{}" Error: "{}"'.format(rule, error))

    def open_web_browser(self):
        if not self.off_webbrowser:
            try:
                webbrowser.get('firefox').open_new_tab(self.src_html_interpreter)                
            except BaseException:
                webbrowser.open_new_tab(self.src_html_interpreter)

    def parse_arguments(self, args):
        parser = argparse.ArgumentParser(
            description='Client for visualization of SCAP rule evaluation results')
        parser.add_argument(
            '--show-fail-rules',
            action="store_true",
            default=False,
            help='Show only FAIL rules')
        parser.add_argument(
            '--show-not-selected-rules',
            action="store_true",
            default=False,
            help="Show notselected rules. These rules will not be visualized.")
        parser.add_argument(
            '--off-web-browser',
            action="store_true",
            default=False,
            help="It does not start the web browser.")
        parser.add_argument(
            '--tree',
            action="store_true",
            default=False,
            help=("Switch graph_html_interpreter to tree_html_interpreter."
                  " Rule will interpret as directory tree."))
        parser.add_argument(
            '--remove-pass-tests',
            action="store_true",
            default=False,
            help=(
                'Do not display passing tests for better orientation in'
                ' graphs that contain a large amount of nodes.(Not implemented)'))
        parser.add_argument("source_filename", help='ARF scan file')
        parser.add_argument(
            "rule_id", help=(
                'Rule ID to be visualized. A part from the full rule ID'
                ' a part of the ID or a regular expression can be used.'
                ' If brackets are used in the regular expression '
                'the regular expression must be quoted.'))
        args = parser.parse_args(args)

        return args
