import json
import os
import re
import tempfile
import uuid
from pathlib import Path

import pytest

TOP_PATH = Path(__file__).parent


class TestTools():
    @staticmethod
    def find_files(file_name, search_path):
        result = []
        # root, directory, files
        for root, _, files in os.walk(search_path):
            for filename in files:
                if file_name in filename:
                    result.append(os.path.abspath(os.path.join(root, filename)))
        return result

    @staticmethod
    def get_text_file(src):
        path = TOP_PATH / src
        with open(path, 'r') as data:
            return data.readlines()

    @staticmethod
    def get_random_path_in_tmp():
        return Path(tempfile.gettempdir()) / str(uuid.uuid4())

    @staticmethod
    def compare_results_html(result):
        result_ = TestTools.get_text_file(result)
        reference_pattern = TestTools.get_text_file(
            'test_commands/test_data/referenc_pattern_html_report.txt')
        prefix_start = '<script>var data_of_tree = '
        prefix_end = ';</script><div>\n'
        data_in_html = ""
        matched = False
        for row in result_:
            if prefix_start in row and prefix_end in row:
                matched = True
                data_in_html = row
                break
        assert matched

        tmp_json_str = data_in_html.replace(prefix_start, '').replace(prefix_end, '')
        tmp_json = json.loads(tmp_json_str)
        data_in_html = prefix_start + json.dumps(tmp_json, indent=4, sort_keys=False) + prefix_end

        count_row = 0
        rule_name = 'xccdforgssgprojectcontentrulepackageabrtremoved'
        for row in reference_pattern:
            if row in data_in_html or rule_name in row:
                count_row += 1
        assert count_row == len(reference_pattern)

    @staticmethod
    def get_data_json(src):
        path = TOP_PATH / src
        with open(path, 'r') as data:
            return json.load(data)

    @staticmethod
    def compare_results_json(result):
        result = TestTools.get_data_json(result)
        reference_result = TestTools.get_data_json(
            'test_commands/test_data/referenc_result_data_json.json')
        rule_name = "xccdf_org.ssgproject.content_rule_package_abrt_removed"
        result_rule_name = [
            x for x in result.keys() if re.search(
                rule_name, x)]
        assert result[result_rule_name[0]] == reference_result[rule_name]

    @staticmethod
    def find_all_in_string(regex, count, string):
        assert len(re.findall(regex, string)) == count

    @staticmethod
    def get_questions_not_selected(capsys, client, result):
        out = client.get_questions()[0].choices
        assert out == result
        captured = capsys.readouterr()
        regex = r'rule_package_\w+_removed +\(Not selected\)'
        TestTools.find_all_in_string(regex, 6, captured.out)

    @staticmethod
    def get_questions_with_option_show_failed_rules(client):
        out = client.get_questions()[0].choices
        rule1 = 'xccdf_org.ssgproject.content_rule_package_abrt_removed'
        assert out[0] == rule1
        with pytest.raises(Exception, match="list index out of range"):
            assert out[2] is None

    @staticmethod
    def prepare_tree_test(client, rule):
        rules = {'rules': [rule]}
        results_src = client.prepare_data(rules)
        TestTools.compare_results_html(results_src[0])
        client.kill_web_browsers()
