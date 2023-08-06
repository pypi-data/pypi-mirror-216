import atexit
import logging
import sys
from queue import Queue
from threading import Thread

from mrlpy import mcommand
from mrlpy import utils
from mrlpy.framework import runtime
from mrlpy.framework.interfaces import ServiceInterface, MRLInterface
from mrlpy.mevent import Message
from mrlpy.utils import MRLListener, Registration, to_callback_topic_name

"""Represents the base service class"""


class Service(ServiceInterface):
    __log = logging.getLogger(__name__)

    def __init__(self, name=""):
        """
        Registers service with mcommand event registers and MRL service registry
        """

        self.proxyClass = None
        self.mrl_listeners: dict[str, list[MRLListener]] = dict()

        self.inbox_queue = Queue()
        self.inbox_thread = Thread(target=self.run_inbox, daemon=True)

        if name == "":
            try:
                # Get name from args
                self.name = sys.argv[1]
            except IndexError:
                # No first argument
                # Need to auto-generate name
                self.name = utils.genID()
        else:
            self.name = name
        # self.connectWithProxy(True) #Proxy classes are not needed in Nixie
        mcommand.addEventListener(self.name, self.onMessage)
        mcommand.addEventListener(f"{self.name}@{runtime.runtime_id}", self.onMessage)
        self.inbox_thread.start()
        # Will release service when Python exits. TODO Check to see if necessary with Messages2 API
        atexit.register(self.release)
        self.register(self.registration)

        # signal.pause()

    def run_inbox(self):
        while True:
            e: Message = self.inbox_queue.get()
            # Enables sending a return value back; Other half implemented in mcommand and proxy service
            ret = None
            # Invoke method with data
            if len(e.data) > 0:
                params = ','.join(map(str, e.data))
                self.__log.debug("Invoking: " + e.method + '(' + params + ')')
                ret = getattr(self, e.method).__call__(*e.data)
            else:
                self.__log.debug("Invoking: " + e.method + '()')
                ret = getattr(self, e.method).__call__()
            if e.method in self.mrl_listeners:
                for listener in self.mrl_listeners[e.method]:
                    if type(ret) is tuple:
                        mcommand.sendCommand(listener.callbackName, listener.callbackMethod, ret)
                    else:
                        mcommand.sendCommand(listener.callbackName, listener.callbackMethod, [ret])

    def register(self, registration: Registration):
        runtime.Runtime.getRuntime().register(registration)

    @property
    def registration(self):
        type_key = f"py:{__name__}"
        for superclass in self.__class__.__mro__:
            print(f"{superclass}: {issubclass(superclass, MRLInterface)}")
        interfaces = [superclass.java_interface_name() for superclass in self.__class__.__mro__
                      if issubclass(superclass, MRLInterface) and superclass is not MRLInterface
                      and superclass is not self.__class__ and superclass is not Service]
        return Registration(id=runtime.runtime_id, name=self.name, typeKey=type_key, interfaces=interfaces)

    def onMessage(self, e: Message):
        """
        Handles message invocation and parsing
        of params; WARNING: DO NOT OVERRIDE
        THIS METHOD UNLESS YOU KNOW WHAT YOU
        ARE DOING!!!!!!!
        """
        self.inbox_queue.put(e)

    def release(self):
        """
        Utility method for releasing the proxy service;
        Also deletes this service
        """
        # mcommand.sendCommand("runtime", "release", [self.name])
        del self

    def outMessage(self, msg):
        if len(msg.sender) == 0:
            msg.sender = self.name
        mcommand.eventDispatch.dispatch_event(msg)

    def out(self, method, *params):
        self.outMessage(Message(self.name, method, params))

    def addListener(self, *args, **kwargs):
        """
        Register a callback on a topic method.
        There are 2 ways to call this method, to account for the
        overloaded Java signature

        1. addListener(listener: MRLListener)
        2. addListener(topicMethod: str, callbackName: str, callbackMethod: str)

        You can pass the arguments either regularly or as keyword arguments,
        but you must be consistent. Don't pass some arguments regularly and
        others as keyword args.
        """

        if type(args[0]) == MRLListener:
            listener = args[0]
        elif 'listener' in kwargs:
            listener = kwargs['listener']
        elif len(args) >= 3:
            listener = MRLListener(args[0], args[1] if '@' in args[1] else f"{args[1]}@{self.getId()}", args[2])
        else:
            listener = MRLListener(**kwargs)

        if listener.topicMethod in self.mrl_listeners:
            self.mrl_listeners[listener.topicMethod].append(listener)
        else:
            self.mrl_listeners.update({listener.topicMethod: [listener]})

    def removeListener(self, topic_name, callback_name, in_method=None) -> None:
        """
        Remove a listener from this service.
        :param topic_name: The topic that the listener to be removed is subscribed to
        :param callback_name: The name of the service the listener calls back to
        :param in_method: The method of the callback service the listener calls
        """
        if in_method is None:
            in_method = to_callback_topic_name(topic_name)
        if topic_name in self.mrl_listeners:
            self.mrl_listeners[topic_name] = [
                listener for listener in self.mrl_listeners[topic_name]
                if listener.callbackName != callback_name or listener.callbackMethod != in_method
            ]

    def subscribe(self, topic_name: str, topic_method: str, callback_name: str = None, callback_method: str = None):
        if callback_name is None:
            callback_name = self.getFullName()
        if callback_method is None:
            callback_method = to_callback_topic_name(topic_method)
        listener = MRLListener(topic_method, callback_name, callback_method)
        print(str(listener))
        mcommand.sendCommand(topic_name if '@' in topic_name else f"{topic_name}@{runtime.runtime_id}", "addListener",
                             [listener])

    def toString(self):
        return str(self)

    def getId(self):
        return runtime.runtime_id

    def getFullName(self):
        return f"{self.name}@{self.getId()}"

    # Aliases to provide similar API to Java MRL, no functional difference in Python due to single thread design
    invoke = out
    invokeMessage = outMessage
