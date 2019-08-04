var data_json ={
    "nodes": [
        {
            "id": "xccdf_org.ssgproject.content_rule_require_singleuser_auth",
            "label": "and",
            "url": "null",
            "text": "null",
            "title": "xccdf_org.ssgproject.content_rule_require_singleuser_auth",
            "x": 0,
            "y": 0,
            "size": 3,
            "color": "#00ff00"
        },
        {
            "id": "oval:ssg-require_singleuser_auth:def:1",
            "label": "and",
            "url": "null",
            "text": "null",
            "title": "oval:ssg-require_singleuser_auth:def:1",
            "x": 0,
            "y": 1,
            "size": 3,
            "color": "#00ff00"
        },
        {
            "id": "oval:ssg-test_require_rescue_service:tst:1",
            "label": "require_rescue_service",
            "url": "null",
            "text": "null",
            "title": "oval:ssg-test_require_rescue_service:tst:1",
            "x": -2,
            "y": 2.36,
            "size": 3,
            "color": "#00ff00"
        },
        {
            "id": "oval:ssg-test_require_rescue_service_runlevel1:tst:1",
            "label": "require_rescue_service_runlevel1",
            "url": "null",
            "text": "null",
            "title": "oval:ssg-test_require_rescue_service_runlevel1:tst:1",
            "x": -1,
            "y": 2,
            "size": 3,
            "color": "#00ff00"
        },
        {
            "id": "oval:ssg-test_no_custom_runlevel1_target:tst:1",
            "label": "no_custom_runlevel1_target",
            "url": "null",
            "text": "null",
            "title": "oval:ssg-test_no_custom_runlevel1_target:tst:1",
            "x": 0,
            "y": 2.36,
            "size": 3,
            "color": "#00ff00"
        },
        {
            "id": "oval:ssg-test_no_custom_rescue_service:tst:1",
            "label": "no_custom_rescue_service",
            "url": "null",
            "text": "null",
            "title": "oval:ssg-test_no_custom_rescue_service:tst:1",
            "x": 1,
            "y": 2,
            "size": 3,
            "color": "#00ff00"
        }
    ],
    "edges": [
        {
            "id": "c7a7f477-760c-4526-9e9e-982b40f5dcf9",
            "source": "xccdf_org.ssgproject.content_rule_require_singleuser_auth",
            "target": "oval:ssg-require_singleuser_auth:def:1"
        },
        {
            "id": "bcad6b9a-0b35-4a21-a9ff-1177fd7aaefe",
            "source": "oval:ssg-require_singleuser_auth:def:1",
            "target": "oval:ssg-test_require_rescue_service:tst:1"
        },
        {
            "id": "db55e891-6af4-4c0e-8def-5457a18d4745",
            "source": "oval:ssg-require_singleuser_auth:def:1",
            "target": "oval:ssg-test_require_rescue_service_runlevel1:tst:1"
        },
        {
            "id": "1371c102-08e3-4fd1-b870-bf9e82f58065",
            "source": "oval:ssg-require_singleuser_auth:def:1",
            "target": "oval:ssg-test_no_custom_runlevel1_target:tst:1"
        },
        {
            "id": "61009772-4c98-49b0-8f53-a8cd8a17a1ab",
            "source": "oval:ssg-require_singleuser_auth:def:1",
            "target": "oval:ssg-test_no_custom_rescue_service:tst:1"
        }
    ]
};