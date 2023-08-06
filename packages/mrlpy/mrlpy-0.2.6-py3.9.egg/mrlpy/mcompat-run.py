#!/usr/bin/python

from mrlpy.mcompat import MCompatibilityService
from mrlpy import utils
import sys

'''
Utility script for running scripts in compatibility mode
'''

if __name__ == "__main__":
    numArgs = len(sys.argv)
    if numArgs < 2:
        print("Usage: mcompat-run <scriptfile>.py <optional: name>")
        exit(1)
    name = ""
    if numArgs < 3:
        name = "MCompatService-" + utils.genID(15)
    m = MCompatibilityService(name)
    m.runScript(sys.argv[1])
