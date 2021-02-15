import json
import os

from ..exceptions import NotChecked
from .client_arf_input import ClientArfInput


class ArfToJson(ClientArfInput):
    def __init__(self, args):
        super().__init__(args)
        self.out = self.arg.output

    def _get_message(self):
        return {
            'description': 'Client for generating JSON of SCAP rule evaluation results',
            'source_filename': 'ARF scan file',
        }

    def create_dict_of_rule(self, rule_id):
        return self.arf_xml_parser.get_oval_tree(rule_id).save_tree_to_dict()

    @staticmethod
    def file_is_empty(path):
        return os.stat(path).st_size == 0

    def save_dict_as_json(self, dict_, src):
        if os.path.isfile(src) and not self.file_is_empty(src):
            with open(src, "r") as file_:
                data = json.load(file_)
                for key in data:
                    dict_[key] = data[key]
        with open(src, "w+") as file_:
            json.dump(dict_, file_)

    def prepare_data(self, rules):
        out = []
        rule = None
        out_oval_tree_dict = dict()
        for rule in rules['rules']:
            try:
                out_oval_tree_dict[
                    rule + self._get_date()] = self.create_dict_of_rule(rule)
            except NotChecked as error:
                out_oval_tree_dict[
                    rule + self._get_date()] = str(error)
        if self.out is not None:
            self.save_dict_as_json(out_oval_tree_dict, self.out)
            out.append(self.out)
        else:
            print(
                str(json.dumps(out_oval_tree_dict, sort_keys=False, indent=4)))
        return out

    def prepare_parser(self, parser):
        super().prepare_parser(parser)
        self.prepare_args_when_user_can_list_in_rules(parser)
