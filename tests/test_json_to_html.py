import pytest
import tempfile
import os
import uuid

from oval_graph.json_to_html import JsonToHtml
import tests.any_test_help


def get_client_json_to_html(src):
    return JsonToHtml(
        ["--off-web-browser", tests.any_test_help.get_src(src)])


def get_client_json_to_html_with_define_dest(src):
    return JsonToHtml(
        ["--out", tests.any_test_help.get_src(
            os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))),
         "--off-web-browser",
         tests.any_test_help.get_src(src)])


def test_prepare_tree():
    src = 'test_data/referenc_result_data_json.json'
    client = get_client_json_to_html(src)
    results_src = client.prepare_data()
    tests.any_test_help.compare_results_js(results_src[0])


def test_prepare_tree_and_save_in_defined_destination():
    src = 'test_data/referenc_result_data_json.json'
    client = get_client_json_to_html_with_define_dest(src)
    results_src = client.prepare_data()
    tests.any_test_help.compare_results_js(results_src[0])
