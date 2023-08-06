from abc import ABC, abstractmethod


class MRLInterface(ABC):

    @classmethod
    @abstractmethod
    def java_interface_name(cls) -> str:
        pass


class ServiceInterface(MRLInterface, ABC):

    @classmethod
    def java_interface_name(cls):
        return "org.myrobotlab.framework.interfaces.ServiceInterface"
