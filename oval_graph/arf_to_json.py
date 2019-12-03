import webbrowser
import json
import os
import shutil
import pprint
from datetime import datetime


from .converter import Converter
from .client import Client


class ArfToJson(Client):

    def create_dict_of_rule(self, rule_id):
        return self.xml_parser.get_oval_tree(rule_id).save_tree_to_dict()

    def save_dict_as_json(self, dict_, src):
        with open(src + '.json', "w+") as f:
            json.dump(dict_, f)

    def prepare_data(self, rules):
        try:
            out = []
            for rule in rules['rules']:
                oval_tree_dict = self.create_dict_of_rule(rule)
                if self.out is not None:
                    src = self.get_save_src(rule)
                    self.save_dict_as_json(oval_tree_dict, src)
                    out.append(src)
                else:
                    print(str(json.dumps(oval_tree_dict, sort_keys=False, indent=4)))
            return out
        except Exception as error:
            raise ValueError('Rule: "{}" Error: "{}"'.format(rule, error))
