import logging
import time

from mrlpy.framework.mrl_dataclass import mrl_dataclass


@mrl_dataclass("org.myrobotlab.framework.Message")
class Message(object):
    """Used to represent MRL messages"""

    msgId: int
    data: list
    historyList: list[str]
    name: str = ""
    method: str = ""
    sender: str = ""
    sendingMethod: str = ""
    encoding: str = "json"

    def __init__(self, name, method, data=(), **kwargs):
        # UNIX epoch timestamp, any system capable of running mrlpy should have sub-second time
        # May not represent actual timeline of messages if connecting between two different systems
        self.msgId = int(time.time() * 1000)

        self.log = logging.getLogger(__name__)

        self.log.debug("Creating message structure")
        self.name = name
        self.log.debug("Name set: " + name)
        self.method = method
        self.log.debug("Method set: " + method)
        self.data = data

        # Set defaults
        self.historyList = []
        self.properties = {}

        # Fill all other fields if set in constructor
        for key in kwargs:
            setattr(self, key, kwargs[key])
