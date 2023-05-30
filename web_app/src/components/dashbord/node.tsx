import { Box, Flex, Modal, ModalOverlay, ModalContent, ModalHeader, ModalBody, ModalCloseButton, Button, useDisclosure, Spinner } from '@chakra-ui/react';
import axios from 'axios';
import React, { useEffect, useState } from 'react';

interface AppProps {
  darkMode: boolean;
}

const NodeItem: React.FC<AppProps> = ({ darkMode }) => {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [ip, setIp] = useState('192.168.34.56');
  const [Localip, setLocalip] = useState('192.168.34.57');
  const [port, setPort] = useState('55687');
  const [loading, setLoading] = useState(true);
  const [loadingErr, setLoadingErr] = useState(false);

  useEffect(() => {
    setLoading(true);
    const myHost = sessionStorage.getItem('host');
    axios.get(`${myHost}/bridge/node`)
      .then(response => {
        setLoading(false);
        setLocalip(response.data.localip);
        setIp(response.data.ip);
        setPort(response.data.port)
      })
      .catch(error => {
        console.error(error);
        setLoadingErr(true)
      });
  }, []);
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
      >
        <Flex margin={'0px'} h={'inherit'} w={'100%'} color={darkMode ? "white" : "black"} align="center" pl={'20px'}>
          {loading?
            <Box width={'100%'}>
              <center>
                <Spinner/>
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
          </Box>
          }
          </ModalBody>
        </ModalContent>
      </Modal>
    </>
  );
};

export default NodeItem;