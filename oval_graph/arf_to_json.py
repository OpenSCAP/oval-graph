import json
import os

from .client import Client
from .exceptions import NotChecked
from .xml_parser import XmlParser


class ArfToJson(Client):
    def _set_attributes(self):
        self.show_failed_rules = self.arg.show_failed_rules
        self.show_not_selected_rules = self.arg.show_not_selected_rules
        self.xml_parser = XmlParser(self.source_filename)

    def _get_message(self):
        MESSAGES = {
            'description': 'Client for generating JSON of SCAP rule evaluation results',
            'source_filename': 'ARF scan file',
        }
        return MESSAGES

    def create_dict_of_rule(self, rule_id):
        return self.xml_parser.get_oval_tree(rule_id).save_tree_to_dict()

    def file_is_empty(self, path):
        return os.stat(path).st_size == 0

    def save_dict_as_json(self, dict_, src):
        if os.path.isfile(src) and not self.file_is_empty(src):
            with open(src, "r") as f:
                data = json.load(f)
                for key in data:
                    dict_[key] = data[key]
        with open(src, "w+") as f:
            json.dump(dict_, f)

    def prepare_data(self, rules):
        out = []
        rule = None
        out_oval_tree_dict = dict()
        for rule in rules['rules']:
            try:
                out_oval_tree_dict[self.START_OF_FILE_NAME + rule +
                                   self.date] = self.create_dict_of_rule(rule)
            except NotChecked as error:
                out_oval_tree_dict[self.START_OF_FILE_NAME + rule +
                                   self.date] = str(error)
        if self.out is not None:
            self.save_dict_as_json(out_oval_tree_dict, self.out)
            out.append(self.out)
        else:
            print(
                str(json.dumps(out_oval_tree_dict, sort_keys=False, indent=4)))
        return out

    def prepare_parser(self):
        super().prepare_parser()
        self.prepare_args_when_user_can_list_in_rules()
