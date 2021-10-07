from ..oval_tree.builder import Builder
from ..oval_tree.converter import Converter
from .client_html_output import ClientHtmlOutput
from .client_json_input import ClientJsonInput

START_OF_FILE_NAME = 'graph-of-'


class JsonToHtml(ClientHtmlOutput, ClientJsonInput):
    def __init__(self, args):
        super().__init__(args)
        self.hide_passing_tests = self.arg.hide_passing_tests
        self.oval_tree = None

    def get_only_fail_rule(self, rules):
        """
        Function processes array of matched IDs of rules in selected file.
        Function retunes array of failed matched IDs of rules in selected file.
        """
        raise NotImplementedError

    def _get_rows_of_unselected_rules(self):
        """
        Function retunes array of rows where is not selected IDs of rules in selected file.
        """
        raise NotImplementedError

    def _get_message(self):
        return {
            'command_name': 'json-to-graph',
            'description': 'Client for visualization of JSON created by command arf-to-json',
            'source_filename': 'JSON file',
        }

    def load_json_to_oval_tree(self, rule):
        dict_of_tree = self.json_data_file[rule]
        try:
            return Builder.dict_to_oval_tree(dict_of_tree)
        except Exception as error:
            raise ValueError('Data is not valid for OVAL tree.') from error

    def create_dict_of_rule(self, rule):
        self.oval_tree = self.load_json_to_oval_tree(rule)
        converter = Converter(self.oval_tree)
        return converter.to_js_tree_dict(self.hide_passing_tests)

    @staticmethod
    def _get_rule_id(rule):
        return rule.replace(START_OF_FILE_NAME, '')

    def _put_to_dict_oval_trees(self, dict_oval_trees, rule):
        dict_oval_trees[self._get_rule_id(rule)] = self.create_dict_of_rule(rule)

    def _get_src_for_one_graph(self, rule):
        return self.get_save_src(self._get_rule_id(rule))

    def prepare_parser(self, parser):
        super().prepare_parser(parser)
        self.prepare_args_when_output_is_html(parser)
