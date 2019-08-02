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
            "x": -4,
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
            "x": -2,
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
            "x": 2,
            "y": 2,
            "size": 3,
            "color": "#00ff00"
        }
    ],
    "edges": [
        {
            "id": "728a4ff0-e176-4077-9c7d-9540ef8d324b",
            "source": "xccdf_org.ssgproject.content_rule_require_singleuser_auth",
            "target": "oval:ssg-require_singleuser_auth:def:1"
        },
        {
            "id": "28108091-48f0-4e58-9504-0f2067db5cb2",
            "source": "oval:ssg-require_singleuser_auth:def:1",
            "target": "oval:ssg-test_require_rescue_service:tst:1"
        },
        {
            "id": "8a1872fc-5324-4836-ac9c-62a0d6287482",
            "source": "oval:ssg-require_singleuser_auth:def:1",
            "target": "oval:ssg-test_require_rescue_service_runlevel1:tst:1"
        },
        {
            "id": "889008c9-e86d-4224-9a41-7b582fa1c930",
            "source": "oval:ssg-require_singleuser_auth:def:1",
            "target": "oval:ssg-test_no_custom_runlevel1_target:tst:1"
        },
        {
            "id": "4ec9d4d7-85bc-47e3-bcb8-5456e613ed5e",
            "source": "oval:ssg-require_singleuser_auth:def:1",
            "target": "oval:ssg-test_no_custom_rescue_service:tst:1"
        }
    ]
};