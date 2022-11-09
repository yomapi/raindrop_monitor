from utils.providers.seoul_city_data_providers import (
    drainpipe_data_provider,
    rain_data_provider,
)


def test_request_drainpipe_data():
    cnt, data = drainpipe_data_provider.get()
    assert isinstance(cnt, int)
    assert isinstance(data, list)


def test_request_rain_data():
    cnt, data = rain_data_provider.get()
    assert isinstance(cnt, int)
    assert isinstance(data, list)
