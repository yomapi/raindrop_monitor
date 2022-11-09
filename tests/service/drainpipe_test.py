from drainpipe.service import drainpipe_service


def test_find_realtime_drainpipe_data_with_limit():
    sut = drainpipe_service.find_realtime_drainpipe_data_with_limit("12")
    return sut
