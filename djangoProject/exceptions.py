class BadRequestException(Exception):
    def __init__(self, message='', *args, **kwargs):
        self.message = message