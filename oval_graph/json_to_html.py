import json

from .client import Client
from .oval_node import restore_dict_to_tree
from .converter import Converter
from .exceptions import NotChecked
from ._builder_html_graph import BuilderHtmlGraph


class JsonToHtml(Client):
    def __init__(self, args):
        super().__init__(args)
        self.json_data_file = self.get_json_data_file()
        self.oval_tree = None

    def _set_attributes(self):
        self.all_in_one = self.arg.all_in_one
        self.all_rules = True if self.all_in_one else self.arg.all
        self.display_html = True if self.out is None else self.arg.display
        self.html_builder = BuilderHtmlGraph(self.parts, self.verbose, self.all_in_one)

    def _get_message(self):
        MESSAGES = {
            'description': 'Client for visualization of JSON created by command arf-to-json',
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
        self.prepare_args_when_output_is_html()
