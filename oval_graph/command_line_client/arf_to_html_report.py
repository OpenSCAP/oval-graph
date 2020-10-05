from .client import Client


class ArfToHtmlReport(Client):
    def __init__(self, args):
        super().__init__(args)
        self.rule_name = '.'

    def _get_message(self):
        return {
            'description': 'Client for genretate of SCAP report from ARF file.',
            '--output': 'The directory where to save output directory with files.',
            'source_filename': 'ARF scan file',
        }

    def prepare_data(self, rules):
        src = ""
        """
        self.verbose
        self.display_html
        self.out
        self.source_filename
        """
        return src

    def prepare_parser(self, parser):
        self.args_basic_functions(parser)
        self.arg_display(parser)
        self.arg_source_file(parser)
