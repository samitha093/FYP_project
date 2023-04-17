import { AddIcon } from '@chakra-ui/icons';
import { Box, Center, Flex, Modal, ModalOverlay, ModalContent, ModalHeader, ModalBody, ModalCloseButton, Button, useDisclosure } from '@chakra-ui/react';
import { useState } from 'react';

interface AppProps {
  darkMode: boolean;
  handledataSave:any;
}

const New: React.FC<AppProps> = ({ darkMode, handledataSave }) => {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [ip, setIp] = useState('');
  const [port, setPort] = useState('');
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
    handledataSave({"ip":ip,"port":port})
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
        align="center"
        w={{ base: `calc(50% - 10px)`, xl: `calc(33% - 10px)` }}
        h="100px"
        borderWidth="5px"
        borderStyle="dashed"
        borderColor={darkMode ? "gray.600" : 'gray.300'}
        borderRadius="20px"
        justifyContent="center"
        _hover={{ cursor: 'pointer' }}
        onClick={onOpen}
      >
        <Center margin="30px" h="inherit" w="inherit" color="white">
          <AddIcon w={6} h={6} color={darkMode ? "gray.600" : 'gray.300'} />
        </Center>
      </Flex>
      <Modal closeOnOverlayClick={false} isOpen={isOpen} onClose={onClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Conect with new node</ModalHeader>
          <ModalCloseButton color={'black'}/>
          <ModalBody>
            <Box mb="4" display="flex" flexDirection="column">
              <label htmlFor="ip">Host Address:</label>
              <input type="text" id="ip" value={ip} onChange={handleIpChange} />
              {ipError && <Box color="red">{ipError}</Box>}
            </Box>
            <Box mb="4" display="flex" flexDirection="column">
              <label htmlFor="port">Port:</label>
              <input type="text" id="port" value={port} onChange={handlePortChange} />
              {portError && <Box color="red">{portError}</Box>}
            </Box>
            <Button w="100%" colorScheme="green" _hover={{ bg: "green.700" }} color="white" onClick={handleSave}>Save</Button>
          </ModalBody>
        </ModalContent>
      </Modal>
    </>
  );
};
export default New;