var data_json ={
    "nodes": [
        {
            "id": "xccdf_org.ssgproject.content_rule_require_singleuser_auth",
            "label": "and",
            "url": "null",
            "text": "null",
            "title": "xccdf_org.ssgproject.content_rule_require_singleuser_auth",
            "x": -6,
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
            "x": -6,
            "y": 1,
            "size": 3,
            "color": "#00ff00"
        },
        {
            "id": "oval:ssg-test_require_rescue_service:tst:1",
            "label": "true",
            "url": "null",
            "text": "null",
            "title": "oval:ssg-test_require_rescue_service:tst:1",
            "x": -4,
            "y": 3,
            "size": 3,
            "color": "#00ff00"
        },
        {
            "id": "oval:ssg-test_require_rescue_service_runlevel1:tst:1",
            "label": "true",
            "url": "null",
            "text": "null",
            "title": "oval:ssg-test_require_rescue_service_runlevel1:tst:1",
            "x": -2,
            "y": 3,
            "size": 3,
            "color": "#00ff00"
        },
        {
            "id": "oval:ssg-test_no_custom_runlevel1_target:tst:1",
            "label": "true",
            "url": "null",
            "text": "null",
            "title": "oval:ssg-test_no_custom_runlevel1_target:tst:1",
            "x": 0,
            "y": 3,
            "size": 3,
            "color": "#00ff00"
        },
        {
            "id": "oval:ssg-test_no_custom_rescue_service:tst:1",
            "label": "true",
            "url": "null",
            "text": "null",
            "title": "oval:ssg-test_no_custom_rescue_service:tst:1",
            "x": 2,
            "y": 3,
            "size": 3,
            "color": "#00ff00"
        }
    ],
    "edges": [
        {
            "id": "e2e284a9-b0e9-4eea-9d1e-c76995260e4f",
            "source": "xccdf_org.ssgproject.content_rule_require_singleuser_auth",
            "target": "oval:ssg-require_singleuser_auth:def:1"
        },
        {
            "id": "4ca7f7c0-dacb-43aa-9522-60f1f9ddecfb",
            "source": "oval:ssg-require_singleuser_auth:def:1",
            "target": "oval:ssg-test_require_rescue_service:tst:1"
        },
        {
            "id": "946cab56-46c6-454c-a6be-85e254634c0f",
            "source": "oval:ssg-require_singleuser_auth:def:1",
            "target": "oval:ssg-test_require_rescue_service_runlevel1:tst:1"
        },
        {
            "id": "270c6e09-2691-4170-9b00-91d3564673ca",
            "source": "oval:ssg-require_singleuser_auth:def:1",
            "target": "oval:ssg-test_no_custom_runlevel1_target:tst:1"
        },
        {
            "id": "96076b69-9dbc-4497-9597-a23e9d82e4dc",
            "source": "oval:ssg-require_singleuser_auth:def:1",
            "target": "oval:ssg-test_no_custom_rescue_service:tst:1"
        }
    ]
};