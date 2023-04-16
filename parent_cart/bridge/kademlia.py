import asyncio
import random
from kademlia.network import Server

class kademlia_network:
    def __init__(self):
        self.server = Server()
        self.event_loop = asyncio.get_event_loop()
        self.port = 0

    def create_bootstrap_node(self,host):
        while True:
            myport = random.randint(49152, 65535)
            try:
                self.event_loop.run_until_complete(self.server.listen(myport))
                print("Boostrap node Stared on : ",myport)
                self.port = myport
                break
            except OSError:
                continue
        try:
            self.event_loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self.event_loop.stop()
            self.event_loop.close()

    def get_port(self):
        return self.port

    async def connect_bootstrap_node(self,bootstrap_ip,bootstrap_port):
        bootstrap_node = (bootstrap_ip, int(bootstrap_port))
        await asyncio.create_task(self.server.bootstrap([bootstrap_node]))
        print("The connection to the distributed network has been successfully established from this node.")

    async def set_data_on_dht(self,key,value):
        await asyncio.create_task(self.server.set(key, value))
        print("DHT Update Successful")

    async def get_data_from_dht(self, key):
        result = await asyncio.create_task(self.server.get(key))
        print("Data : ",result)
        return result

    def getnabourList(self):
        bootstrappable_neighbors = self.server.bootstrappable_neighbors()
        return bootstrappable_neighbors