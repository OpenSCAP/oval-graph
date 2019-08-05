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
            "id": "0360b2c7-8467-42e5-8175-214cd9f95209",
            "source": "xccdf_org.ssgproject.content_rule_require_singleuser_auth",
            "target": "oval:ssg-require_singleuser_auth:def:1"
        },
        {
            "id": "18b82536-781e-416b-9c92-9aeb8d2821f9",
            "source": "oval:ssg-require_singleuser_auth:def:1",
            "target": "oval:ssg-test_require_rescue_service:tst:1"
        },
        {
            "id": "3dfc4900-5695-4168-b5ca-944116e7a5fa",
            "source": "oval:ssg-require_singleuser_auth:def:1",
            "target": "oval:ssg-test_require_rescue_service_runlevel1:tst:1"
        },
        {
            "id": "127ada56-bd57-477b-9aab-44c25056743f",
            "source": "oval:ssg-require_singleuser_auth:def:1",
            "target": "oval:ssg-test_no_custom_runlevel1_target:tst:1"
        },
        {
            "id": "2cd85a8a-f394-43cb-841d-0de9a38850d7",
            "source": "oval:ssg-require_singleuser_auth:def:1",
            "target": "oval:ssg-test_no_custom_rescue_service:tst:1"
        }
    ]
};