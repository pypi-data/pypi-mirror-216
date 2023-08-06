class Proxy(object):
    """
    Base class for proxy services
    """

    def __init__(self, classtype, name):
        self._type = classtype
        self.name = name
