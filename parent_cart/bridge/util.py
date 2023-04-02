def requestModel(msgTo, data,msgFrom = "SERVER"):
    return {
        'Sender':msgFrom,
        'Receiver': msgTo,
        'Data':data
    }
