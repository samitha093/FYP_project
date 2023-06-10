import asyncio
import random
import logging
from kademlia.network import Server

# handler = logging.StreamHandler()
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# log = logging.getLogger('kademlia')
# log.addHandler(handler)
# log.setLevel(logging.DEBUG)

class kademlia_network:
    def __init__(self):
        self.server = Server()
        self.event_loop = asyncio.new_event_loop()
        self.isAvailabale = False

    def create_bootstrap_node(self,myport):
        # self.event_loop.set_debug(True)
        while True:
            # myport = random.randint(49152, 65535)
            self.isAvailabale = True
            try:
                self.event_loop.run_until_complete(self.server.listen(myport))
                print("Boostrap node Stared on : ",myport)
                break
            except OSError:
                continue
        try:
            self.event_loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            print("Stoped Kademlia server ")

    async def connect_bootstrap_node(self,bootstrap_ip,bootstrap_port):
        bootstrap_node = (bootstrap_ip, int(bootstrap_port))
        await asyncio.create_task(self.server.bootstrap([bootstrap_node]))
        print("The connection to the distributed network has been successfully established from this node.")

    async def getnabourList(self):
        bootstrappable_neighbors = self.server.bootstrappable_neighbors()
        return bootstrappable_neighbors
    
    async def set_data_on_dht(self,key,value):
        await asyncio.create_task(self.server.set(key, value))
        print("DHT Update Successful")

    async def get_data_from_dht(self, key):
        result = await asyncio.create_task(self.server.get(key))
        print("Data : ",result)
        return result
    
    def ServerStatus_bootstrap_node(self):
        return self.isAvailabale
    
    def stop_server(self):
        self.server.stop()
        self.event_loop.stop()
        self.isAvailabale = False
