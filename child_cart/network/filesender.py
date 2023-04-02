def partDevider(sock, serialized_data):
    MAX_CHUNK_SIZE = 1024
    chunks = [serialized_data[i:i+MAX_CHUNK_SIZE] for i in range(0, len(serialized_data), MAX_CHUNK_SIZE)]
    print("NO OF CHUNKS : ",len(chunks))
    for x in chunks:
        sock.send(x)


def PartModel(msgFrom,msgTo, data, MsgID, NoOfParts, PartID):
    modelparametersPart = ["MODELPARAMETERS",data]
    return {
        'Sender':msgFrom,
        'Receiver': msgTo,
        'MsgID': MsgID,
        'NoOfParts': NoOfParts,
        'PartID': PartID,
        'Data':modelparametersPart
    }