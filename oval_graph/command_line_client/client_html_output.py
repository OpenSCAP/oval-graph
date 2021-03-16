import os
import subprocess
import tempfile
import webbrowser

from ..exceptions import NotChecked
from ..html_builder.graph import Graph
from .client import Client

START_OF_FILE_NAME = 'graph-of-'


class ClientHtmlOutput(Client):
    def __init__(self, args):
        super().__init__(args)
        self.out = self.arg.output
        self.part = self.get_src('../parts')
        self.all_in_one = self.arg.all_in_one
        self.all_rules = True if self.all_in_one else self.arg.all
        self.display_html = True if self.out is None else self.arg.display
        self.html_builder = Graph(self.part, self.arg.verbose, self.all_in_one)
        self.web_browsers = []

    @staticmethod
    def get_src(src):
        _dir = os.path.dirname(os.path.realpath(__file__))
        return str(os.path.join(_dir, src))

    def prepare_data(self, rules):
        paths_to_generated_rules = self._prepare_data(rules)
        self.open_results_in_web_browser(paths_to_generated_rules)
        return paths_to_generated_rules

    def _put_to_dict_oval_trees(self, dict_oval_trees, rule):
        """
        The function inserts into dict_oval_trees a dictionary from
        the rule with the key as the rule id.
        """
        raise NotImplementedError

    def _prepare_data(self, rules):
        dict_oval_trees = dict()
        paths_to_generated_rules = []
        for rule in rules['rules']:
            try:
                self._put_to_dict_oval_trees(dict_oval_trees, rule)
                if not self.all_in_one:
                    src = self._get_src_for_one_graph(rule)
                    self.html_builder.save_html(dict_oval_trees, src)
                    paths_to_generated_rules.append(src)
                    dict_oval_trees = {}
            except NotChecked as error:
                start_red_color = '\033[91m'
                end_red_color = '\033[0m'
                print(start_red_color + str(error) + end_red_color)
        if self.all_in_one:
            src = self.get_save_src('rules' + self._get_date())
            self.html_builder.save_html(dict_oval_trees, src)
            paths_to_generated_rules.append(src)
        return paths_to_generated_rules

    def _get_src_for_one_graph(self, rule):
        return self.get_save_src(rule + self._get_date())

    def get_save_src(self, rule):
        if self.out is not None:
            os.makedirs(self.out, exist_ok=True)
            return os.path.join(
                self.out,
                START_OF_FILE_NAME + rule + '.html')
        return os.path.join(
            tempfile.gettempdir(),
            START_OF_FILE_NAME + rule + '.html')

    def open_results_in_web_browser(self, paths_to_results):
        if self.display_html:
            try:
                self.web_browsers.append(
                    subprocess.Popen(["firefox", *paths_to_results]))
            except subprocess.CalledProcessError:
                default_web_browser_name = webbrowser.get().name
                self.web_browsers.append(
                    subprocess.Popen([default_web_browser_name, *paths_to_results]))

    def kill_web_browsers(self):
        for web_browser in self.web_browsers:
            web_browser.kill()

    @staticmethod
    def prepare_args_when_output_is_html(parser):
        parser.add_argument(
            '-i',
            '--all-in-one',
            action="store_true",
            default=False,
            help="Processes all rules into one file.")
        parser.add_argument(
            '-d',
            '--display',
            action="store_true",
            default=False,
            help="Enables opening a web browser with a graph, when is used --output.")
