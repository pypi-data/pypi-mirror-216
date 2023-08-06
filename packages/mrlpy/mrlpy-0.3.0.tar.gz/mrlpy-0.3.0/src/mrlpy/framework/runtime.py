"""
Python-equivalent of org.myrobotlab.service.Runtime. Methods that require
the actual MRL runtime instead just call the connected MRL instance, such as createAndStart.
Methods not needing the actual MRL runtime are reimplemented, such as getHelloResponse.
Runtime is a singleton, and so is not written inside of a class, unlike the real Runtime
(since Java requires everything to be a class, even if they are a singleton)
"""

import logging
from threading import Thread

from mrlpy import mcommand
from mrlpy.framework.interfaces import MRLInterface
from mrlpy.framework.service import Service
from mrlpy.utils import DescribeResults, Registration, MRLListener

runtime_id = "obsidian"


class Runtime(Service):
    compatMode = False
    compatObj = None
    local_registrations = []
    _runtime = None
    __log = logging.getLogger(__name__)

    def __init__(self, name="runtime"):
        self.remote_id = None
        self.listeners = []
        self.post_connect_hooks = []
        self.connected = False
        if Runtime.getRuntime() is not None:
            raise ValueError(
                "Runtime is a singleton and there is already an instance.")
        super().__init__(name)

    @classmethod
    def createAndStart(cls, name, service_type):
        return mcommand.callService("runtime", "createAndStart", [name, service_type])

    @classmethod
    def shutdown(cls):
        mcommand.sendCommand("runtime", "shutdown", [])

    @classmethod
    def getRuntime(cls):
        return cls._runtime

    @classmethod
    def start(cls, name, service_type):
        return mcommand.callService("runtime", "start", [name, service_type])

    @classmethod
    def startService(cls, name, service_type):
        return mcommand.callService("runtime", "startService", [name, service_type])

    def describe(self, uuid="platform", query=None):
        # Add listener for describe
        listener = MRLListener("describe", f"runtime@{runtime_id}", "onDescribe")
        mcommand.sendCommand("runtime", "addListener", [listener], sender="runtime@obsidian")

        # Add listener for registered
        listener = MRLListener("registered", "runtime@obsidian", "onRegistered")
        mcommand.sendCommand("runtime", "addListener", [listener], sender="runtime@obsidian")

        if query is not None:
            self.remote_id = query.id
        self.__log.info("Describing: " + str(query))
        results = DescribeResults()
        results.status = None
        results.id = runtime_id
        results.registrations.extend(Runtime.local_registrations)
        # results.registrations.append(Registration(id=runtime_id, name="runtime",
        #                                           typeKey="org.myrobotlab.service.Runtime", state="{}",
        #                                           interfaces=[]))
        # results.registrations.append(Registration(id=runtime_id, name="native_python", typeKey="py:example_service",
        #                                           state="{}",
        #                                           interfaces=["org.myrobotlab.framework.interfaces.ServiceInterface"]))

        return results

    @classmethod
    def setCompat(cls, mode):
        cls.compatMode = mode

    @classmethod
    def setCompatServiceObject(cls, obj):
        cls.compatObj = obj

    @classmethod
    def init_runtime(cls):
        cls._runtime = Runtime()

    def register(self, registration: Registration):
        self.__class__.local_registrations.append(registration)
        self.invoke("registered", registration)

    @property
    def registration(self):
        type_key = f"org.myrobotlab.service.Runtime"
        interfaces = [superclass.java_interface_name() for superclass in self.__class__.__mro__
                      if isinstance(superclass, MRLInterface)]
        return Registration(id=runtime_id, name=self.name, typeKey=type_key, interfaces=interfaces)

    def registered(self, registration: Registration):
        return registration

    def run_hooks(self):
        for hook in self.post_connect_hooks:
            hook()

    def onRegistered(self, registration: Registration):
        if not self.connected:
            self.connected = True
            Thread(target=self.run_hooks).start()

        self.__log.info(f"Registered service {registration.name}@{registration.id} (type {registration.typeKey})")

    def onDescribe(self, results: DescribeResults):
        self.__log.info(f"Got describe results: {str(results)}")

    # def getHelloResponse(uuid, request):
    #     """
    #     Remote MRL will call this after we initiate contact, uuid will be unusuable until
    #     we replace it with our own generated uuid for the connected server (useful for multi-server connections
    #     but not for single-server connections)
    #     """
    #     response = {
    #         "id": "obsidian",
    #         "request": request,
    #         "services": [],
    #     }
    #     return response
