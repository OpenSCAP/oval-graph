from ..converter import Converter
from .client_arf_input import ClientArfInput
from .client_html_output import ClientHtmlOutput


class ArfToHtml(ClientArfInput, ClientHtmlOutput):
    def __init__(self, args):
        super().__init__(args)
        self.hide_passing_tests = self.arg.hide_passing_tests

    def _get_message(self):
        return {
            'description': 'Client for visualization of SCAP rule evaluation results',
            'source_filename': 'ARF scan file',
        }

    def create_dict_of_rule(self, rule_id):
        converter = Converter(self.arf_xml_parser.get_oval_tree(rule_id))
        return converter.to_JsTree_dict(self.hide_passing_tests)

    def _put_to_dict_oval_trees(self, dict_oval_trees, rule):
        dict_oval_trees[rule] = self.create_dict_of_rule(rule)

    def prepare_parser(self, parser):
        super().prepare_parser(parser)
        self.prepare_args_when_output_is_html(parser)
        self.prepare_args_when_user_can_list_in_rules(parser)
