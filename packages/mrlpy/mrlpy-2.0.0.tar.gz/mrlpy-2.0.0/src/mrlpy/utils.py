import string
import random
from mrlpy.framework.mrl_dataclass import mrl_dataclass
from mrlpy.meventdispatch import MEventDispatch
from mrlpy.mevent import Message
from dataclasses import field

'''
Utility methods and variables
'''

eventDispatch = MEventDispatch()


def to_callback_topic_name(topic_method: str) -> str:
    if topic_method.startswith("publish"):
        return f"on{topic_method.lstrip('publish')[0].capitalize() + topic_method.lstrip('publish')[1:]}"
    elif topic_method.startswith("get"):
        return f"on{topic_method.lstrip('get')[0].capitalize() + topic_method.lstrip('get')[1:]}"
    else:
        return f"on{topic_method.capitalize()[0].capitalize() + topic_method[1:]}"


@mrl_dataclass("org.myrobotlab.framework.DescribeResults")
class DescribeResults(object):
    id: str = ""
    uuid: str = ""
    request: dict = field(default_factory=lambda: {})
    platform: object = None
    status: object = None
    registrations: list = field(default_factory=lambda: [])


@mrl_dataclass("org.myrobotlab.framework.MRLListener")
class MRLListener(object):
    topicMethod: str
    callbackName: str
    callbackMethod: str

    def __call__(self, ev):
        message = Message(self.callbackName, self.callbackMethod, ev.data)
        eventDispatch.dispatch_event(message)

    def __hash__(self) -> int:
        return 37 + self.topicMethod.__hash__() + self.callbackName.__hash__() + self.callbackMethod.__hash__()


@mrl_dataclass("org.myrobotlab.framework.DescribeQuery")
class DescribeQuery(object):
    id: str
    uuid: str
    platform: object


@mrl_dataclass("org.myrobotlab.framework.Registration")
class Registration(object):
    id: str
    name: str
    typeKey: str
    state: str = field(default_factory=lambda: "{}")
    interfaces: list[str] = ()


def genID(size=6, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    """
    Generate a random ID for creating unique names
    """
    return ''.join(random.choice(chars) for _ in range(size))
