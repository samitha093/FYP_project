from enum import Enum

class errMsg(Enum):
    MSG001 = "Socket connections are being disrupted."
    MSG002 = "Error connecting to socket"
    MSG003 = "Error : no existing socket connection established"
    MSG004 = "SHELL type connection established"
    MSG005 = "Data receiving ....."
    MSG006 = "Data received done."
    MSG007 = "Data Processing Started."
    MSG008 = "RECIVED DATA FROM : "
    MSG009 = "Cant Send more than 5MB data file "
    MSG010 = "OVERLOADED DATAPACK FOUND : "