import { Box, Flex, Modal, ModalOverlay, ModalContent, ModalHeader, ModalBody, ModalCloseButton, Button, useDisclosure, Spinner } from '@chakra-ui/react';
import axios from 'axios';
import React, { useEffect, useState } from 'react';
import Swal from 'sweetalert2'

interface AppProps {
  darkMode: boolean;
  nodeArray: any;
}

const NodeItem: React.FC<AppProps> = ({ darkMode,nodeArray }) => {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [ip, setIp] = useState('0.0.0.0');
  const [Localip, setLocalip] = useState('0.0.0.0');
  const [port, setPort] = useState('0');
  const [loading, setLoading] = useState(false);
  const [offline, setOffline] = useState(true);
  const [loadingErr, setLoadingErr] = useState(false);

  useEffect(() => {
    setLoading(true);
    const myHost = sessionStorage.getItem('host');
    axios.get(`${myHost}/bridge/node`)
      .then(response => {
        setLoading(false);
        if (response.data.port > 0 ){
          setOffline(false);
          setLocalip(response.data.localip);
          setIp(response.data.ip);
          setPort(response.data.port)
        }
      })
      .catch(error => {
        console.error(error);
        setLoadingErr(true)
      });
  }, []);


  const Toast = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true,
    didOpen: (toast) => {
      toast.addEventListener('mouseenter', Swal.stopTimer)
      toast.addEventListener('mouseleave', Swal.resumeTimer)
    }
  })

  const handleServer = () => {
    const myHost = sessionStorage.getItem('host');
    onClose();
    setLoading(true);
    axios.post(`${myHost}/bridge/kademlia`, nodeArray)
      .then(response => {
        setLocalip(response.data.localip);
        setIp(response.data.ip);
        setPort(response.data.port)
        setLoading(false);
        setOffline(false);
        Toast.fire({
          icon: 'info',
          title: 'Server settings update in progress. It may take up to 5 minutes to apply'
        })
      })
      .catch(error => {
        console.log(error);
      });
  };
  return (
    <>
      <Flex
        justify="space-between"
        w={{ base: `calc(50% - 10px)`, xl: `calc(33% - 10px)` }}
        h={'100px'}
        borderWidth="2px"
        borderStyle="solid"
        borderColor={darkMode ? "gray.600" : 'gray.300'}
        borderRadius={'20px'}
        _hover={{ cursor: 'pointer' }}
        mr={'10px'}
        mb={'10px'}
        position="relative"
        overflow={'hidden'}
        onClick={onOpen}
        style={{ backgroundColor: offline?'#FDEBD0':'#E8F8F5'}}
      >
        <Flex margin={'0px'} h={'inherit'} w={'100%'} color={darkMode ? "white" : "black"} align="center" pl={'20px'}>
          {loading?
            <Box width={'100%'}>
              <center>
                <Spinner/>
              </center>
            </Box>
          :offline?
          <Box width={'100%'} style={{color: 'red', fontStyle: 'italic' }}>
              <center>
                Offline Node
              </center>
            </Box>
          :
            <Box>
              Host: {ip}
              <Box>
                PORT: {port}
              </Box>
            </Box>
          }
        </Flex>
        <Box
          position="absolute"
          bottom="0"
          right="0"
          w="auto"
          bg={'purple.600'}
          p={'10px 20px'}
          color="white"
          borderTopLeftRadius="20px"
        >
          Boostrap
        </Box>
      </Flex>
      <Modal closeOnOverlayClick={false} isOpen={isOpen} onClose={onClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Boostrap Node Settings</ModalHeader>
          <ModalCloseButton color={'black'}/>
          <ModalBody>
          {loading?
            <Box width={'100%'}>
              <center>
                <Spinner/>
              </center>
            </Box>
          :
          <Box>
            <Box mb="4" display="flex" flexDirection="column">
              <label htmlFor="cartPort">Boostrap Node Host: Public</label>
              <input type="text" id="cartPort" value={ip}/>
            </Box>
            <Box mb="4" display="flex" flexDirection="column">
              <label htmlFor="cartPort">Boostrap Node Host: Private</label>
              <input type="text" id="cartPort" value={Localip}/>
            </Box>
            <Box mb="4" display="flex" flexDirection="column">
              <label htmlFor="mobilePort">Boostrap Node Port:</label>
              <input type="text" id="mobilePort" value={port} />
            </Box>
            <Button w="100%" colorScheme="orange" _hover={{ bg: "orange.700" }} color="white" onClick={handleServer}>Restart Server</Button>
          </Box>
          }
          </ModalBody>
        </ModalContent>
      </Modal>
    </>
  );
};

export default NodeItem;