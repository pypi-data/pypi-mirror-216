VERSION = "0.2.93"


def get_dapi_version():
    return VERSION


class DapiError:
    def __init__(self, response, exception):
        self.response = response
        self.exception = exception
