import webbrowser
import json
import os
import argparse
import shutil
from datetime import datetime
import sys
import re
from .client import Client
from .oval_node import restore_dict_to_tree
from .converter import Converter


class JsonToHtml(Client):
    def __init__(self, args):
        self.parser = None
        self.MESSAGES = self._get_message()
        self.arg = self.parse_arguments(args)
        self.remove_pass_tests = self.arg.remove_pass_tests
        self.source_filename = self.arg.source_filename
        self.rule_name = self.arg.rule_id
        self.out = self.arg.output
        self.all_rules = self.arg.all
        self.isatty = sys.stdout.isatty()
        self.show_fail_rules = False
        self.show_not_selected_rules = False
        if self.remove_pass_tests:
            raise NotImplementedError('Not implemented!')
        self.oval_tree = None
        self.off_webbrowser = self.arg.off_web_browser
        self.json_data_file = self.get_json_data_file()

    def _get_message(self):
        MESSAGES = {
            'description': 'Client for visualization of JSON created by command arf-to-json',
            '--output': 'The directory where to save output directory with files.',
            'source_filename': 'JSON file',
        }
        return MESSAGES

    def get_json_data_file(self):
        with open(self.source_filename, 'r') as f:
            try:
                return json.load(f)
            except Exception as error:
                raise ValueError("err- Used file is not json or valid.")

    def load_json_to_oval_tree(self, rule):
        try:
            return restore_dict_to_tree(self.json_data_file[rule])
        except Exception as error:
            raise ValueError("err- Data is not valid for oval tree.")

    def create_dict_of_oval_node(self, oval_node):
        converter = Converter(oval_node)
        return converter.to_JsTree_dict()

    def load_rule_names(self):
        return self.json_data_file.keys()

    def get_rules_id(self):
        out = []
        for id in self.load_rule_names():
            out.append(dict(id_rule=id))
        return out

    def get_choices(self):
        rules = self.search_rules_id()
        choices = []
        for rule in rules:
            choices.append(rule['id_rule'])
        return choices

    def _get_wanted_rules(self):
        return [
            x for x in self.get_rules_id() if re.search(
                self.rule_name, x['id_rule'])]

    def _get_wanted_not_selected_rules(self):
        return []

    def prepare_data(self, rules):
        try:
            out = []
            for rule in rules["rules"]:
                self.oval_tree = self.load_json_to_oval_tree(rule)
                oval_tree_dict = self.create_dict_of_oval_node(self.oval_tree)
                src = self.get_save_src(rule.replace('graph-of-', '') + "-")
                self.copy_interpreter(src)
                self.save_dict(oval_tree_dict, src)
                self.open_web_browser(src)
                print('Rule "{}" done!'.format(rule))
                out.append(src)
            return out
        except Exception as error:
            raise ValueError(
                'Rule: "{}" Error: "{}"'.format(
                    self.source_filename, error))

    def prepare_parser(self):
        super().prepare_parser()
        self.parser.add_argument(
            '--off-web-browser',
            action="store_true",
            default=False,
            help="It does not start the web browser.")
