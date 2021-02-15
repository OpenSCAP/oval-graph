from io import BytesIO

import lxml.html
from lxml import etree


class BuilderHtmlReport():

    def __init__(self, display_html, xml_parser, arf_file_src):
        self.display_html = display_html
        self.arf_file_src = arf_file_src
        self.src_xsl = xml_parser.get_src("schemas/xsl/xccdf-report.xsl")
        self.xslt_doc = etree.parse(self.src_xsl)
        self.xslt_transformer = etree.XSLT(self.xslt_doc)

        self.source_doc = etree.parse(self.arf_file_src)
        self.output_doc = self.xslt_transformer(self.source_doc)

    def _get_html_object(self):
        html_object = lxml.html.fromstring(str(self.output_doc))
        return html_object

    def _get_html(self):
        html_object = self._get_html_object()
        result = etree.tostring(
            html_object,
            xml_declaration=True,
            doctype=('<!DOCTYPE html>'),
            encoding='utf-8',
            standalone=False,
            with_tail=False,
            method='html',
            pretty_print=True)
        return BytesIO(result)

    def save_report(self, save_src):
        with open(save_src, 'wb+') as data_file:
            data_file.writelines(self._get_html())
        return [save_src]
