from datetime import datetime


from .client import Client


class ArfToHtml(Client):
    def __init__(self, args):
        super().__init__(args)
        self.off_webbrowser = self.arg.off_web_browser
        self.show_fail_rules = self.arg.show_fail_rules
        self.show_not_selected_rules = self.arg.show_not_selected_rules

    def _get_message(self):
        MESSAGES = {
            'description': 'Client for visualization of SCAP rule evaluation results',
            '--output': 'The directory where to save output directory with files.',
            'source_filename': 'ARF scan file',
        }
        return MESSAGES

    def prepare_data(self, rules):
        try:
            out = []
            for rule in rules['rules']:
                oval_tree_dict = self.create_dict_of_rule(rule)
                src = self.get_save_src(rule)
                self.copy_interpreter(src)
                self.save_dict(oval_tree_dict, src)
                self.open_web_browser(src)
                print('Rule "{}" done!'.format(rule))
                out.append(src)
            return out
        except Exception as error:
            raise ValueError('Rule: "{}" Error: "{}"'.format(rule, error))

    def prepare_parser(self):
        super().prepare_parser()
        self.parser.add_argument(
            '--off-web-browser',
            action="store_true",
            default=False,
            help="It does not start the web browser.")
        self.parser.add_argument(
            '--show-fail-rules',
            action="store_true",
            default=False,
            help="Show only FAIL rules")
        self.parser.add_argument(
            '--show-not-selected-rules',
            action="store_true",
            default=False,
            help="Show notselected rules. These rules will not be visualized.")
