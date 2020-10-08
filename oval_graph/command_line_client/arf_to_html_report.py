import uuid

from .._builder_html_report import BuilderHtmlReport
from .client_arf_input import ClientArfInput
from .client_html_output import ClientHtmlOutput


class ArfToHtmlReport(ClientArfInput, ClientHtmlOutput):
    def __init__(self, args):
        super().__init__(args)
        self.rule_name = '.'
        self.all_rules = True

    def _get_message(self):
        return {
            'description': 'Client for genretate of SCAP report from ARF file.',
            '--output': 'The directory where to save output directory with files.',
            'source_filename': 'ARF scan file',
        }

    @staticmethod
    def get_start_of_file_name():
        return 'report-'

    def _put_to_dict_oval_trees(self, dict_oval_trees, rule):
        """
        The function inserts into dict_oval_trees a dictionary from
        the rule with the key as the rule id.
        """
        raise NotImplementedError

    def prepare_data(self, rules):
        builder = BuilderHtmlReport(
            self.display_html,
            self.arf_xml_parser,
            self.source_filename)
        out_src = builder.save_report(
            self.get_save_src(str(uuid.uuid4())))
        self.open_results_in_web_browser(out_src)
        return out_src

    def prepare_parser(self, parser):
        self.args_basic_functions(parser)
        self.arg_display(parser)
        self.arg_source_file(parser)
