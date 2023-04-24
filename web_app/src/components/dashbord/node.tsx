import { Box, Flex, Modal, ModalOverlay, ModalContent, ModalHeader, ModalBody, ModalCloseButton, Button, useDisclosure } from '@chakra-ui/react';
import axios from 'axios';
import React, { useEffect, useState } from 'react';

interface AppProps {
  darkMode: boolean;
}

const NodeItem: React.FC<AppProps> = ({ darkMode }) => {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [ip, setIp] = useState('192.168.34.56');
  const [port, setPort] = useState('55687');
  const [ipError, setIpError] = useState('');
  const [portError, setPortError] = useState('');

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
  useEffect(() => {
    const myHost = sessionStorage.getItem('host');
    axios.get(`${myHost}/bridge/node`)
      .then(response => {
        setIp(response.data.ip);
        setPort(response.data.port)
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
            Host: {ip}
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
          bg={'purple.600'}
          p={'10px 20px'}
          color="white"
          borderTopLeftRadius="20px"
        >
          B-Node
        </Box>
      </Flex>
    </>
  );
};

export default NodeItem;