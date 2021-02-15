from ..converter import Converter
from ..oval_node import restore_dict_to_tree
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
            'description': 'Client for visualization of JSON created by command arf-to-json',
            'source_filename': 'JSON file',
        }

    def load_json_to_oval_tree(self, rule):
        dict_of_tree = self.json_data_file[rule]
        try:
            return restore_dict_to_tree(dict_of_tree)
        except Exception:
            raise ValueError('Data is not valid for OVAL tree.')

    def create_dict_of_oval_node(self, oval_node):
        converter = Converter(oval_node)
        return converter.to_JsTree_dict(self.hide_passing_tests)

    def create_dict_of_rule(self, rule):
        self.oval_tree = self.load_json_to_oval_tree(rule)
        return self.create_dict_of_oval_node(self.oval_tree)

    def _put_to_dict_oval_trees(self, dict_oval_trees, rule):
        dict_oval_trees[rule.replace(
            START_OF_FILE_NAME, '')] = self.create_dict_of_rule(rule)

    def _get_src_for_one_graph(self, rule):
        return self.get_save_src(rule.replace(START_OF_FILE_NAME, ''))

    def prepare_parser(self, parser):
        super().prepare_parser(parser)
        self.prepare_args_when_output_is_html(parser)
