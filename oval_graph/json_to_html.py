import webbrowser
import json
import os
import argparse
from datetime import datetime
import shutil
import sys
import re

from .client import Client
from .oval_node import restore_dict_to_tree
from .converter import Converter
from .exceptions import NotChecked


class JsonToHtml(Client):
    def __init__(self, args):
        self.parser = None
        self.MESSAGES = self._get_message()
        self.arg = self.parse_arguments(args)
        self.hide_passing_tests = self.arg.hide_passing_tests
        self.source_filename = self.arg.source_filename
        self.rule_name = self.arg.rule_id
        self.out = self.arg.output
        self.all_in_one = self.arg.all_in_one
        self.all_rules = True if self.all_in_one else self.arg.all
        self.isatty = sys.stdout.isatty()
        self.show_failed_rules = False
        self.show_not_selected_rules = False
        self.oval_tree = None
        self.display_html = True if self.out is None else self.arg.display
        self.json_data_file = self.get_json_data_file()
        self.parts = self.get_src('parts')
        self.START_OF_FILE_NAME = 'graph-of-'
        self.date = datetime.now().strftime("-%d_%m_%Y-%H_%M_%S")
        self.verbose = self.arg.verbose

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
                raise ValueError(
                    'Used file "{}" is not valid json.'.format(
                        self.source_filename))

    def load_json_to_oval_tree(self, rule):
        dict_of_tree = self.json_data_file[rule]
        if isinstance(dict_of_tree, str):
            raise NotChecked(dict_of_tree)
        try:
            return restore_dict_to_tree(dict_of_tree)
        except Exception as error:
            raise ValueError('Data is not valid for OVAL tree.')

    def create_dict_of_oval_node(self, oval_node):
        converter = Converter(oval_node)
        return converter.to_JsTree_dict(self.hide_passing_tests)

    def load_rule_names(self):
        return self.json_data_file.keys()

    def search_rules_id(self):
        rules = self._get_wanted_rules_from_array_of_IDs(
            self.load_rule_names())
        notselected_rules = []
        return self._check_rules_id(rules, notselected_rules)

    def create_dict_of_rule(self, rule):
        self.oval_tree = self.load_json_to_oval_tree(rule)
        return self.create_dict_of_oval_node(self.oval_tree)

    def _put_to_dict_oval_trees(self, dict_oval_trees, rule):
        dict_oval_trees[rule.replace(
            self.START_OF_FILE_NAME, '')] = self.create_dict_of_rule(rule)

    def _get_src_for_one_graph(self, rule):
        return self.get_save_src(rule.replace(self.START_OF_FILE_NAME, ''))

    def prepare_parser(self):
        super().prepare_parser()
        self.parser.add_argument(
            '--all-in-one',
            action="store_true",
            default=False,
            help="Processes all rules into one file.")
        self.parser.add_argument(
            '--display',
            action="store_true",
            default=False,
            help="Enables opening a web browser with a graph, when is used --output.")
