import webbrowser
import json
import os
import shutil
from datetime import datetime


from .converter import Converter
from .client import Client


class ArfToHtml(Client):
    def __init__(self, args):
        super().__init__(args)
        self.off_webbrowser = self.arg.off_web_browser

    def create_dict_of_rule(self, rule_id):
        converter = Converter(self.xml_parser.get_oval_tree(rule_id))
        return converter.to_JsTree_dict()

    def save_dict(self, dict_, src):
        with open(os.path.join(src, 'data.js'), "w+") as data_file:
            data_file.write("var data_json =" + str(json.dumps(
                dict_, sort_keys=False, indent=4) + ";"))

    def copy_interpreter(self, dst):
        src = self.xml_parser.get_src('tree_html_interpreter')
        os.mkdir(dst)
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                shutil.copytree(s, d)
            else:
                shutil.copy2(s, d)

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

    def open_web_browser(self, src):
        if not self.off_webbrowser:
            src = os.path.join(src, 'index.html')
            try:
                webbrowser.get('firefox').open_new_tab(src)
            except BaseException:
                webbrowser.open_new_tab(src)

    def prepare_parser(self):
        super().prepare_parser()
        self.parser.add_argument(
            '--off-web-browser',
            action="store_true",
            default=False,
            help="It does not start the web browser.")
