import json
import os
import re
import sys
from io import BytesIO

import lxml.html
from lxml import etree
from lxml.builder import E, ElementMaker


class Graph():

    def __init__(self, parts, verbose, all_in_one):
        self.parts = parts
        self.verbose = verbose
        self.all_in_one = all_in_one
        self.html_head = self._get_html_head()
        self.script = self._get_part('script.js')
        self.search_bar = self._get_search_bar()

    def save_html(self, dict_oval_trees, src):
        with open(src, "wb+") as data_file:
            data_file.writelines(self._get_html(dict_oval_trees))
        if self.verbose:
            self.print_output_message(src, list(dict_oval_trees.keys()))

    def _get_html(self, dict_of_rules):
        maker = ElementMaker()
        html = maker.html(
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
            E.script(self._get_script_graph_data(dict_of_rules)),
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

    def _get_script_graph_data(self, dict_of_rules):
        json_of_graphs = {
            re.sub(
                r'[\_\-\.]',
                '',
                k): v for k,
            v in dict_of_rules.items()}
        return ("var data_of_tree = " +
                str(json.dumps(json_of_graphs, sort_keys=False, indent=4)) +
                ";")

    def _get_titles_and_places_for_graph(self, dict_of_rules):
        out = '<section id="selection-content"><div id="graphs">'
        for rule in dict_of_rules.keys():
            out += ('<div class="target"><h1>' +
                    rule +
                    '</h1><div id="' +
                    re.sub(r'[\_\-\.]', '', rule) +
                    '"></div></div>')
        out += '</div>'
        return lxml.html.fromstring(out)

    def _get_part(self, part):
        out = ''
        with open(os.path.join(self.parts, part), "r") as data_file:
            for line in data_file.readlines():
                out += line
        return out

    @staticmethod
    def print_output_message(src, rules):
        if len(rules) > 1:
            rule_names = "\n" + "\n".join(rules)
            print('Rules "{}" done!'.format(rule_names), file=sys.stderr)
        else:
            print('Rule "{}" done!'.format(rules.pop()), file=sys.stderr)
        print('Result is saved:"{}"'.format(src), file=sys.stderr)
