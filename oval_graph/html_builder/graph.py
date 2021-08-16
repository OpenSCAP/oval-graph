import json
import re
import sys
from io import BytesIO
from pathlib import Path

from lxml import etree
from lxml.builder import E

LOCAL_DATA_DIR = Path(__file__).parent.parent / "parts"


class Graph():

    def __init__(self, verbose, all_in_one):
        self.verbose = verbose
        self.all_in_one = all_in_one
        self.html_head = self._get_html_head()
        self.script = self._get_part('script.js')
        self.search_bar = self._get_search_bar()

    def save_html(self, dict_oval_trees, path):
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wb+") as data_file:
            data_file.writelines(self._get_html(dict_oval_trees))
        if self.verbose:
            self.print_output_message(path, list(dict_oval_trees.keys()))

    def _get_html(self, dict_of_rules):
        html = E.html(
            self.html_head,
            self._get_html_body(dict_of_rules))
        result = etree.tostring(
            html,
            xml_declaration=True,
            doctype=('<!DOCTYPE html>'),
            encoding='utf-8',
            standalone=False,
            with_tail=False,
            method='html',
            pretty_print=True)
        return BytesIO(result)

    def _get_html_head(self):
        return E.head(
            E.meta(charset="utf-8"),
            E.title("OVAL TREE"),
            E.style(self._get_part('css.txt')),
            E.style(self._get_part('bootstrapStyle.txt')),
            E.style(self._get_part('jsTreeStyle.txt')),
            E.script(self._get_part('jQueryScript.txt')),
            E.script(self._get_part('bootstrapScript.txt')),
            E.script(self._get_part('jsTreeScript.txt')),
        )

    def _get_search_bar(self):
        if self.all_in_one:
            return E.div({'class': 'search'},
                         E.div({'class': 'form-group has-feedback has-search'},
                               E.span(
                                   {'class': 'glyphicon glyphicon-search form-control-feedback'}),
                               E.input({'id': 'Search',
                                        'onkeyup': 'search()',
                                        'class': 'form-control',
                                        'type': 'text',
                                        'placeholder': 'Search rule'})))
        return E.div()

    def _get_html_body(self, dict_of_rules):
        return E.body(
            E.script(self._get_data_of_graphs_in_js(dict_of_rules)),
            E.div(
                self.search_bar,
                self._get_titles_and_places_for_graph(dict_of_rules),
            ),
            E.div({'id': 'modal', 'class': 'modal'},
                  E.div({'class': 'modal-content'},
                        E.span({'id': 'close', 'class': 'close'}, '×'),
                        E.div({'id': 'content'}),
                        )
                  ),
            E.script(self.script),
        )

    @staticmethod
    def _remove_unfit_chars(string):
        return re.sub(r'[_\-\.]', '', string)

    def _get_data_of_graphs_in_js(self, dict_of_rules):
        json_of_graphs = {self._remove_unfit_chars(key): value
                          for key, value in dict_of_rules.items()}
        data = str(json.dumps(json_of_graphs))
        return "var data_of_tree = {};".format(data)

    def _get_titles_and_places_for_graph(self, dict_of_rules):
        rules_html = E.div({'id': 'graphs'})
        for rule in dict_of_rules.keys():
            rule_id_h1 = E.h1(rule)
            space_for_graph = E.div({'id': self._remove_unfit_chars(rule)})
            space_for_whole_rule = E.div({'class': 'target'}, rule_id_h1, space_for_graph)
            rules_html.append(space_for_whole_rule)
        return E.selection({'id': 'selection-content'}, rules_html)

    @staticmethod
    def _get_part(part):
        out = ''
        with open(LOCAL_DATA_DIR / part, "r") as data_file:
            out = ''.join(data_file.readlines())
        return out

    @staticmethod
    def print_output_message(src, rules):
        if len(rules) > 1:
            rule_names = "\n" + "\n".join(rules)
            print('Rules "{}" done!'.format(rule_names), file=sys.stderr)
        else:
            print('Rule "{}" done!'.format(rules.pop()), file=sys.stderr)
        print('Result is saved:"{}"'.format(src), file=sys.stderr)
