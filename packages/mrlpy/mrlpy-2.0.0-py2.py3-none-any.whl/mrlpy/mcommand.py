#!/usr/bin/env python

""" Created on May 17, 2017

This module represents the low-level command API
for a running MRL instance.
				###########
				ERROR CODES
		0: Success
		1: Incorrect usage from command line
		2: Unable to connect to MRL instance

  sendCommandQuick() and sendCommand()
		return all codes except 1


@author: AutonomicPerfectionist
"""
import logging
import signal
from socket import error as WebSocketError

import websocket

from mrlpy.framework.serializer import PolymorphicEncoder, encode

try:
    import thread
except ImportError:
    import _thread  # For python3 compatibility
import time
import os
import sys
import threading
import json
import requests

from json import JSONEncoder

from mrlpy import utils
from mrlpy.meventdispatch import MEventDispatch
from mrlpy.proxy import Proxy
from mrlpy.framework.deserializer import loads

useEnvVariables = True
MRL_URL = "localhost"

MRL_PORT = '8888'
"""
Port of MRL; MUST be a string
"""

eventDispatch = MEventDispatch()
utils.eventDispatch = eventDispatch
socket = None
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)
apiType = "messages"

serverInfo = dict()


class DefaultEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


def connect(bypassRegisters=False, forceReconnect=False, id=None, daemon=True, timeout=5):
    """
    Connects to MRL instance
    Returns True if successful, False otherwise
    """
    global socket
    global MRL_URL
    global MRL_PORT
    global useEnvVariables

    if useEnvVariables:
        MRL_URL = os.getenv('MRL_URL', MRL_URL)
        MRL_PORT = os.getenv('MRL_PORT', MRL_PORT)

    if socket is not None and forceReconnect:
        close()

    if socket is None or socket.sock is None or forceReconnect:
        url = "ws://" + MRL_URL + ':' + MRL_PORT + '/api/' + \
              apiType + (("?id=" + str(id)) if id is not None else "")
        if bypassRegisters:
            try:
                socket = websocket.create_connection(url)
            except WebSocketError as we:
                log.error("MRL is not online for URL " +
                          MRL_URL + ":" + MRL_PORT)
                raise WebSocketError(
                    we, "MRL is not online for URL " + MRL_URL + ":" + MRL_PORT)

        else:
            socket = websocket.WebSocketApp(url,
                                            on_message=on_message,
                                            on_error=on_error,
                                            on_close=on_close)
            socket.on_open = on_open
            wst = threading.Thread(target=socket.run_forever)
            wst.daemon = daemon
            wst.start()
            conn_timeout = timeout
            time.sleep(0.1)
            if socket is None or socket.sock is None:
                raise WebSocketError(
                    "MRL is not online for URL " + MRL_URL + ":" + MRL_PORT)
            try:
                while not socket.sock.connected and conn_timeout:
                    time.sleep(1)
                    conn_timeout -= 1
            except Exception as we:
                raise WebSocketError(
                    we, "MRL is not online for URL " + MRL_URL + ":" + MRL_PORT)
        # Begin handshake#
        # sendCommand("runtime", "getHelloResponse", ["figure-it-out", HelloRequest("obsidian", "FIGURE-IT-OUT").__dict__])
    return True


def sendCommand(name, method, dat, sender=""):
    """
    Sends a command to MRL

    Initializes socket so that the connection is held;
    Equivalent to sendCommandQuick() if socket has
    already been initialized
    """

    global MRL_URL
    global MRL_PORT
    global socket

    connect()
    return send(name, method, dat, sender)


def sendCommandQuick(name, method, dat):
    """
    Sends a command to MRL

    Sends a command, and if socket is not
    initialized, will create a quick
    connection that bypasses event registers
    """

    global MRL_URL
    global MRL_PORT
    global socket
    # if socket == None:
    # 	try :
    # 		socket = websocket.create_connection("ws://" + MRL_URL + ':' + MRL_PORT + '/api/messages')
    # 	except Exception:
    # 		log.error("MRL is not online for URL " + MRL_URL + ":" + MRL_PORT)
    # 		return 2
    connect(bypassRegisters=True)
    # req = '{"name": ' + name + ', "method": ' + method + ', "data": ' + str(dat) + '}'
    # ret = socket.send(req)
    return send(name, method, dat)


