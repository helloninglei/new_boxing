
let mock = true;
let options = {};
let detail = [];

if (mock) {
    options = {
        "count": 1,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 5,
                "created_time": "2018-03-28T10:23:01.541066+08:00",
                "updated_time": "2018-03-28T10:23:01.541103+08:00",
                "current_period": 1,
                "name": "测试集合2",
                "frequency": "QUARTERLY",
                "way": "BONUS",
                "start_date": "2018-03-28",
                "end_date": "2018-06-27",
                "finish_time": "2018-03-28T19:35:39+08:00",
                "attachment_url": null,
                "result": 90,
                "is_lock": false,
                "exam_set": 2,
                "examinee_role": 8,
                "examinee": 8
            },
            {
                "id": 6,
                "created_time": "2018-03-28T10:23:01.541066+08:00",
                "updated_time": "2018-03-28T10:23:01.541103+08:00",
                "current_period": 1,
                "name": "测试集合2",
                "frequency": "QUARTERLY",
                "way": "BONUS",
                "start_date": "2018-03-28",
                "end_date": "2018-06-27",
                "finish_time": "2018-03-28T19:35:39+08:00",
                "attachment_url": null,
                "result": 90,
                "is_lock": false,
                "exam_set": 2,
                "examinee_role": 8,
                "examinee": 8
            },
            {
                "id": 7,
                "created_time": "2018-03-28T10:23:01.541066+08:00",
                "updated_time": "2018-03-28T10:23:01.541103+08:00",
                "current_period": 1,
                "name": "测试集合2",
                "frequency": "QUARTERLY",
                "way": "BONUS",
                "start_date": "2018-03-28",
                "end_date": "2018-06-27",
                "finish_time": "2018-03-28T19:35:39+08:00",
                "attachment_url": null,
                "result": 90,
                "is_lock": false,
                "exam_set": 2,
                "examinee_role": 8,
                "examinee": 8
            }
        ]
    };

    detail =  [
        {
            "id": 33,
            "examiner": {
                "id": 13,
                "roles": [
                    {
                        "id": 7,
                        "name": "rolet2"
                    },
                    {
                        "id": 8,
                        "name": "role8"
                    }
                ],
                "name": "张三100",
                "identity": "id100",
                "mobile": null,
                "org_name": null,
                "org_code": null
            },
            "examiner_role": {
                "id": 7,
                "name": "rolet2"
            },
            "created_time": "2018-03-28T10:23:01.591592+08:00",
            "updated_time": "2018-03-28T10:23:01.591622+08:00",
            "name": "测试集合1指标1",
            "upper": 20,
            "lower": 10,
            "description": "测试集合1指标1的描述可以300个字",
            "attachment_url": null,
            "result": 10,
            "remark": null,
            "doc_url": null,
            "is_lock": false,
            "exam_item": 1,
            "exam_set_task": 5
        },
        {
            "id": 28,
            "examiner": {
                "id": 13,
                "roles": [
                    {
                        "id": 7,
                        "name": "rolet2"
                    },
                    {
                        "id": 8,
                        "name": "role8"
                    }
                ],
                "name": "张三100",
                "identity": "id100",
                "mobile": null,
                "org_name": null,
                "org_code": null
            },
            "examiner_role": {
                "id": 8,
                "name": "role8"
            },
            "created_time": "2018-03-28T10:23:01.560378+08:00",
            "updated_time": "2018-03-28T10:23:01.560403+08:00",
            "name": "测试指标3",
            "upper": 30,
            "lower": 5,
            "description": "测试指标2的描述可以300个字",
            "attachment_url": "http://www.baidu.com",
            "result": 20,
            "remark": null,
            "doc_url": null,
            "is_lock": false,
            "exam_item": 4,
            "exam_set_task": 5
        }
    ]
}


export {options,detail}