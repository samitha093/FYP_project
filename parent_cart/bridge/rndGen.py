import random
import string

existing_ids = []

#genarate user id and clusterid
def generateId(id_length=8):
    global existing_ids
    while True:
        # Generate a random ID string
        id_str = ''.join(random.choices(string.ascii_letters + string.digits, k=id_length))
        # Check if the ID is unique
        if id_str not in existing_ids:
            # Add the ID to the list of existing IDs
            existing_ids.append(id_str)
            return id_str