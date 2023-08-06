from mrlpy.framework.service import Service


# This is an example service. To create it, you MUST have an MRL instance running and mrlpy configured to connect To
# create, either run python exampleService.py or, in MRL, create a proxy and call proxy.startNativeService() with the
# location of this script as the argument
class ExampleService(Service):

	# Basic constructor of service, should have this signature but not required
	def __init__(self, name=""):
		# REALLY REALLY REALLY IMPORTANT TO CALL THIS, otherwise service is not registered, name not allocated,
		# everything blows up
		super(ExampleService, self).__init__(
			name)  # If name is empty string, then it is taken from the first command-line argument.  If there is no

	# such argument, then the name is auto-generated

	# Normal method declarations. MService handles messaging and invocation of methods, so nothing special is needed
	def doSomething(self):
		print("Doing something interesting")


# etc.


# This allows the service to be created when calling on the command line
if __name__ == "__main__":
	ExampleService()
