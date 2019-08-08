var data_json ={
    "nodes": [
        {
            "id": "xccdf_org.ssgproject.content_rule_sssd_ssh_known_hosts_timeout",
            "label": "rule_sssd_ssh_known_hosts_timeout",
            "url": "null",
            "text": "null",
            "title": "xccdf_org.ssgproject.content_rule_sssd_ssh_known_hosts_timeout",
            "x": 0,
            "y": 0.36,
            "size": 3,
            "color": "#ff0000"
        },
        {
            "id": "oval:ssg-sssd_ssh_known_hosts_timeout:def:1",
            "label": "or",
            "url": "null",
            "text": "null",
            "title": "oval:ssg-sssd_ssh_known_hosts_timeout:def:1",
            "x": 0,
            "y": 1,
            "size": 3,
            "color": "#ff0000"
        },
        {
            "id": "e820767d-603a-44f7-a8b0-de759ff12616",
            "label": "or",
            "url": "null",
            "text": "null",
            "title": "e820767d-603a-44f7-a8b0-de759ff12616",
            "x": -2,
            "y": 2,
            "size": 3,
            "color": "#ff0000"
        },
        {
            "id": "oval:ssg-test_sssd_ssh_known_hosts_timeout:tst:1",
            "label": "sssd_ssh_known_hosts_timeout",
            "url": "null",
            "text": "null",
            "title": "oval:ssg-test_sssd_ssh_known_hosts_timeout:tst:1",
            "x": 2,
            "y": 2,
            "size": 3,
            "color": "#ff0000"
        },
        {
            "id": "4f2eb641-c71f-484c-a25b-7f27ac34560a",
            "label": "or",
            "url": "null",
            "text": "null",
            "title": "4f2eb641-c71f-484c-a25b-7f27ac34560a",
            "x": -2,
            "y": 3,
            "size": 3,
            "color": "#ff0000"
        },
        {
            "id": "671c0f0b-fc38-42d7-8064-5272a740804b",
            "label": "and",
            "url": "null",
            "text": "null",
            "title": "671c0f0b-fc38-42d7-8064-5272a740804b",
            "x": 2,
            "y": 3,
            "size": 3,
            "color": "#ff0000"
        },
        {
            "id": "6c283d82-7b54-4100-9c1b-42df0e008546",
            "label": "and",
            "url": "null",
            "text": "null",
            "title": "6c283d82-7b54-4100-9c1b-42df0e008546",
            "x": -2,
            "y": 4,
            "size": 3,
            "color": "#ff0000"
        },
        {
            "id": "9371e06b-43e9-483f-8172-a06f795d8ac7",
            "label": "and",
            "url": "null",
            "text": "null",
            "title": "9371e06b-43e9-483f-8172-a06f795d8ac7",
            "x": 0,
            "y": 4,
            "size": 3,
            "color": "#ff0000"
        },
        {
            "id": "oval:ssg-test_sssd_conf_exists:tst:1",
            "label": "sssd_conf_exists",
            "url": "null",
            "text": "null",
            "title": "oval:ssg-test_sssd_conf_exists:tst:1",
            "x": 2,
            "y": 4.36,
            "size": 3,
            "color": "#ff0000"
        },
        {
            "id": "oval:ssg-test_package_sssd_removed:tst:1",
            "label": "package_sssd_removed",
            "url": "null",
            "text": "null",
            "title": "oval:ssg-test_package_sssd_removed:tst:1",
            "x": -4,
            "y": 5,
            "size": 3,
            "color": "#ff0000"
        },
        {
            "id": "oval:ssg-test_sssd_not_wanted_by_multi_user_target:tst:1",
            "label": "sssd_not_wanted_by_multi_user_target",
            "url": "null",
            "text": "null",
            "title": "oval:ssg-test_sssd_not_wanted_by_multi_user_target:tst:1",
            "x": -2,
            "y": 5.36,
            "size": 3,
            "color": "#ff0000"
        },
        {
            "id": "oval:ssg-test_sssd_socket_not_wanted_by_multi_user_target:tst:1",
            "label": "sssd_socket_not_wanted_by_multi_user_target",
            "url": "null",
            "text": "null",
            "title": "oval:ssg-test_sssd_socket_not_wanted_by_multi_user_target:tst:1",
            "x": 0,
            "y": 5,
            "size": 3,
            "color": "#00ff00"
        },
        {
            "id": "oval:ssg-test_service_not_running_sssd:tst:1",
            "label": "service_not_running_sssd",
            "url": "null",
            "text": "null",
            "title": "oval:ssg-test_service_not_running_sssd:tst:1",
            "x": 2,
            "y": 5.36,
            "size": 3,
            "color": "#ff0000"
        }
    ],
    "edges": [
        {
            "id": "041da22f-5625-437d-9695-963342610504",
            "source": "xccdf_org.ssgproject.content_rule_sssd_ssh_known_hosts_timeout",
            "target": "oval:ssg-sssd_ssh_known_hosts_timeout:def:1",
            "color": "#ff0000"
        },
        {
            "id": "7c1c3eb4-7662-47a2-a3ac-054e710a462a",
            "source": "oval:ssg-sssd_ssh_known_hosts_timeout:def:1",
            "target": "e820767d-603a-44f7-a8b0-de759ff12616",
            "color": "#ff0000"
        },
        {
            "id": "4bba79a8-5c51-4f69-a4da-b83d01be359f",
            "source": "e820767d-603a-44f7-a8b0-de759ff12616",
            "target": "4f2eb641-c71f-484c-a25b-7f27ac34560a",
            "color": "#ff0000"
        },
        {
            "id": "2d158125-1a58-47b7-ac3d-66b4bc8ac6b6",
            "source": "4f2eb641-c71f-484c-a25b-7f27ac34560a",
            "target": "6c283d82-7b54-4100-9c1b-42df0e008546",
            "color": "#ff0000"
        },
        {
            "id": "9ec800d4-d95b-4738-8179-1d91e9894030",
            "source": "6c283d82-7b54-4100-9c1b-42df0e008546",
            "target": "oval:ssg-test_package_sssd_removed:tst:1",
            "color": "#ff0000"
        },
        {
            "id": "bf7c457a-fc7d-45b4-b40e-e41a67b79b6b",
            "source": "4f2eb641-c71f-484c-a25b-7f27ac34560a",
            "target": "9371e06b-43e9-483f-8172-a06f795d8ac7",
            "color": "#ff0000"
        },
        {
            "id": "cedb55aa-61c3-40de-a86c-9e9d1d238e7d",
            "source": "9371e06b-43e9-483f-8172-a06f795d8ac7",
            "target": "oval:ssg-test_sssd_not_wanted_by_multi_user_target:tst:1",
            "color": "#ff0000"
        },
        {
            "id": "bd289d14-ac20-45fc-b9ce-58d6f4f98b3d",
            "source": "9371e06b-43e9-483f-8172-a06f795d8ac7",
            "target": "oval:ssg-test_sssd_socket_not_wanted_by_multi_user_target:tst:1",
            "color": "#00ff00"
        },
        {
            "id": "da917efb-7b1f-4f48-b1e2-9f04ad0b593f",
            "source": "9371e06b-43e9-483f-8172-a06f795d8ac7",
            "target": "oval:ssg-test_service_not_running_sssd:tst:1",
            "color": "#ff0000"
        },
        {
            "id": "c2b06693-fded-402c-b23b-ede7784a3135",
            "source": "e820767d-603a-44f7-a8b0-de759ff12616",
            "target": "671c0f0b-fc38-42d7-8064-5272a740804b",
            "color": "#ff0000"
        },
        {
            "id": "df241f11-ec4a-409d-8a11-e652b4881855",
            "source": "671c0f0b-fc38-42d7-8064-5272a740804b",
            "target": "oval:ssg-test_sssd_conf_exists:tst:1",
            "color": "#ff0000"
        },
        {
            "id": "058c9f00-4827-4ceb-9002-d9413c379d9f",
            "source": "oval:ssg-sssd_ssh_known_hosts_timeout:def:1",
            "target": "oval:ssg-test_sssd_ssh_known_hosts_timeout:tst:1",
            "color": "#ff0000"
        }
    ]
};