import asyncio
import json
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

    def create_bootstrap_node(self,myport,kademlaNodeList,bootstrap_ip='127.0.0.1',bootstrap_port='63524'):
        # self.event_loop.set_debug(True)
        data_string = kademlaNodeList.decode('utf-8')
        dataDic = json.loads(data_string)

        while True:
            self.isAvailabale = True
            try:
                ## create boostrap node
                self.event_loop.run_until_complete(self.server.listen(myport))
                print("Boostrap node Stared on : ",myport)
                ## conect with boostrap nodes
                for item in dataDic:
                    port = item['port']
                    ip = item['ip']
                    bootstrap_node = (ip, int(port))
                    self.event_loop.run_until_complete(self.server.bootstrap([bootstrap_node]))
                    print(f"IP: {ip}, Port: {port} = > node conected")
                break
            except OSError:
                continue
        try:
            self.event_loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            print("Stoped Kademlia server ")

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
