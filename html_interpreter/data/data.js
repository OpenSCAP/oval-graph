var data_json ={
    "nodes": [
        {
            "id": "xccdf_org.ssgproject.content_rule_disable_host_auth",
            "label": "and",
            "url": "null",
            "text": "null",
            "title": "xccdf_org.ssgproject.content_rule_disable_host_auth",
            "x": -17,
            "y": 0,
            "size": 3,
            "color": "#00ff00"
        },
        {
            "id": "oval:ssg-disable_host_auth:def:1",
            "label": "or",
            "url": "null",
            "text": "null",
            "title": "oval:ssg-disable_host_auth:def:1",
            "x": -17,
            "y": 1,
            "size": 3,
            "color": "#00ff00"
        },
        {
            "id": "96bdb8b3-4d9c-4546-9732-67227f131100",
            "label": "and",
            "url": "null",
            "text": "null",
            "title": "96bdb8b3-4d9c-4546-9732-67227f131100",
            "x": -15,
            "y": 3,
            "size": 3,
            "color": "#ff0000"
        },
        {
            "id": "b3bc349e-4930-418c-bf1f-9f433657af09",
            "label": "or",
            "url": "null",
            "text": "null",
            "title": "b3bc349e-4930-418c-bf1f-9f433657af09",
            "x": -13,
            "y": 5,
            "size": 3,
            "color": "#00ff00"
        },
        {
            "id": "oval:ssg-test_sshd_not_required:tst:1",
            "label": "false",
            "url": "null",
            "text": "null",
            "title": "oval:ssg-test_sshd_not_required:tst:1",
            "x": -11,
            "y": 7,
            "size": 3,
            "color": "#ff0000"
        },
        {
            "id": "9706d717-7d92-4631-b8c3-23d168e9f162",
            "label": "and",
            "url": "null",
            "text": "null",
            "title": "9706d717-7d92-4631-b8c3-23d168e9f162",
            "x": -9,
            "y": 7,
            "size": 3,
            "color": "#00ff00"
        },
        {
            "id": "c336b850-679b-4e95-964d-37e7d58f89e4",
            "label": "and",
            "url": "null",
            "text": "null",
            "title": "c336b850-679b-4e95-964d-37e7d58f89e4",
            "x": -8,
            "y": 5,
            "size": 3,
            "color": "#ff0000"
        },
        {
            "id": "oval:ssg-test_package_openssh-server_removed:tst:1",
            "label": "false",
            "url": "null",
            "text": "null",
            "title": "oval:ssg-test_package_openssh-server_removed:tst:1",
            "x": -6,
            "y": 7,
            "size": 3,
            "color": "#ff0000"
        },
        {
            "id": "912a1471-72cf-49e1-a054-d55781a0c191",
            "label": "and",
            "url": "null",
            "text": "null",
            "title": "912a1471-72cf-49e1-a054-d55781a0c191",
            "x": -7,
            "y": 3,
            "size": 3,
            "color": "#00ff00"
        },
        {
            "id": "b1372f91-6f2c-4edc-8913-19d1f227a0db",
            "label": "or",
            "url": "null",
            "text": "null",
            "title": "b1372f91-6f2c-4edc-8913-19d1f227a0db",
            "x": -5,
            "y": 5,
            "size": 3,
            "color": "#00ff00"
        },
        {
            "id": "oval:ssg-test_sshd_required:tst:1",
            "label": "false",
            "url": "null",
            "text": "null",
            "title": "oval:ssg-test_sshd_required:tst:1",
            "x": -3,
            "y": 7,
            "size": 3,
            "color": "#ff0000"
        },
        {
            "id": "4acff7c6-b693-4652-8592-a735786a9927",
            "label": "and",
            "url": "null",
            "text": "null",
            "title": "4acff7c6-b693-4652-8592-a735786a9927",
            "x": -1,
            "y": 7,
            "size": 3,
            "color": "#00ff00"
        },
        {
            "id": "c57402d1-55b7-42e2-a2eb-5dfdeb55ae99",
            "label": "and",
            "url": "null",
            "text": "null",
            "title": "c57402d1-55b7-42e2-a2eb-5dfdeb55ae99",
            "x": 0,
            "y": 5,
            "size": 3,
            "color": "#00ff00"
        },
        {
            "id": "oval:ssg-test_package_openssh-server_installed:tst:1",
            "label": "true",
            "url": "null",
            "text": "null",
            "title": "oval:ssg-test_package_openssh-server_installed:tst:1",
            "x": 2,
            "y": 7,
            "size": 3,
            "color": "#00ff00"
        },
        {
            "id": "oval:ssg-test_sshd_hostbasedauthentication:tst:1",
            "label": "true",
            "url": "null",
            "text": "null",
            "title": "oval:ssg-test_sshd_hostbasedauthentication:tst:1",
            "x": 3,
            "y": 5,
            "size": 3,
            "color": "#00ff00"
        },
        {
            "id": "oval:ssg-test_sshd_requirement_unset:tst:1",
            "label": "true",
            "url": "null",
            "text": "null",
            "title": "oval:ssg-test_sshd_requirement_unset:tst:1",
            "x": -7,
            "y": 9,
            "size": 3,
            "color": "#00ff00"
        }
    ],
    "edges": [
        {
            "id": "4ae9f842-0f46-460f-8728-ac435d8e65e5",
            "source": "xccdf_org.ssgproject.content_rule_disable_host_auth",
            "target": "oval:ssg-disable_host_auth:def:1"
        },
        {
            "id": "43a9f878-4376-4bc1-a7fd-db802597d91c",
            "source": "oval:ssg-disable_host_auth:def:1",
            "target": "96bdb8b3-4d9c-4546-9732-67227f131100"
        },
        {
            "id": "337e875c-1c96-45dd-919e-26d012f6f153",
            "source": "96bdb8b3-4d9c-4546-9732-67227f131100",
            "target": "b3bc349e-4930-418c-bf1f-9f433657af09"
        },
        {
            "id": "237b106a-4879-4400-8200-016b452505de",
            "source": "b3bc349e-4930-418c-bf1f-9f433657af09",
            "target": "oval:ssg-test_sshd_not_required:tst:1"
        },
        {
            "id": "c9a8d4ee-70c6-4f6a-b7ef-8381dae35740",
            "source": "b3bc349e-4930-418c-bf1f-9f433657af09",
            "target": "9706d717-7d92-4631-b8c3-23d168e9f162"
        },
        {
            "id": "f1ebe72f-3db9-4a81-b3a3-aee3dcc2eb49",
            "source": "9706d717-7d92-4631-b8c3-23d168e9f162",
            "target": "oval:ssg-test_sshd_requirement_unset:tst:1"
        },
        {
            "id": "c225c505-50f3-4423-a121-cf72f0bab44a",
            "source": "96bdb8b3-4d9c-4546-9732-67227f131100",
            "target": "c336b850-679b-4e95-964d-37e7d58f89e4"
        },
        {
            "id": "77a72430-2918-4feb-93a8-c24f81556799",
            "source": "c336b850-679b-4e95-964d-37e7d58f89e4",
            "target": "oval:ssg-test_package_openssh-server_removed:tst:1"
        },
        {
            "id": "864d88ca-5fd6-404f-af3a-addecd0a048a",
            "source": "oval:ssg-disable_host_auth:def:1",
            "target": "912a1471-72cf-49e1-a054-d55781a0c191"
        },
        {
            "id": "0c65f824-b7cc-4532-95d9-bd93f7c9e8b1",
            "source": "912a1471-72cf-49e1-a054-d55781a0c191",
            "target": "b1372f91-6f2c-4edc-8913-19d1f227a0db"
        },
        {
            "id": "1987c86f-a159-4439-89ad-52f5cf2de8cd",
            "source": "b1372f91-6f2c-4edc-8913-19d1f227a0db",
            "target": "oval:ssg-test_sshd_required:tst:1"
        },
        {
            "id": "ddc0c3b4-20a5-4acc-81db-d924ef78fd1f",
            "source": "b1372f91-6f2c-4edc-8913-19d1f227a0db",
            "target": "4acff7c6-b693-4652-8592-a735786a9927"
        },
        {
            "id": "2a946c3e-b4e5-42a3-a32c-4114e9467642",
            "source": "4acff7c6-b693-4652-8592-a735786a9927",
            "target": "oval:ssg-test_sshd_requirement_unset:tst:1"
        },
        {
            "id": "04e6abd1-4516-46b2-8efe-615f42b8d35b",
            "source": "912a1471-72cf-49e1-a054-d55781a0c191",
            "target": "c57402d1-55b7-42e2-a2eb-5dfdeb55ae99"
        },
        {
            "id": "9c1eefdb-ecb4-43f5-916f-fe6204ae468b",
            "source": "c57402d1-55b7-42e2-a2eb-5dfdeb55ae99",
            "target": "oval:ssg-test_package_openssh-server_installed:tst:1"
        },
        {
            "id": "c91eee3e-fdb9-4a15-b3f0-2568e4ee6af1",
            "source": "912a1471-72cf-49e1-a054-d55781a0c191",
            "target": "oval:ssg-test_sshd_hostbasedauthentication:tst:1"
        }
    ]
};