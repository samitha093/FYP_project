from enum import Enum



class peerType(Enum):
    SERVER = "SERVER"

class conctionType(Enum):
    SEED = "SEED" #send and recive modela
    KERNEL = "KERNEL" #send modela
    SHELL = "SHELL" #recive modela