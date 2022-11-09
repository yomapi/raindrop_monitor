import requests
import json

from configs.config import config
from exceptions import SeoulAPIResponseError

SEOUL_OPEN_API_KEY = config.seoul_api["key"]
DRAINPIPE_ROOT_URL = (
    f"http://openAPI.seoul.go.kr:8088/{SEOUL_OPEN_API_KEY}/json/DrainpipeMonitoringInfo"
)
RAINDROP_ROOT_URL = (
    f"http://openAPI.seoul.go.kr:8088/{SEOUL_OPEN_API_KEY}/json/ListRainfallService"
)


class SeoulOpenAPIProvider:
    def __init__(self, root_url: str, data_key: str) -> None:
        self.key = SEOUL_OPEN_API_KEY
        self.root_url = root_url
        self.data_key = data_key
        self.success_res_code = "INFO-000"

    def _get_response_code_from_response(self, response: dict) -> str:
        return response["RESULT"]["CODE"]

    def _parse_response_data(self, response: requests.Response) -> tuple:
        """
        총 데이터 갯수, 추출한 데이터를 return 합니다.
        """
        data = json.loads(response.content)[self.data_key]
        res_code = self._get_response_code_from_response(data)
        if res_code == self.success_res_code:
            return data["list_total_count"], data["row"]
        else:
            raise SeoulAPIResponseError

    def _request_api(self, url: str) -> tuple:
        """
        api를 요청하고, 데이터를 파싱해서 return 합니다.
        return 형태는 총 갯수, data list 입니다
        """
        response = requests.get(url)
        return self._parse_response_data(response)

    def get(self, start: int = 1, end: int = 2) -> tuple:
        # TODO: 검색 옵션 받기
        # TODO: 비동기 처리
        """
        파라매터로 url을 만든후, api 요청 함수를 호출합니다.
        return 형태는 총 갯수, data list 입니다
        """
        url = f"{self.root_url}/{start}/{end}"
        return self._request_api(url)


class DrainpipeAPIProvider(SeoulOpenAPIProvider):
    def get(
        self, city_code: int, start_at: str, end_at: str, start: int, end: int
    ) -> tuple:
        # TODO: 검색 옵션 받기
        # TODO: 비동기 처리
        url = f"{self.root_url}/{start}/{end}/{city_code}/{start_at}/{end_at}/"
        return self._request_api(url)


class RainAPIProvider(SeoulOpenAPIProvider):
    def get(
        self,
        start: int,
        end: int,
        city_name: str = "",
    ) -> tuple:
        # TODO: 검색 옵션 받기
        # TODO: 비동기 처리
        url = f"{self.root_url}/{start}/{end}/{city_name}"
        return self._request_api(url)


drainpipe_data_provider = DrainpipeAPIProvider(
    DRAINPIPE_ROOT_URL, "DrainpipeMonitoringInfo"
)
rain_data_provider = RainAPIProvider(RAINDROP_ROOT_URL, "ListRainfallService")
