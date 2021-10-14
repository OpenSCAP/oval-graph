import argparse
import re
import sys
from datetime import datetime

from .. import __version__


class Client():
    def __init__(self, args):
        self.arg = self.parse_arguments(args)

        self.source_filename = self.arg.source_filename
        self.rule_name = self.arg.rule_id

        self.isatty = sys.stdout.isatty()

        self.all_rules = self.arg.all
        self.show_failed_rules = False
        self.show_not_selected_rules = False
        self.show_not_tested_rules = False

        self.verbose = self.arg.verbose

    @staticmethod
    def _get_message():
        return {
            'command_name': '',
            'description': '',
            'source_filename': '',
        }

    @staticmethod
    def _get_date():
        return str(datetime.now().strftime("-%d_%m_%Y-%H_%M_%S"))

    # Functions for selection of rules

    def search_rules_id(self):
        """
        Function returns array of all matched IDs of rules in selected file.
        """
        raise NotImplementedError

    def get_only_fail_rule(self, rules):
        """
        Function processes array of matched IDs of rules in selected file.
        Function returns array of failed matched IDs of rules in selected file.
        """
        raise NotImplementedError

    def _get_rows_of_unselected_rules(self):
        """
        Function returns array of rows where is not selected IDs of rules in selected file.
        """
        raise NotImplementedError

    def load_file(self):
        """
        Function returns parser or data.
        """
        raise NotImplementedError

    def _get_rows_not_visualizable_rules(self):
        """
        Function returns array of rows where is not selected IDs of rules in selected file.
        """
        raise NotImplementedError

    def run_gui_and_return_answers(self):
        if self.isatty:
            if self.all_rules:
                return self._get_rules()

            print(self.get_selection_rules())
            return None
        return self._get_rules()

    def _get_rules(self):
        rules = self.search_rules_id()
        if self.show_failed_rules:
            return {'rules': self.get_only_fail_rule(rules)}
        return {'rules': rules}

    def _get_list_of_matched_rules(self):
        rules = self.search_rules_id()
        if self.show_failed_rules:
            return self.get_only_fail_rule(rules)
        return rules

    def _get_list_of_lines(self):
        lines = ['== The Rule ID regular expressions ==']
        for rule in self._get_list_of_matched_rules():
            lines.append("^" + rule + "$")
        if self.show_not_selected_rules and not self.show_not_tested_rules:
            for line in self._get_rows_of_unselected_rules():
                lines.append(line)
        if not self.show_not_selected_rules and self.show_not_tested_rules:
            for line in self._get_rows_not_visualizable_rules():
                lines.append(line)
        lines.append(
            " Copy id of the rule you want to visualize and"
            " paste it into a command with regular"
            " expression characters(^$).\n"
            "Alternatively, use the --all or --all-in-one arguments.")
        return lines

    def get_selection_rules(self):
        return "\n".join(self._get_list_of_lines())

    def _get_choices(self):
        if self.show_not_selected_rules and not self.show_not_tested_rules:
            print("\n".join(self._get_rows_of_unselected_rules()))
        if not self.show_not_selected_rules and self.show_not_tested_rules:
            print("\n".join(self._get_rows_not_visualizable_rules()))
        return self._get_list_of_matched_rules()

    def _get_wanted_rules(self, rules):
        return [
            x for x in rules if re.search(
                self.rule_name, x)]

    # Function for setting arguments

    def parse_arguments(self, args):
        parser = argparse.ArgumentParser(
            prog=self._get_message().get('command_name'),
            description=self._get_message().get('description'))
        self.prepare_parser(parser)
        if args is None:
            return parser.parse_args()
        return parser.parse_args(args)

    @staticmethod
    def prepare_args_when_user_can_list_in_rules(parser):
        parser.add_argument(
            '--show-failed-rules',
            action="store_true",
            default=False,
            help="Show only FAILED rules")
        parser.add_argument(
            '--show-not-selected-rules',
            action="store_true",
            default=False,
            help="Show notselected rules. These rules will not be visualized.")
        parser.add_argument(
            '--show-not-tested-rules',
            action="store_true",
            default=False,
            help="Shows rules which weren't tested. These rules will not be visualized.")

    def prepare_parser(self, parser):
        parser.add_argument(
            '--version',
            action='version',
            version='%(prog)s ' + __version__)
        parser.add_argument(
            '-a',
            '--all',
            action="store_true",
            default=False,
            help="Process all matched rules.")
        parser.add_argument(
            '--hide-passing-tests',
            action="store_true",
            default=False,
            help=(
                "Do not display passing tests for better orientation in"
                " graphs that contain a large amount of nodes."))
        parser.add_argument(
            '-v',
            '--verbose',
            action="store_true",
            default=False,
            help="Displays details about the results of the running command.")
        parser.add_argument(
            '-o',
            '--output',
            action="store",
            default=None,
            help=("The path where to save the output. If there are more report "
                  "files to generate it will create an OUTPUT path as a directory."))
        parser.add_argument(
            "source_filename",
            help=self._get_message().get('source_filename'))
        parser.add_argument(
            "rule_id", help=(
                "Rule ID to be visualized. A part from the full rule ID"
                " a part of the ID or a regular expression can be used."
                " If brackets are used in the regular expression "
                "the regular expression must be quoted."))