def isSequence(arg):
    """
    Returns True if arg is a sequence and False if string, dict, or otherwise
    """
    return (not hasattr(arg, "strip") and
            (not hasattr(arg, "values")) and
            (hasattr(arg, "__getitem__") or
             hasattr(arg, "__iter__")))


def parseRet(ret):
    """
    Will look at ret (return value from callServiceWithJson)
    and convert it to Python types
    """
    if isSequence(ret):
        tmpRet = []
        for val in ret:
            tmpRet.append(parseRet(val))
        return tmpRet
    else:

        # Not a sequence, so can be string, int, json, dict, etc.
        if isinstance(ret, str):
            return ret
        else:
            if type(ret) is dict:
                if 'serviceType' in ret:
                    return genProxy(ret)
                else:
                    return ret
            else:
                # ret is not string or dictionary
                return ret


def callServiceWithJson(name, method, dat):
    """
    Calls a service's method with data as params.

    Returns json
    """

    global MRL_URL
    global MRL_PORT

    dat_formed = list(dat)
    params = encode(dat_formed)
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    r = requests.post(f"http://{MRL_URL}:{MRL_PORT}/api/service/{name}/{method}", data=params,
                      headers=headers)
    log.debug(f"Data formed: {dat_formed}")

    try:
        return r.json()
    except Exception:
        return r.text


def callService(name, method, dat):
    """
    Calls a service's methods with data as params.

    Returns what the method returns, and creates a proxy service if service returned.
    """

    retFromMRL = callServiceWithJson(name, method, dat)
    return parseRet(retFromMRL)


def callServiceWithVarArgs(*args):
    """
    Same as callService() except data doesn't have to be in a list

    Returns what callService() returns
    """

    name = args[0]
    method = args[1]
    dat = list(args)[2:]
    return callService(name, method, dat)


def send(name, method, dat, sender=""):
    """
    Send json to MRL (INTERNAL USE ONLY!)
    """

    global socket
    try:
        # Need to "double encode," encode each param then encode container
        tempData = list()
        for d in dat:
            tempData.append(encode(d))
        req = encode({"name": name, "method": method,
                      "data": tempData, "sender": sender, "class": "org.myrobotlab.framework.Message"})

        ret = socket.send(req)
        return ret

    except WebSocketError as e:  # CHANGE TO CORRECT EXCEPTION TYPE FOR NETWORK ERRORS
        log.error("MRL is not online for URL " + MRL_URL + ":" + MRL_PORT)
        raise WebSocketError(e, "MRL is not online for URL " + MRL_URL + ":" + MRL_PORT)


def getURL():
    global MRL_URL
    return MRL_URL


def setURL(url):
    """
    Self-explanatory; Use INSTEAD of directly setting URL
    """
    global MRL_URL
    global useEnvVariables
    MRL_URL = url
    useEnvVariables = False


def getPort():
    global MRL_PORT
    return MRL_PORT


def setPort(port):
    """
    Self-explanatory; Use INSTEAD of directly setting port
    """
    global MRL_PORT
    global useEnvVariables
    MRL_PORT = str(port)
    useEnvVariables = False


###################################
#	START EVENT REGISTERS		#
###################################


def on_error(ws, error):
    """
    Error event register; called
    by socket on errors
    """
    log.error(error)


def on_close(ws, close_status_code, close_msg):
    """
    Called by socket on closing
    """
    log.info("### Closed socket ###")
    log.debug(f"Close status code: {close_status_code}")
    log.debug(f"Close message: {close_msg}")


def on_open(ws):
    """
    Called by socket when opening
    """
    log.info("### Opened socket ###")


def close():
    """
    Utility function for forcefully closing the connection
    """

    global socket
    if socket is not None:
        socket.close()


