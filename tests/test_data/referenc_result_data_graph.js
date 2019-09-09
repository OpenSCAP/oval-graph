var data_json ={
    "nodes": [
        {
            "id": "xccdf_org.ssgproject.content_rule_package_abrt_removed",
            "label": "rule_package_abrt_removed",
            "url": "null",
            "text": null,
            "title": "xccdf_org.ssgproject.content_rule_package_abrt_removed",
            "x": 0,
            "y": 0.36,
            "size": 3,
            "color": "#ff0000",
            "type": "circle",
            "borderColor": "#ff0000"
        },
        {
            "id": "oval:ssg-package_abrt_removed:def:1",
            "label": "and",
            "url": "null",
            "text": null,
            "title": "oval:ssg-package_abrt_removed:def:1",
            "x": 0,
            "y": 1,
            "size": 3,
            "color": "#ff0000",
            "type": "circle",
            "borderColor": "#ff0000"
        },
        {
            "id": "oval:ssg-test_package_abrt_removed:tst:1",
            "label": "package_abrt_removed",
            "url": "null",
            "text": "package abrt is removed",
            "title": "oval:ssg-test_package_abrt_removed:tst:1",
            "x": 0,
            "y": 2,
            "size": 3,
            "color": "#ff0000",
            "type": "circle",
            "borderColor": "#ff0000"
        }
    ],
    "edges": [
        {
            "id": "c84530e6-2ffb-4128-b911-bd43bb34508b",
            "source": "xccdf_org.ssgproject.content_rule_package_abrt_removed",
            "target": "oval:ssg-package_abrt_removed:def:1",
            "color": "#ff0000"
        },
        {
            "id": "bc0f649c-d5f1-4c9a-acca-12e204f4b1d7",
            "source": "oval:ssg-package_abrt_removed:def:1",
            "target": "oval:ssg-test_package_abrt_removed:tst:1",
            "color": "#ff0000"
        }
    ]
};