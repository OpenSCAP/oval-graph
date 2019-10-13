from __future__ import print_function, unicode_literals
from datetime import datetime
import re
import oval_graph.xml_parser
import oval_graph.oval_graph
import oval_graph.converter
import webbrowser
import json
import argparse
import tempfile
import os
import shutil


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
        self.xml_parser = oval_graph.xml_parser.xml_parser(
            self.source_filename)
        if self.tree:
            self.html_interpreter = 'tree_html_interpreter'
        else:
            self.html_interpreter = 'graph_html_interpreter'
        if self.remove_pass_tests:
            raise NotImplementedError('Not implemented!')

    def run_gui_and_return_answers(self):
        try:
            import inquirer
            return inquirer.prompt(self.get_questions())
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

    def get_questions(self):
        rules = self.search_rules_id()
        if self.show_fail_rules:
            rules = self.get_only_fail_rule(rules)
        choices_ = []
        for rule in rules:
            choices_.append(rule['id_rule'])
        if self.show_not_selected_rules:
            print('== The not selected rule IDs ==')
            for rule in self._get_wanted_not_selected_rules():
                print(rule['id_rule'] + '(Not selected)')
        from inquirer.questions import Checkbox as checkbox
        questions = [
            checkbox(
                'rules',
                message=(
                    "= The Rules IDs = (move - UP and DOWN arrows,"
                    " select - SPACE or LEFT and RIGHT arrows, submit - ENTER)"),
                choices=choices_,
            ),
        ]
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
                 "so there are no results. The rule is"
                 ' "notselected" because it'
                 " wasn't a part of the executed profile"
                 " and therefore it wasn't evaluated "
                 "during the scan.")
                .format(notselected_rules[0]['id_rule']))
        elif not notselected_rules and not rules:
            raise ValueError('err- 404 rule not found!')
        else:
            return rules

    def create_dict_of_rule(self, rule_id):
        converter = oval_graph.converter.converter(
            oval_graph.oval_graph.build_nodes_form_xml(
                self.source_filename, rule_id))
        if self.tree:
            return converter.to_JsTree_dict()
        return converter.to_sigma_dict(0, 0)

    def save_dict(self, dict_, name_dir):
        with open(os.path.join(
                tempfile.gettempdir(),
                'graph-of-' + name_dir, 'data.js'), "w+") as data_file:
            data_file.write("var data_json =" + str(json.dumps(
                dict_, sort_keys=False, indent=4) + ";"))

    def copy_interpreter(self, name_dir):
        src = self.xml_parser.get_src(self.html_interpreter)
        dst = os.path.join(tempfile.gettempdir(), 'graph-of-' + name_dir)
        os.mkdir(dst)
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                shutil.copytree(s, d)
            else:
                shutil.copy2(s, d)

    def prepare_data(self, rules):
        try:
            date = str(datetime.now().strftime("_%d-%m-%Y_%H:%M:%S"))
            for rule in rules['rules']:
                oval_tree = self.create_dict_of_rule(rule)
                tempfile.gettempdir()
                date = str(datetime.now().strftime("_%d-%m-%Y_%H:%M:%S"))
                name_dir = rule + date
                self.copy_interpreter(name_dir)
                self.save_dict(oval_tree, name_dir)
                self.open_web_browser(name_dir)
                print('Rule "{}" done!'.format(rule))
            return date
        except Exception as error:
            raise ValueError('Rule: "{}" Error: "{}"'.format(rule, error))

    def open_web_browser(self, name_dir):
        if not self.off_webbrowser:
            src = os.path.join(
                tempfile.gettempdir(),
                'graph-of-' + name_dir,
                'index.html')
            try:
                webbrowser.get('firefox').open_new_tab(src)
            except BaseException:
                webbrowser.open_new_tab(src)

    def parse_arguments(self, args):
        parser = argparse.ArgumentParser(
            description="Client for visualization of SCAP rule evaluation results")
        parser.add_argument(
            '--show-fail-rules',
            action="store_true",
            default=False,
            help="Show only FAIL rules")
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
            help="Render the graph in a form of directory tree")
        parser.add_argument(
            '--remove-pass-tests',
            action="store_true",
            default=False,
            help=(
                "Do not display passing tests for better orientation in"
                " graphs that contain a large amount of nodes.(Not implemented)"))
        parser.add_argument("source_filename", help="ARF scan file")
        parser.add_argument(
            "rule_id", help=(
                "Rule ID to be visualized. A part from the full rule ID"
                " a part of the ID or a regular expression can be used."
                " If brackets are used in the regular expression "
                "the regular expression must be quoted."))
        args = parser.parse_args(args)

        return args
