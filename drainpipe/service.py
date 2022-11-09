from utils.providers.seoul_city_data_providers import (
    drainpipe_data_provider,
    rain_data_provider,
)
from constants.seoul_district_code_map import (
    DRAINPIPE_DATA_DISTRICT_CODES,
)
from datetime import datetime, timedelta
from django.utils import timezone
from utils.datetime_handler import datetime_to_str, str_to_datetime, get_first_second


class DrainpipeService:
    def __init__(self) -> None:
        pass

    def is_in_1hour_time_range(
        self,
        target_time_str: str,
        hour_ago_dt: datetime,
        dt_foramt: str = "%Y-%m-%d %H:%M",
    ) -> bool:
        return get_first_second(hour_ago_dt) <= str_to_datetime(
            target_time_str, dt_foramt
        )

    def _filter_rain_data_by_recieve_time(
        self, rain_data: list[dict], date_from: datetime
    ) -> list:
        return list(
            filter(
                lambda x: self.is_in_1hour_time_range(x["receive_time"], date_from),
                rain_data,
            )
        )

    def _get_rain_drop_district_name(self, drainpipe_district_code: str):
        return DRAINPIPE_DATA_DISTRICT_CODES[drainpipe_district_code] + "구"

    def _get_average_group_by_id(
        self, data_lst: list[dict], average_target_key: str, id_key: str
    ) -> float:
        sum_dict = dict()
        for data in data_lst:
            machine_serial_number = data[id_key]
            if sum_dict.get(machine_serial_number, None) != None:
                sum_dict[machine_serial_number]["total"] += data[average_target_key]
                sum_dict[machine_serial_number]["cnt"] += 1
            else:
                sum_dict[machine_serial_number] = dict()
                sum_dict[machine_serial_number]["total"] = data[average_target_key]
                sum_dict[machine_serial_number]["cnt"] = 1
                sum_dict[machine_serial_number]["loaction"] = data["location"]

        for machine_serial_number in sum_dict.keys():
            data = sum_dict[machine_serial_number]
            sum_dict[machine_serial_number]["average"] = data["total"] / data["cnt"]
        return sum_dict

    def _parse_drain_pipe_data(self, drainpipe_data_lst: list[dict]) -> list[dict]:
        return list(
            map(
                lambda x: {
                    "sensor_id": x["IDN"],
                    "receive_time": x["MEA_YMD"],
                    "wal": x["MEA_WAL"],
                    "location": x["REMARK"],
                },
                drainpipe_data_lst,
            )
        )

    def _parse_rain_data_lst(self, rain_data_lst: list[dict]) -> list[dict]:
        return list(
            map(
                lambda x: {
                    "gauge_code": str(int(x["RAINGAUGE_CODE"])),
                    "location": x["RAINGAUGE_NAME"],
                    "rain_drop": float(x["RAINFALL10"]),
                    "receive_time": x["RECEIVE_TIME"],
                },
                rain_data_lst,
            )
        )

    def find_realtime_drainpipe_data_with_limit(
        self,
        drainpipe_district_code: str,
        start_index: int = 1,
        end_index: int = 1000,
    ) -> dict:
        """
        1시간전 부터 현재까지 데이터를 요청해서 가져옵니다
        """
        # TODO: 비동기 처리
        date_from = timezone.now() - timedelta(hours=1)
        date_from_str = datetime_to_str(date_from, "%Y%m%d%H")
        date_end_str = datetime_to_str(timezone.now(), "%Y%m%d%H")
        drainpipe_data_cnt, drainpipe_data = drainpipe_data_provider.get(
            drainpipe_district_code, date_from_str, date_end_str, start_index, end_index
        )
        rain_data_cnt, rain_data = rain_data_provider.get(
            start_index,
            end_index,
            self._get_rain_drop_district_name(drainpipe_district_code),
        )

        drainpipe_data = self._parse_drain_pipe_data(drainpipe_data)
        rain_data = self._filter_rain_data_by_recieve_time(
            self._parse_rain_data_lst(rain_data), date_from
        )
        rain_drop_average_data = self._get_average_group_by_id(
            rain_data, "rain_drop", "gauge_code"
        )
        drainpipe_average_data = self._get_average_group_by_id(
            drainpipe_data, "wal", "sensor_id"
        )

        return {
            "pipe_average": drainpipe_average_data,
            "rain_average": rain_drop_average_data,
            "pipe_list": drainpipe_data,
            "rain_list": rain_data,
        }


drainpipe_service = DrainpipeService()
