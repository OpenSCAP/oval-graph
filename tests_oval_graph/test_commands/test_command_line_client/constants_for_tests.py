from pathlib import Path

SEARCH_RULES = [
    ('xccdf_org.ssgproject.', 184),
    (r'_package_\w+_removed', 2),
    ('fips', 1),
    ('audit', 110),
    ('password', 15),
]

SEARCH_BAD_RULES = [
    ('non-existent_rule', '404'),
    ('xccdf_org.ssgproject.content_rule_package_nis_removed', 'notselected'),
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
PATH_TO_REPORT = TOP_PATH.parent.parent / "global_test_data/ssg-fedora-ds-arf.xml"
