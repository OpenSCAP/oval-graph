import webbrowser
import json
import os
import argparse
import shutil
from datetime import datetime


from .client import Client
from .oval_node import restore_dict_to_tree
from .converter import Converter


class JsonToHtml(Client):
    def __init__(self, args):
        self.parser = None
        self.arg = self.parse_arguments(args)
        self.off_webbrowser = self.arg.off_web_browser
        self.source_filename = self.arg.source_filename
        self.out = self.arg.output
        self.oval_tree = None

    def load_json_to_oval_tree(self, rule):
        with open(self.source_filename, 'r') as f:
            try:
                return restore_dict_to_tree(json.load(f)[rule])
            except Exception as error:
                raise ValueError("err- Used file is not json or valid.")

    def create_dict_of_oval_node(self, oval_node):
        converter = Converter(oval_node)
        return converter.to_JsTree_dict()

    def load_rule_names(self):
        with open(self.source_filename, 'r') as f:
            try:
                return json.load(f).keys()
            except Exception as error:
                raise ValueError("err- Used file is not json or valid.")

    def prepare_data(self):
        try:
            out = []
            for rule in self.load_rule_names():
                self.oval_tree = self.load_json_to_oval_tree(rule)
                rule_name = self.oval_tree.node_id
                oval_tree_dict = self.create_dict_of_oval_node(self.oval_tree)
                src = self.get_save_src(rule_name)
                self.copy_interpreter(src)
                self.save_dict(oval_tree_dict, src)
                self.open_web_browser(src)
                print('Rule "{}" done!'.format(rule_name))
                out.append(src)
            return out
        except Exception as error:
            raise ValueError(
                'Rule: "{}" Error: "{}"'.format(
                    self.source_filename, error))

    def prepare_parser(self):
        self.parser = argparse.ArgumentParser(
            description="Client for visualization of SCAP rule evaluation results")
        self.parser.add_argument(
            '--off-web-browser',
            action="store_true",
            default=False,
            help="It does not start the web browser.")
        self.parser.add_argument(
            '--output',
            action="store",
            default=None,
            help="Save the output files where it is defined.")
        self.parser.add_argument("source_filename", help="ARF scan file")
