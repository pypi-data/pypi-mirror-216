'''
Python-equivalent of org.myrobotlab.service.Runtime. Methods that require
the actual MRL runtime instead just call the connected MRL instance, such as createAndStart.
Methods not needing the actual MRL runtime are reimplemented, such as getHelloResponse.
Runtime is a singleton, and so is not written inside of a class, unlike the real Runtime
(since Java requires everything to be a class, even if they are a singleton)
'''


from mrlpy import mcommand

compatMode = False
compatObj = None 

def createAndStart(name, type):
	return mcommand.callService("runtime", "createAndStart", [name, type])
	
	
def shutdown():
	mcommand.sendCommand("runtime", "shutdown", [])

def getRuntime():
	return mcommand.callService("runtime", "start", ["runtime", "Runtime"])

def start(name, type):
        return mcommand.callService("runtime", "start", [name, type])

def setCompat(mode):
	global compatMode
	compatMode = mode

def setCompatServiceObject(obj):
	global compatObj
	compatObj = obj

'''
Remote MRL will call this after we initiate contact, uuid will be unusuable until
we replace it with our own generated uuid for the connected server (useful for multi-server connections
but not for single-server connections)
'''
def getHelloResponse(uuid, request):
	response = {
		"id":"obsidian",
		"request":request,
		"services":[],
	}
	return response
