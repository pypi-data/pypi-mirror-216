import sys
import time
import atexit
import signal
import logging
from mrlpy.exceptions import HandshakeTimeout
from mrlpy import mcommand
from mrlpy import utils
from mrlpy.mevent import Message

"""Represents the base service class"""


class Service (object):
	name = ""

	#DEPRECATED, replaced with built-in handshake procedure
	handshakeSuccessful = False
	handshakeTimeout = 1
	handshakeSleepPeriod = 0.25
	createProxyOnFailedHandshake = True
	proxyClass = "PythonProxy"
	#End deprecated


	__log = logging.getLogger(__name__)


	def __init__(self, name=""):
		'''
		Registers service with mcommand event registers and MRL service registry
		'''

		if name == "":
			try:
				#Get name from args
				self.name = sys.argv[1]
			except IndexError:
				#No first argument
				#Need to auto-generate name
				self.name = utils.genID()
		else:
			self.name = name
		#self.connectWithProxy(True) #Proxy classes are not needed in Nixie
		mcommand.addEventListener(self.name, self.onMessage)
		atexit.register(self.release) #Will release service when Python exits. TODO Check to see if necessary with Messages2 API
		#signal.pause()

	def setProxyClass(self, proxy):
		self.proxyClass = proxy

	#Deprecated, handled in mcommand with builtin handshake facilities
	def connectWithProxy(self, tryagain=False):
		'''
		Utility method used for getting initialization info from proxy and running handshake
		'''
		#Can do this since it won't do anything if proxy already active
		mcommand.sendCommand("runtime", "createAndStart", [self.name, self.proxyClass])
		#Useful for determining whether the proxy service has been created yet
		mrlRet = mcommand.callServiceWithJson(self.name, "handshake", [])
		self.__log.debug("mrlRet = " + str(mrlRet))
		#If we get to here, MRL is running because mcommand did not throw an exception
		#TODO: Use mrlRet to determine if we need to create a proxy service
		#Register this service with MRL's messaging system (Actually, with mcommand's event registers, which forward the event here)
		#Proxy service forwards all messages to mcommand
		mcommand.addEventListener(self.name, self.onMessage)
		#BEGIN HANDSHAKE$
		start = time.time()
		lastTime = 0
		while (not self.handshakeSuccessful) and ((time.time() - start) < self.handshakeTimeout):
			time.sleep(self.handshakeSleepPeriod)
			lastTime = time.time()
			#print str(lastTime - start >= self.handshakeTimeout)
			if lastTime - start >= self.handshakeTimeout:
				if self.createProxyOnFailedHandshake and tryagain:
					self.__log.info("Proxy not active. Creating proxy...")
					mcommand.sendCommand("runtime", "createAndStart", [self.name, "PythonProxy"])
					self.connectWithProxy()
				else:   
					raise HandshakeTimeout("Error attempting to sync with MRL proxy service; Proxy name = " + str(self.name))
		#END HANDSHAKE#

	def onMessage(self, e):
		'''
		Handles message invocation and parsing
		of params; WARNING: DO NOT OVERRIDE
		THIS METHOD UNLESS YOU KNOW WHAT YOU
		ARE DOING!!!!!!!
		'''
		#Enables sending a return value back; Other half implemented in mcommand and proxy service
		ret = None
		#Invoke method with data
		if len(e.data) > 0:
			params = ','.join(map(str, e.data))
			self.__log.debug("Invoking: " + e.method + '(' + params + ')')
			ret = getattr(self, e.method).__call__(*e.data)
		else:
			self.__log.debug("Invoking: " + e.method + '()')
			ret = getattr(self, e.method).__call__()
		self.returnData(ret)

	def returnData(self, dat):
		mcommand.sendCommand(self.name, "returnData", [dat])


	#Deprecated, replaced with built-in handshake in mcommand
	def handshake(self):
		'''
		Second half of handshake.

		Called by proxy during the handshake procedure.
		'''

		self.__log.debug("Handshake successful.")
		self.handshakeSuccessful = True
	def release(self):
		'''
		Utility method for releasing the proxy service;
		Also deletes this service
		'''
		mcommand.sendCommand("runtime", "release", [self.name])
		del self

	def outMessage(self, msg):
		if len(msg.sender) == 0:
			msg.sender = self.name
		mcommand.eventDispatch.dispatch_event(msg)

	def out(self, method, params=[]):
		self.outMessage(Message(self.name, method, params))

	#Aliases to provide similar API to Java MRL, no functional difference in Python due to single thread design
	invoke = out
	invokeMessage = outMessage
