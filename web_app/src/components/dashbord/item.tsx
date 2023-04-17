import { Box, Flex, Modal, ModalOverlay, ModalContent, ModalHeader, ModalBody, ModalCloseButton, Button, useDisclosure } from '@chakra-ui/react';
import React, { useEffect, useState } from 'react';

interface AppProps {
  darkMode: boolean;
  data:any;
}

const Item: React.FC<AppProps> = ({ darkMode, data }) => {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [ip, setIp] = useState('192.168.34.56');
  const [port, setPort] = useState('55687');
  const [ipError, setIpError] = useState('');
  const [portError, setPortError] = useState('');

  useEffect(() => {
    setIp(data.ip);
    setPort(data.port);
  }, []);

  const handleSave = () => {
    if (!ip || !port) {
        setIpError(ip ? '' : 'IP address is required');
        setPortError(port ? '' : 'Port number is required');
        return;
      }
  
      if (!/^(\d{0,2}|1\d{0,2}|2[0-4]\d|25[0-5])(\.(\d{0,2}|1\d{0,2}|2[0-4]\d|25[0-5])){3}$/.test(ip)) {
        setIpError('Invalid IP address');
        return;
      }
  
      if (!/^\d+$/.test(port) || parseInt(port, 10) <= 0 || parseInt(port, 10) > 65535) {
        setPortError('Invalid port number');
        return;
      }
    // Handle saving IP and port
    onClose();
  };

  const handleIpChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    if (/^(\d{0,2}|1\d{0,2}|2[0-4]\d|25[0-5])(\.(\d{0,2}|1\d{0,2}|2[0-4]\d|25[0-5])){0,3}$/.test(value)) {
      setIp(value);
    }
    setIpError('');
  };

  const handlePortChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    if (value === '' || (/^\d+$/.test(value) && parseInt(value, 10) > 0 && parseInt(value, 10) <= 65535)) {
      setPort(value);
    }
    setPortError('');
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
            Remote Host: {ip}
            <Box>
              PORT: {port}
            </Box>
          </Box>
        </Flex>
        <Box
          position="absolute"
          bottom="0"
          right="0"
          w="auto"
          bg={'green.700'}
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
          <ModalHeader>Boostrap link config</ModalHeader>
          <ModalCloseButton color={'black'}/>
          <ModalBody>
            <Box mb="4" display="flex" flexDirection="column">
              <label htmlFor="ip">IP:</label>
              <input type="text" id="ip" value={ip} onChange={handleIpChange} />
              {ipError && <Box color="red">{ipError}</Box>}
            </Box>
            <Box mb="4" display="flex" flexDirection="column">
              <label htmlFor="port">Port:</label>
              <input type="text" id="port" value={port} onChange={handlePortChange} />
              {portError && <Box color="red">{portError}</Box>}
            </Box>
            <Button w="100%" colorScheme="green" _hover={{ bg: "green.700" }} color="white" onClick={handleSave}>Update</Button>
          </ModalBody>
        </ModalContent>
      </Modal>
    </>
  );
};

export default Item;