from mrlpy import mcommand
from mrlpy.framework.runtime import Runtime
from mrlpy.framework.service import Service

Runtime.init_runtime()


class ExampleService(Service):
    def __init__(self, name):
        super().__init__(name)


def connection_done():
    print("Connection done")
    ex = ExampleService("native_python")
    print(ex)
    # print(mcommand.callService("runtime", "start", ["python", "Python"]))


Runtime.getRuntime().post_connect_hooks.append(connection_done)

mcommand.setPort("8888")
mcommand.connect(id="obsidian", daemon=False)

# mcommand.connect(daemon=False, bypassRegisters=True)
# mcommand.sendCommand("runtime", "describe", [])
# p = mcommand.callService("runtime", "start", ["python", "Python"])
# print(p)
# print(p.__dict__)
