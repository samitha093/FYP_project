import { Box, Flex, Modal, ModalOverlay, ModalContent, ModalHeader, ModalBody, ModalCloseButton, Button, useDisclosure } from '@chakra-ui/react';
import axios from 'axios';
import React, { useEffect, useState } from 'react';

interface AppProps {
  darkMode: boolean;
}

const Tcpitem: React.FC<AppProps> = ({ darkMode }) => {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [remoteHost, setRemoteHost] = useState('192.168.34.56');
  const [localHost, setLocalHost] = useState('192.168.34.56');
  const [port, setPort] = useState('9000');
  const [Ktimeout, setKtimeout] = useState(60);
  const [Stimeout, setStimeout] = useState(180);
  const [SyncConstant, setSyncConstant] = useState(1);

  useEffect(() => {
    axios.get('http://127.0.0.1:5001/network/config')
      .then(response => {
        setRemoteHost(response.data.message.HOST);
        setLocalHost(response.data.message.LOCALHOST);
        setPort(response.data.message.PORT);
        setKtimeout(response.data.message.KERNAL_TIMEOUT);
        setStimeout(response.data.message.SHELL_TIMEOUT);
        setSyncConstant(response.data.message.SYNC_CONST)
      })
      .catch(error => {
        console.error(error);
      });
  }, []);

  const handleSave = () => {
    // Handle saving IP and port
    onClose();
  };

  const handleRemoteHostChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setRemoteHost(value);
  };

  const handleLocalHostChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setLocalHost(value);
  };

  const handlePortChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setPort(value);
  };

  const handleKtimeout = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setKtimeout(parseInt(value));
  };
  const handleStimeout = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setStimeout(parseInt(value));
  };
  const handleSyncConstant = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setSyncConstant(parseInt(value));
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
      >
        <Flex margin={'0px'} h={'inherit'} w={'100%'} color={darkMode ? "white" : "black"} align="center" pl={'20px'}>
          <Box>
            Remote Host: {remoteHost}
            <Box>
              Local Host: {localHost}
            </Box>
          </Box>
        </Flex>
        <Box
          position="absolute"
          bottom="0"
          right="0"
          w="auto"
          bg={'orange.500'}
          p={'10px 20px'}
          color="white"
          borderTopLeftRadius="20px"
        >
          TCP:{port}
        </Box>
      </Flex>
      <Modal closeOnOverlayClick={false} isOpen={isOpen} onClose={onClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Network Module Settings</ModalHeader>
          <ModalCloseButton color={'black'}/>
          <ModalBody>
            <Box mb="4" display="flex" flexDirection="column">
              <label htmlFor="remoteHost">Remote Host:</label>
              <input type="text" id="remoteHost" value={remoteHost} onChange={handleRemoteHostChange} />
            </Box>
            <Box mb="4" display="flex" flexDirection="column">
              <label htmlFor="localHost">Local Host:</label>
              <input type="text" id="localHost" value={localHost} onChange={handleLocalHostChange} />
            </Box>
            <Box mb="4" display="flex" flexDirection="column" position="relative">
              <label htmlFor="localHost">Kernal Timeout:</label>
              <input type="text" id="localHost" value={Ktimeout} onChange={handleKtimeout} />
              <span style={{ position: 'absolute', right: '10px', bottom: '10px' }}>second</span>
            </Box>
            <Box mb="4" display="flex" flexDirection="column" position="relative">
                <label htmlFor="localHost">Shell Timeout:</label>
                <input type="text" id="localHost" value={Stimeout} onChange={handleStimeout} />
                <span style={{ position: 'absolute', right: '10px', bottom: '10px' }}>second</span>
            </Box>
            <Box mb="4" display="flex" flexDirection="column">
              <label htmlFor="localHost">Sync. Constant:</label>
              <input type="text" id="localHost" value={SyncConstant} onChange={handleSyncConstant} />
            </Box>
            <Box mb="4" display="flex" flexDirection="column">
              <label htmlFor="port">Port:</label>
              <input type="text" id="port" value={port} onChange={handlePortChange} />
            </Box>
            <Button w="100%" colorScheme="orange" _hover={{ bg: "orange.700" }} color="white" onClick={handleSave}>Update</Button>
          </ModalBody>
        </ModalContent>
      </Modal>
    </>
  );
};

export default Tcpitem;