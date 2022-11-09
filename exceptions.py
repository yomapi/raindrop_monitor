class CustomBaseExecption(Exception):
    is_custom_execption = True


class SeoulAPIResponseError(CustomBaseExecption):
    def __init__(self, msg="Seoul open api request failed.", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)
