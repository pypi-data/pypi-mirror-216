import logging
from mrlpy.framework.service import Service


# This is an example service. To create it, you MUST have an MRL instance running and mrlpy configured to connect To
# create, either run python exampleService.py or, in MRL, create a proxy and call proxy.startNativeService() with the
# location of this script as the argument
class _TemplateProxy(Service):
    log = logging.getLogger(__name__)

    # Basic constructor of service, should have this signature but not required
    def __init__(self, name=""):
        # Overrides default proxy class of PythonProxy, allowing a custom proxy to be used instead
        super(_TemplateProxy, self).setProxyClass(type(self).__name__)
        # REALLY REALLY REALLY IMPORTANT TO CALL THIS, otherwise service is not registered, name not allocated,
        # everything blows up
        super(_TemplateProxy, self).__init__(
            name)  # If name is empty string, then it is taken from the first command-line argument.  If there is no

    # such argument, then the name is auto-generated

    # Normal method declarations. MService handles messaging and invocation of methods, so nothing special is needed
    def doSomething(self):
        self.__log.info("Doing something interesting")

    def test(self):
        return "Hello!"


# This allows the service to be created when calling on the command line
if __name__ == "__main__":
    _TemplateProxy()
