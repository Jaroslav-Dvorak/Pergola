from rs485 import EPever

publ = EPever.publ

@service
def hello_world(action=None, id=None):
    task.unique("publ", kill_me=True)
    task.executor(publ, None)
