# Written for MRL's Python service To run in mrlpy, pass this script's location to the constructor of
# mrlpy.mcompat.MCompatibilityService or on the command line to mcompat-run ex: $ mcompat-run
# ~/mrlpy/examples/exampleCompatScript.py OR: compat = MCompatibilityService("~/mrlpy/examples/exampleCompatScript.py")


ard = Runtime.createAndStart("ard", "Arduino")
ard.connect("/dev/ttyUSB0")

# etc.
