import re
import argparse
import tempfile
import os
import json
import shutil
from datetime import datetime

from .xml_parser import XmlParser
from .converter import Converter


class Client():
    def __init__(self, args):
        self.parser = None
        self.arg = self.parse_arguments(args)
        self.remove_pass_tests = self.arg.remove_pass_tests
        self.show_fail_rules = self.arg.show_fail_rules
        self.show_not_selected_rules = self.arg.show_not_selected_rules
        self.source_filename = self.arg.source_filename
        self.rule_name = self.arg.rule_id
        self.out = self.arg.out
        self.xml_parser = XmlParser(
            self.source_filename)
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
                rules = self._get_only_fail_rule(rules)
            for rule in rules:
                print(rule['id_rule'] + r'\b')
            if self.show_not_selected_rules:
                print('== The not selected rule IDs ==')
                for rule in self._get_wanted_not_selected_rules():
                    print(rule['id_rule'] + '(Not selected)')
            print("You haven't got installed inquirer lib. "
                  "Please copy id rule with you want use and put it in command")
            return None

    def get_questions(self):
        rules = self.search_rules_id()
        if self.show_fail_rules:
            rules = self._get_only_fail_rule(rules)
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

    def _get_only_fail_rule(self, rules):
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
        parser = XmlParser(self.source_filename)
        converter = Converter(parser.get_oval_tree(rule_id))
        return converter.to_JsTree_dict()

    def save_dict(self, dict_, src):
        with open(os.path.join(src, 'data.js'), "w+") as data_file:
            data_file.write("var data_json =" + str(json.dumps(
                dict_, sort_keys=False, indent=4) + ";"))

    def copy_interpreter(self, dst):
        src = self.XmlParser.get_src(self.html_interpreter)
        os.mkdir(dst)
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                shutil.copytree(s, d)
            else:
                shutil.copy2(s, d)

    def get_save_src(self, rule):
        date = str(datetime.now().strftime("_%d-%m-%Y_%H:%M:%S"))
        if self.out is not None:
            if not os.path.isdir(self.out):
                os.mkdir(self.out)
                return os.path.join(self.out, 'graph-of-' + rule + date)
            return os.path.join(
                self.out,
                'graph-of-' + rule + date)
        return os.path.join(
            tempfile.gettempdir(),
            'graph-of-' + rule + date)

    def parse_arguments(self, args):
        self.prepare_parser()
        args = self.parser.parse_args(args)
        return args

    def prepare_parser(self):
        self.parser = argparse.ArgumentParser(
            description="Client for visualization of SCAP rule evaluation results")
        self.parser.add_argument(
            '--show-fail-rules',
            action="store_true",
            default=False,
            help="Show only FAIL rules")
        self.parser.add_argument(
            '--show-not-selected-rules',
            action="store_true",
            default=False,
            help="Show notselected rules. These rules will not be visualized.")
        self.parser.add_argument(
            '--out',
            action="store",
            default=None,
            help="The directory where to save output files.")
        self.parser.add_argument(
            '--remove-pass-tests',
            action="store_true",
            default=False,
            help=(
                "Do not display passing tests for better orientation in"
                " graphs that contain a large amount of nodes.(Not implemented)"))
        self.parser.add_argument("source_filename", help="ARF scan file")
        self.parser.add_argument(
            "rule_id", help=(
                "Rule ID to be visualized. A part from the full rule ID"
                " a part of the ID or a regular expression can be used."
                " If brackets are used in the regular expression "
                "the regular expression must be quoted."))
