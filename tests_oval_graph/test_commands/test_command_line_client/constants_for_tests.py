from pathlib import Path

from oval_graph.exceptions import NotTestedRule

SEARCH_RULES = [
    ('xccdf_org.ssgproject.', 184),
    (r'_package_\w+_removed', 2),
    ('fips', 1),
    ('audit', 110),
    ('password', 15),
]

SEARCH_BAD_RULES = [
    ('non-existent_rule', '404', ValueError),
    ('xccdf_org.ssgproject.content_rule_package_nis_removed', 'notselected', NotTestedRule),
]

EXPECTED_RULES_ID = [
    'xccdf_org.ssgproject.content_rule_package_abrt_removed',
    'xccdf_org.ssgproject.content_rule_package_sendmail_removed'
]

EXPECTED_RULES_ID_WITH_ARGS = [
    (
        ["--show-not-selected-rules"],
        EXPECTED_RULES_ID,
    ),
    (
        ["--show-not-selected-rules", "--show-failed-rules"],
        [EXPECTED_RULES_ID[0]],
    ),
]

TOP_PATH = Path(__file__).parent
PATH_TO_ARF_REPORT = TOP_PATH.parent.parent / "global_test_data/ssg-fedora-ds-arf.xml"
PATH_TO_JSON_REPORT = TOP_PATH.parent / "test_data/referenc_result_data_json.json"
PATH_TO_EMPTY_FILE = TOP_PATH.parent / "test_data/empty_file.json"
PATH_TO_REFERENCE_RESULT_JSON = TOP_PATH.parent / "test_data/referenc_result_data_json.json"
PATH_TO_REFERENCE_RESULT_HTML = TOP_PATH.parent / "test_data/referenc_html_report.html"
PATH_TO_BAD_RESULT_JSON = TOP_PATH.parent / "test_data/bad_result_data_json.json"
