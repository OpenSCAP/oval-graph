import webbrowser
import json
import os
import shutil
import pprint
from datetime import datetime
import sys

from .converter import Converter
from .client import Client


class ArfToJson(Client):

    def run_gui_and_return_answers(self):
        try:
            if sys.stdout.isatty():
                import inquirer
                return inquirer.prompt(self.get_questions())
            else:
                return {'rules': [
                    rule['id_rule'] for rule in self.search_rules_id()]}
        except ImportError:
            print(self.get_selection_rules())
            return None

    def create_dict_of_rule(self, rule_id):
        return self.xml_parser.get_oval_tree(rule_id).save_tree_to_dict()

    def save_dict_as_json(self, dict_, src):
        with open(src + '.json', "w+") as f:
            json.dump(dict_, f)

    def prepare_data(self, rules):
        try:
            out = []
            out_oval_tree_dict = dict()
            for rule in rules['rules']:
                out_oval_tree_dict[rule] = self.create_dict_of_rule(rule)
                if self.out is not None:
                    src = self.get_save_src(rule)
                    self.save_dict_as_json(out_oval_tree_dict, src)
                    out.append(src)
            print(
                str(json.dumps(out_oval_tree_dict, sort_keys=False, indent=4)))
            return out
        except Exception as error:
            raise ValueError('Rule: "{}" Error: "{}"'.format(rule, error))
