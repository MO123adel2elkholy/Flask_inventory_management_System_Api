class APIException(Exception):
    def init(self, message, status_code):
        self.message = message
        self.status_code = status_code
