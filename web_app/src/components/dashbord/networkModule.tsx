import { Box, Flex, Modal, ModalOverlay, ModalContent, ModalHeader, ModalBody, ModalCloseButton, Button, useDisclosure, Spacer } from '@chakra-ui/react';
import axios from 'axios';
import Swal from 'sweetalert2'
import React, { useEffect, useState } from 'react';
import Loading from '../module/loading';

interface AppProps {
  darkMode: boolean;
}

const NetworkModule: React.FC<AppProps> = ({ darkMode }) => {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [remoteHost, setRemoteHost] = useState('0.0.0.0');
  const [localHost, setLocalHost] = useState('0.0.0.0');
  const [port, setPort] = useState('0');
  const [APIport, setApiPort] = useState('5001');
  const [ClusterSize, setClusterSize] = useState('0');
  const [SyncConstant, setSyncConstant] = useState(0);
  const [DeviceIp, setDeviceIp] = useState('0.0.0.0');
  const [loadingVisible, setLoadingVisible] = useState(false);
  const [PALREQ, setPALREQ] = useState(0);

    // Function to show the loading component
    const showLoading = () => {
      setLoadingVisible(true);
    };

    // Function to hide the loading component
    const hideLoading = () => {
      setLoadingVisible(false);
    };
  useEffect(() => {
    showLoading()
    const myHost = sessionStorage.getItem('host');
    axios.get(`${myHost}/network/config`)
      .then(response => {
        setRemoteHost(response.data.message.HOST);
        setLocalHost(response.data.message.LOCALHOST);
        setPort(response.data.message.PORT);
        setSyncConstant(response.data.message.SYNC_CONST)
        setClusterSize(response.data.message.CLUSTER_SIZE)
        setDeviceIp(response.data.message.NET_IP)
        setPALREQ(response.data.message.PALREQ)

        // console.log(response.data.message)
        hideLoading()

      })
      .catch(error => {
        console.error(error);
        hideLoading()
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

  const handleSave = () => {
    showLoading()
    const myHost = sessionStorage.getItem('host');
    const requestData = {
      CLUSTER_SIZE: ClusterSize,
      HOST: remoteHost,
      KERNAL_TIMEOUT: 60,
      LOCALHOST: localHost,
      PORT: port,
      SHELL_TIMEOUT: 300,
      SYNC_CONST: SyncConstant,
      PALREQ: PALREQ

    };
    axios.post(`${myHost}/network/config`, requestData)
      .then(response => {
        Toast.fire({
          icon: 'success',
          title: 'Network Configuration update Success'
        })
        hideLoading()
      })
      .catch(error => {
        Toast.fire({
          icon: 'error',
          title: 'Network Configuration Not updated'
        })
        hideLoading()
      });
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
  const handleSyncConstant = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setSyncConstant(parseInt(value));
  };
  const handleClusterSize = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setClusterSize(value);
  };

  const handlepalReq = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setPALREQ(parseInt(value));
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
        <Loading visible={loadingVisible} /> 
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
          Network
        </Box>
      </Flex>
      <Modal closeOnOverlayClick={false} isOpen={isOpen} onClose={onClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Network Module Settings</ModalHeader>
          <ModalCloseButton color={'black'}/>
          <ModalBody>
            <Box mb="4" display="flex" flexDirection="column">
              <label htmlFor="remoteHost">Global Remote Host:</label>
              <input type="text" id="remoteHost" value={remoteHost} onChange={handleRemoteHostChange} />
            </Box>
            <Box mb="4" display="flex" flexDirection="column">
              <label htmlFor="localHost">Local Remote Host:</label>
              <input type="text" id="localHost" value={localHost} onChange={handleLocalHostChange} />
            </Box>
            <Box mb="4" display="flex" flexDirection="column">
              <label htmlFor="port">Host Port:</label>
              <input type="text" id="port" value={port} onChange={handlePortChange} />
            </Box>
            <Box mb="4" display="flex" flexDirection="column">
              <label htmlFor="localHost">Network Sync. Constant:</label>
              <input type="text" id="localHost" value={SyncConstant} onChange={handleSyncConstant} />
            </Box>
            <Box mb="4" display="flex" flexDirection="column">
              <Flex justifyContent='center'>
              <Box w={'45%'}>
                <label htmlFor="clusterSize">Model count</label>
                <input type="text" id="clusterSize" value={ClusterSize} style={{ width: '100%' }} onChange={handleClusterSize} />
              </Box>
                <Spacer />
                <Box  w={'45%'}>
                  <label htmlFor="localHost">Parallel Req. :</label>
                  <input type="text" id="deviceIp" value={PALREQ} style={{ width: '100%' }}  onRateChange={handlepalReq}/>
                </Box>
              </Flex>
            </Box>
            <Box mb="4" display="flex" flexDirection="column">
              <Flex justifyContent='center'>
                <Box w={'30%'}>
                  <label htmlFor="localHost">COM Port:</label>
                  <input type="text" id="localHost" defaultValue={APIport} style={{ width: '100%' }} />
                </Box>
                <Spacer />
                <Box  w={'60%'}>
                  <label htmlFor="localHost">Network Interface IP:</label>
                  <input type="text" id="deviceIp" defaultValue={DeviceIp} style={{ width: '100%' }} />
                </Box>
              </Flex>
            </Box>
            <Button w="100%" colorScheme="orange" _hover={{ bg: "orange.700" }} color="white" onClick={handleSave}>Update</Button>
          </ModalBody>
        </ModalContent>
      
      </Modal>
    </>
  );
};

export default NetworkModule;