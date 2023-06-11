import { Box, Flex, Modal, ModalOverlay, ModalContent, ModalHeader, ModalBody, ModalCloseButton, Button, useDisclosure } from '@chakra-ui/react';
import axios from 'axios';
import React, { useEffect, useState } from 'react';

interface AppProps {
  darkMode: boolean;
}

const BridgeModule: React.FC<AppProps> = ({ darkMode }) => {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [cartPort, setCartPort] = useState('9000');
  const [mobilePort, setMobilePort] = useState('8000');
  const [HTTPPort, setHTTPPort] = useState('5000');

  useEffect(() => {
    const myHost = sessionStorage.getItem('host');
    axios.get(`${myHost}/bridge/servers`)
      .then(response => {
        setCartPort(response.data.CARTPORT);
        setMobilePort(response.data.MOBILEPORT);
        setHTTPPort(response.data.HTTPPORT);
      })
      .catch(error => {
        console.error(error);
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
          <Box>
            Cart Server port: {"9000"}
            <Box>
            Mobile Server Port: {"8000"}
            </Box>
          </Box>
        </Flex>
        <Box
          position="absolute"
          bottom="0"
          right="0"
          w="auto"
          bg={'green.500'}
          p={'10px 20px'}
          color="white"
          borderTopLeftRadius="20px"
        >
          Bridge
        </Box>
      </Flex>
      <Modal closeOnOverlayClick={false} isOpen={isOpen} onClose={onClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Bridge Module Settings</ModalHeader>
          <ModalCloseButton color={'black'}/>
          <ModalBody>
            <Box mb="4" display="flex" flexDirection="column">
              <label htmlFor="cartPort">Cart Server port:</label>
              <input type="text" id="cartPort" value={cartPort}/>
            </Box>
            <Box mb="4" display="flex" flexDirection="column">
              <label htmlFor="mobilePort">Mobile Server Port:</label>
              <input type="text" id="mobilePort" value={mobilePort}/>
            </Box>
            <Box mb="4" display="flex" flexDirection="column" position="relative">
              <label htmlFor="HTTPPort">HTTP Server Port:</label>
              <input type="text" id="HTTPPort" value={HTTPPort} />
            </Box>
          </ModalBody>
        </ModalContent>
      </Modal>
    </>
  );
};

export default BridgeModule;