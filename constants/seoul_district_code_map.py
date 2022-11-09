RAIN_DATA_DISTRICT_CODES = {
    "125": "송파",
    "124": "서초",
    "123": "관악",
    "122": "금천",
    "121": "동작",
    "120": "구로",
    "119": "영등포",
    "118": "양천",
    "117": "강서",
    "116": "용산",
    "115": "마포",
    "114": "서대문",
    "113": "은평",
    "112": "광진",
    "111": "중",
    "110": "종로",
    "109": "성동",
    "108": "동대문",
    "107": "중랑",
    "106": "성북",
    "105": "강북",
    "104": "노원",
    "103": "도봉",
    "102": "강동",
    "101": "강남",
}

DRAINPIPE_DATA_DISTRICT_CODES = {
    "01": "종로",
    "02": "중",
    "03": "용산",
    "04": "성동",
    "05": "광진",
    "06": "동대문",
    "07": "중랑",
    "08": "성북",
    "09": "강북",
    "10": "도봉",
    "11": "노원",
    "12": "은평",
    "13": "서대문",
    "14": "마포",
    "15": "양천",
    "16": "강서",
    "17": "구로",
    "18": "금천",
    "19": "영등포",
    "20": "동작",
    "21": "관악",
    "22": "서초",
    "23": "강남",
    "24": "송파",
    "25": "강동",
}

key_value_switched_rain_data = {y: x for x, y in RAIN_DATA_DISTRICT_CODES.items()}
key_value_switched_drainpipe_data = {
    y: x for x, y in DRAINPIPE_DATA_DISTRICT_CODES.items()
}

SEOUL_DISTRICT_CODES_MAP = dict()
for k in key_value_switched_drainpipe_data.keys():
    # 구청 코드가 key이고 수도관의 구분코드가 value가 됨
    SEOUL_DISTRICT_CODES_MAP[
        key_value_switched_drainpipe_data[k]
    ] = key_value_switched_rain_data[k]

rain_data_district_name = map(lambda x: x + "구", RAIN_DATA_DISTRICT_CODES.values())
RAIN_DATA_DISTRICT_CODES = dict(
    zip(RAIN_DATA_DISTRICT_CODES.keys(), rain_data_district_name)
)
