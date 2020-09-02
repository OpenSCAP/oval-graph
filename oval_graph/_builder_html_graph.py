import os
import webbrowser
import json
import re
import sys
from lxml import etree
from lxml.builder import ElementMaker, E
import lxml.html


class BuilderHtmlGraph():
    def __init__(self, parts, display_html, verbose):
        self.parts = parts
        self.display_html = display_html
        self.verbose = verbose

    def save_html_and_open_html(self, dict_oval_trees, src, rules, out):
        self.save_html_report(dict_oval_trees, src)
        self.print_output_message_and_open_web_browser(
            src, self._format_rules_output(rules), out)

    def save_html_report(self, dict_of_rules, src):
        with open(src, "w+") as data_file:
            data_file.writelines(self._get_html(dict_of_rules))

    def _get_html(self, dict_of_rules):
        maker = ElementMaker(namespace=None,
                             nsmap={None: "http://www.w3.org/1999/xhtml"})
        html = maker.html(
            self._get_html_head(),
            self._get_html_body(dict_of_rules))
        result = etree.tostring(
            html,
            xml_declaration=True,
            doctype=('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"'
                     ' "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">'),
            encoding='utf-8',
            standalone=False,
            with_tail=False,
            method='html',
            pretty_print=True)
        return result.decode('UTF-8')

    def _get_html_head(self):
        return E.head(
            E.title("OVAL TREE"),
            E.style(self._get_part('css.txt')),
            E.style(self._get_part('bootstrapStyle.txt')),
            E.style(self._get_part('jsTreeStyle.txt')),
            E.script(self._get_part('jQueryScript.txt')),
            E.script(self._get_part('bootstrapScript.txt')),
            E.script(self._get_part('jsTreeScript.txt')),
        )

    def _get_html_body(self, dict_of_rules):
        return E.body(
            E.script(self._get_script_graph_data(dict_of_rules)),
            self._get_titles_and_places_for_graph(dict_of_rules),
            E.div({'id': 'data'}),
            E.div({'id': 'modal', 'class': 'modal'},
                  E.div({'class': 'modal-content'},
                        E.span({'id': 'close', 'class': 'close'}, '×'),
                        E.div({'id': 'content'}),
                        )
                  ),
            E.script(self._get_part('script.js')),
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
        out = ''
        for rule in dict_of_rules.keys():
            out += ('<h1>' +
                    rule +
                    '</h1><div id="' +
                    re.sub(r'[\_\-\.]', '', rule) +
                    '"></div>')
        return lxml.html.fromstring(out)

    def _get_part(self, part):
        out = ''
        with open(os.path.join(self.parts, part), "r") as data_file:
            for line in data_file.readlines():
                out += line
        return out

    def print_output_message_and_open_web_browser(self, src, rule, out):
        if self.verbose:
            print('Rule(s) "{}" done!'.format(rule), file=sys.stderr)
        out.append(src)
        self.open_web_browser(src)

    def open_web_browser(self, src):
        if self.display_html:
            try:
                webbrowser.get('firefox').open_new_tab(src)
            except BaseException:
                webbrowser.open_new_tab(src)

    def _format_rules_output(self, rules):
        out = ''
        for rule in rules['rules']:
            out += rule + '\n'
        return out
