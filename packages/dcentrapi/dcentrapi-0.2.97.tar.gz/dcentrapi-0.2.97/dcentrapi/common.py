class DapiError:
    def __init__(self, response, exception):
        self.response = response
        self.exception = exception
