import tempfile
import time
import webbrowser
from pathlib import Path
from subprocess import PIPE, Popen, check_call

from ..exceptions import NotTestedRule
from ..html_builder.graph import Graph
from .client import Client

START_OF_FILE_NAME = 'graph-of-'


class ClientHtmlOutput(Client):
    def __init__(self, args):
        super().__init__(args)
        self.out = self.arg.output
        self.all_in_one = self.arg.all_in_one
        self.all_rules = True if self.all_in_one else self.arg.all
        self.display_html = True if self.out is None else self.arg.display
        self.html_builder = Graph(self.arg.verbose, self.all_in_one)
        self.web_browsers = []
        self.selected_only_one_rule = False

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
        if len(rules['rules']) == 1:
            self.selected_only_one_rule = True
        for rule in rules['rules']:
            try:
                self._put_to_dict_oval_trees(dict_oval_trees, rule)
                if not self.all_in_one:
                    path = self._get_src_for_one_graph(rule)
                    self.html_builder.save_html(dict_oval_trees, path)
                    paths_to_generated_rules.append(str(path))
                    dict_oval_trees = {}
            except NotTestedRule as error:
                start_red_color = '\033[91m'
                end_red_color = '\033[0m'
                message = '{}{}{}'.format(start_red_color, str(error), end_red_color)
                raise NotTestedRule(message) from error
        if self.all_in_one:
            path = self.get_save_src('rules' + self._get_date())
            self.html_builder.save_html(dict_oval_trees, path)
            paths_to_generated_rules.append(str(path))
        return paths_to_generated_rules

    def _get_src_for_one_graph(self, rule):
        return self.get_save_src(rule + self._get_date())

    @staticmethod
    def get_file_name(rule):
        return "{}{}.html".format(START_OF_FILE_NAME, rule)

    def get_save_src(self, rule):
        if self.out is not None:
            output_path = Path(self.out)
            if not output_path.is_dir():
                if (self.all_in_one and self.all_rules) or self.selected_only_one_rule:
                    return output_path
            return output_path / self.get_file_name(rule)
        return Path(tempfile.gettempdir()) / self.get_file_name(rule)

    def open_results_in_web_browser(self, paths_to_results):
        if self.display_html:
            try:
                for path_to_result in paths_to_results:
                    self._open_web_browser(path_to_result)
            except OSError as os_error:
                if os_error.errno != 24:
                    raise OSError from os_error
                error_msg = (
                    'Opening too many reports. Increase '
                    'the open file limit or try to use '
                    'the --all-in-one parameter')
                raise ResourceWarning(error_msg) from os_error

    @staticmethod
    def _is_firefox_installed():
        firefox_is_installed = True
        try:
            command = ['firefox', '--version']
            if check_call(command, stdout=PIPE, stderr=PIPE):
                firefox_is_installed = False
        except FileNotFoundError:
            firefox_is_installed = False
        return firefox_is_installed

    def _open_web_browser(self, path_to_result):
        is_firefox_installed = self._is_firefox_installed()
        if is_firefox_installed:
            command = ["firefox", path_to_result]
            browser = Popen(command, stdout=PIPE, stderr=PIPE)
            self.web_browsers.append(browser)
            time.sleep(0.2)
        else:
            default_web_browser_name = webbrowser.get().name
            command = [default_web_browser_name, path_to_result]
            browser = Popen(command, stdout=PIPE, stderr=PIPE)
            self.web_browsers.append(browser)
            time.sleep(0.2)

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
