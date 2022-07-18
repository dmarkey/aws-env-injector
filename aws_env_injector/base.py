

class BaseBackend:
    json_expand_capable = True

    @classmethod
    def fetch_value(cls, config: dict):
        pass


class MisconfigurationException(Exception):
    pass