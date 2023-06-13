import { Box, Flex, Modal, ModalOverlay, ModalContent, ModalHeader, ModalBody, ModalCloseButton, Button, useDisclosure } from '@chakra-ui/react';
import axios from 'axios';
import React, { useEffect, useState } from 'react';
import Swal from 'sweetalert2'

interface AppProps {
  darkMode: boolean;
  data:any;
  handledataremove:any;
  handlerdataUpdate:any;
}

const Item: React.FC<AppProps> = ({ darkMode, data, handledataremove, handlerdataUpdate }) => {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [ip, setIp] = useState('192.168.34.56');
  const [port, setPort] = useState('55687');
  const [ipError, setIpError] = useState('');
  const [portError, setPortError] = useState('');
  const [index, setindex] = useState(0);

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

  useEffect(() => {
    setIp(data.ip);
    setPort(data.port);
    setindex(data.index)
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
    handlerdataUpdate({"index":index,"ip":ip,"port":port})
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

  const handleCloseClick = () => {
    Swal.fire({
      title: 'Are you sure?',
      text: "Do you need delete this boostrap node",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Yes, delete it!'
    }).then((result) => {
      if (result.isConfirmed) {
        handledataremove(index)
        Toast.fire({
          icon: 'success',
          title: 'Removed boostrap node'
        })
      }
    })

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
      >
        <Flex margin={'0px'} h={'inherit'} w={'100%'} color={darkMode ? "white" : "black"} align="center" pl={'20px'} onClick={onOpen}>
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
        <Box
          position="absolute"
          top="0"
          right="0"
          w="auto"
          p={'10px 20px'}
          color="red"
          onClick={handleCloseClick}
        >
          X
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