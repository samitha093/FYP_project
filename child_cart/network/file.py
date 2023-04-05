import os

def getID(newId):
    filename = "./dataset/cashData.txt"
    # Check if file exists, create it if not
    if not os.path.isfile(filename):
        open(filename, 'w').close()
    # Open file and read first line
    with open(filename, 'r') as f:
        first_line = f.readline().strip()
        f.close()
    # Check if first line has data
    if first_line:
        print("USER ID    : ",first_line)
        return first_line
    else:
        print("USER ID    : ",newId)
        WriteData(newId)
        return newId

def WriteData(data):
    file = open("./dataset/cashData.txt","w")
    file.writelines(data)
    file.close()
    return