def addEventListener(name, l):
    """
    Add a listener to topic (name); Normally
    used for registering a service's name to the
    event registers
    """
    # print "Adding event listener: name=" + name + ", l=" + str(l)
    logging.info(f"Adding event listener on topic {name}: {l}")
    eventDispatch.add_event_listener(name, l)


def removeEventListener(name, l):
    """
    Removes listener l from topic name
    """
    eventDispatch.remove_event_listener(name, l)


def hasEventListener(name, l):
    """
    Returns true if l is a listener for topic name, false otherwise.
    """

    return eventDispatch.has_listener(name, l)


def on_message(ws, msg):
    """
    Primary event register. Everything goes through here

    Parses message. If a heartbeat, updates heartbeat register.
    Else, create mrlMessage and dispatch.
    """
    if msg == "X":
        log.debug("Heartbeat received: " + str(msg))
    else:
        eventDispatch.dispatch_event(loads(msg))


################################
#	  END EVENT REGISTERS	 #
################################

def __keyboardExit(signal, frame):
    log.info("KeyboardInterrupt... Shutting down")
    sys.exit(0)


# Don't do this, if python service is subscribed to any other service this will cause that service to be released as
# well def __del__(self): ''' Releases all proxy services on delete. '''

#	for type, serv in eventDispatch._events.iteritems():
#		self.sendCommand("runtime", "release", [serv.name])


'''
Caching proxy classes. Keyed with simpleName + "_Proxy"
'''
proxies = dict()

'''
Cachine proxy instances. Keyed with service name
'''
proxyInstances = dict()

'''
Used for generating proxy classes by inputting json.
'''


def MClassFactory(qualName, methods, BaseClass=Proxy):
    def __init__(self, simpleName, name):
        BaseClass.__init__(self, simpleName, name)

    newclass = type(str(qualName), (BaseClass,), dict(
        {"__init__": __init__}, **methods))
    return newclass


def methodListToDict(names, methods):
    if len(names) != len(methods):
        raise ValueError(
            "The size of names and methods must be equivalent; Mapping cannot continue!")
    ret = {}
    for x in range(0, len(names) - 1):
        ret.update({names[x]: methods[x]})
    return ret


def genProxy(data):
    """
    Generate proxy service class
    """
    log.debug("Generating proxy")
    global proxies
    # Fully-qualified class name
    qualName = str(data['serviceClass'])

    simpleName = str(data['simpleName'] + '_Proxy')

    # Service's name
    name = str(data['name'])

    # List of the service's methods, for which the proxy service's will be created from
    methodList = callService(name, 'getMethodNames', [])

    proxyMethods = list(map(lambda x: lambda self, *args: callService(name,
                                                                      x, list(args) if len(args) > 0 else []),
                            methodList))

    methodDict = methodListToDict(methodList, proxyMethods)
    proxies[simpleName] = MClassFactory(simpleName, methodDict)
    proxyInstances[name] = proxies[simpleName](simpleName, name)

    for methodName in methodDict:
        bind(proxyInstances[name], methodDict[methodName], methodName)
    return proxyInstances[name]


def bind(instance, func, asname): return setattr(
    instance, asname, func.__get__(instance, instance.__class__))


# Statements to run during import


if __name__ == "__main__":
    # Silences KeyboardInterrupt stacktrace and logs the interrupt, then exits
    signal.signal(signal.SIGINT, __keyboardExit)

    MRL_URL = os.getenv('MRL_URL', MRL_URL)
    MRL_PORT = os.getenv('MRL_PORT', MRL_PORT)
    logging.basicConfig()
    if len(sys.argv) < 3:
        print("Usage: mcommand <name> <method> <dat>")
        exit(1)
    # websocket.enableTrace(True)
    try:
        ret = callService(sys.argv[1], sys.argv[2], sys.argv[3:])
        print(ret)
    except WebSocketError as e:
        log.error("Connection failed.")
        exit(2)
    close()
    exit(0)
