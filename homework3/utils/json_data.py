import faker

fake = faker.Faker()

segment_payload = {"name": fake.lexify(text='???? ????? ???'),
                   "pass_condition": 1,
                   "relations": [{"object_type": "remarketing_player",
                                  "params": {"type": "positive",
                                             "left": 365,
                                             "right": 0}}],
                   "logicType": "or"}

campaign_payload = {
    "name": fake.lexify(text='???? ????? ???'),
    "read_only": False,
    "conversion_funnel_id": None,
    "objective": "traffic",
    "enable_offline_goals": False,
    "targetings": {
        "split_audience": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "sex": ["male", "female"],
        "age": {
            "age_list": [0, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32,
                         33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54,
                         55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75],
            "expand": True
        },
        "geo": {
            "regions": [188]
        },
        "interests_soc_dem": [],
        "segments": [],
        "interests": [],
        "fulltime": {
            "flags": ["use_holidays_moving", "cross_timezone"],
            "mon": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
            "tue": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
            "wed": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
            "thu": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
            "fri": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
            "sat": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
            "sun": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
        },
        "pads": [102643],
        "mobile_types": ["tablets", "smartphones"],
        "mobile_vendors": [],
        "mobile_operators": []
    },
    "age_restrictions": None,
    "date_start": None,
    "date_end": None,
    "autobidding_mode": "second_price_mean",
    "budget_limit_day": None,
    "budget_limit": None,
    "mixing": "fastest",
    "utm": None,
    "enable_utm": True,
    "price": "6.31",
    "max_price": "0",
    "package_id": 961,
    "banners": [{
        "urls": {
            "primary": {
                "id": 0
            }
        },
        "textblocks": {},
        "content": {
            "image_240x400": {
                "id": 0
            }
        },
        "name": ""
    }]
}
