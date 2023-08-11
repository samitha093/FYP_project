import { AbsoluteCenter, Box, Center, Flex , Button, VStack} from '@chakra-ui/react';
import { CalendarIcon, HamburgerIcon, RepeatIcon, SettingsIcon } from "@chakra-ui/icons";
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Image } from '@chakra-ui/react';

import New from './new';
import Item from './item';
import Sitem from './sitem';
import NetworkModule from './networkModule';
import NodeItem from './node';
import BridgeModule from './bridgeModule';

import emptyimage from '../../\assets/empty.png';
import { FaNetworkWired } from 'react-icons/fa';
import Log from './log';
import { io } from 'socket.io-client';
import Statistics from './statistics/statistics';

interface AppProps {
    darkMode: boolean;
}

interface portIp {
  ip: string;
  port: string;
  index: string;
}

const Dashboard: React.FC<AppProps> = ({ darkMode }) => {
  const [isBridge, setIsBridge] = useState(false);
  const [BoostrapArray, setBoostrapArray] = useState<any>([]);
  const [NabourArray, setNabourArray] = useState<any>([]);
  const [PeerArray, setPeerArray] = useState<any>([]);
  var ischange = true;
  const [isTrueButton1, setIsTrueButton1] = useState(true);
  const [isTrueButton2, setIsTrueButton2] = useState(false);
  const [isTrueButton3, setIsTrueButton3] = useState(false);
  const [myUserID, setMyUserID] = useState<any>("");
  useEffect(() => {
    const myHost = sessionStorage.getItem('host');
    axios.get(`${myHost}/bridge/hello`)
      .then(response => {
        setIsBridge(true)
        // get history boostrap nodes
        axios.get(`${myHost}/bridge/boostrap`)
          .then(response => {
            setBoostrapArray(response.data)
          })
          .catch(error => {
            console.error(error);
          });
      })
      .catch(error => {
        console.error(error);
      });
  }, []);

  //subscribe to the socket.io events
  useEffect(() => {
    var hostname = 'http://'+ window.location.hostname+ ':5001';
    const socket = io(hostname);
    // Event handler when connected to the server
    socket.on('connect', () => {
      console.log('Dashboard = > connected to the python backend');
    });
     // Event handler for custom events from the server
    socket.on('server_message', (data) => {
      console.log('Received from server:', data);
    });
    socket.on('NBRLIST', (data) => {
      setNabourArray([])
      setTimeout(() => {
      // Update the nabourArray with new data after the delay
      setNabourArray(data);
      }, 3000);
    });
    socket.on('PEERLIST', (data) => {
      setPeerArray([])
      setTimeout(() => {
        // Update the nabourArray with new data after the delay
        setPeerArray(data);
      }, 3000);
    });
    socket.on('USERID', (data) => {
      setMyUserID(data)
    });
    // Clean up the socket connection when the component unmounts
    return () => {
      socket.disconnect();
    };
  }, []);

  const handleClickButton1 = () =>{
    // console.log("Button1");
    setIsTrueButton1(true)
    setIsTrueButton2(false)
    setIsTrueButton3(false)
  }
  const handleClickButton2 = () =>{
    // console.log("Button2");
    setIsTrueButton1(false)
    setIsTrueButton2(true)
    setIsTrueButton3(false)

  }

  const handleClickButton3 = () =>{
    // console.log("Button2");
    setIsTrueButton1(false)
    setIsTrueButton2(false)
    setIsTrueButton3(true)
  }
  const handledataSave = (e: any) => {
    setBoostrapArray([])
    // setBoostrapArray([...BoostrapArray, e])
    const myHost = sessionStorage.getItem('host');
    axios.post(`${myHost}/bridge/boostrap`, {
      ip: e.ip,
      port: e.port
    })
      .then(response => {
      setBoostrapArray(response.data)
      })
      .catch(error => {
        console.log(error);
      });
  };

  const handledataUpdate = (e: any) => {
    setBoostrapArray([])
    const myHost = sessionStorage.getItem('host');
    axios.put(`${myHost}/bridge/boostrap`, {
      index: e.index,
      ip: e.ip,
      port: e.port
    })
      .then(response => {
      setBoostrapArray(response.data)
      })
      .catch(error => {
        console.log(error);
      });
  };

  const handleCloseClick = (e: any) => {
    setBoostrapArray([])
    const myHost = sessionStorage.getItem('host');
    axios
      .delete(`${myHost}/bridge/boostrap`, {
        headers: {
          index: e,
        },
      })
      .then((response) => {
        setBoostrapArray(response.data)
        // console.log(response.data)
      })
      .catch((error) => {
        console.log(error);
      });
  };
    return (
        <Box
          w={'100%'}
          h={'100%'}
          display="flex"
          >

          {/*  Side bar */}
          <Box
          width={'50px'}
            height={'100%'}
            display="flex"
            flexDirection="column"
            justifyContent="center"
            alignItems="center"
            m={'10px'}>
            <Button
              colorScheme="green"
              onClick={handleClickButton1}
              height="60px"
              display="flex"
              alignItems="center"
              style={{ marginRight: '6px', marginBottom: '6px' }}
            >
              <SettingsIcon style={{ marginRight: '5px' }} />
            </Button>
            <Button
              colorScheme="green"
              onClick={handleClickButton2}
              height="60px"
              display="flex"
              alignItems="center"
              style={{ marginRight: '6px', marginBottom: '6px' }}
            >
              <CalendarIcon style={{ marginRight: '5px' }} />
            </Button>
            <Button
              colorScheme="green"
              onClick={handleClickButton3}
              height="60px"
              display="flex"
              alignItems="center"
              style={{ marginRight: '6px', marginBottom: '6px' }}
            >
              <HamburgerIcon style={{ marginRight: '5px' }} />
              
            </Button>
          </Box>

          {/* component container start */}
          <Flex  w={`calc(100% - 10px)`} 
            h={'100%'}
            justify="space-between"
            align="center"
            flexDir={{ base: 'column', lg: 'row' }}
            overflow={'scroll'}>
        {isTrueButton1 ? (
            <>
               <Box border="1px solid" borderColor={darkMode ? "gray.600" : 'gray.300'} padding={'20px'}
                  mr={{ base: '0', lg: '30px' }} w={{ base: '100%', lg: '60%' }} h={'100%'} minW={'300px'}
                  overflow="auto">
                  <Flex flexWrap="wrap">
                      <NetworkModule darkMode={darkMode}/>
                      {isBridge?<BridgeModule darkMode={darkMode}/>:null}
                      {isBridge?<NodeItem darkMode={darkMode} nodeArray={BoostrapArray}/>:null}
                      {BoostrapArray.map((element:any, index:any)=>(
                          <Item darkMode={darkMode} key={index} data={element} handledataremove={handleCloseClick} handlerdataUpdate={handledataUpdate}/>
                      ))}
                      {isBridge?<New darkMode={darkMode} handledataSave={handledataSave}/>:null}
                  </Flex>
                </Box>
                <Box 
                  w={{ base: '100%', lg: '40%' }} 
                  h={'100%'} 
                  minW={'300px'} 
                  mt={{ base: '30px', lg: '0px' }}
                  overflow="auto">
                    <Box border="1px solid" padding={'20px'} borderColor={darkMode ? "gray.600" : 'gray.300'} h={'calc(50% - 15px)'}  mb={'10px'} overflow={'auto'}> 
                      Global neibhour list
                      {NabourArray.length == 0 ?
                      <Box width={'100%'} height={'calc(100% - 30px)'}>
                        <Center p='4' w={'100%'} h={'100%'}>
                          <Image
                            src={emptyimage}
                            alt="Description of the image"
                            boxSize="200px"
                            objectFit="cover"
                            opacity={0.4}
                          />
                        </Center>
                      </Box>
                      :
                        <Flex flexWrap="wrap" width={'100%'} height={'calc(100% - 30px)'}>
                          {NabourArray.map((element:any, index:any)=>(
                              <Sitem darkMode={darkMode} key={index} data={element} myid={myUserID} backgroundColour={'#42A5F5'}/>
                            ))}
                        </Flex>
                      }
                    </Box>
                    <Box border="1px solid" padding={'20px'} borderColor={darkMode ? "gray.600" : 'gray.300'} h={'50%'} overflow={'auto'}> 
                      Local peer list
                      {NabourArray.length == 0 ?
                        <Box width={'100%'} height={'calc(100% - 30px)'}>
                          <Center p='4' w={'100%'} h={'100%'}>
                            <Image
                              src={emptyimage}
                              alt="Description of the image"
                              boxSize="200px"
                              objectFit="cover"
                              opacity={0.4}
                            />
                          </Center>
                        </Box>
                      :
                        <Flex flexWrap="wrap" width={'100%'} height={'calc(100% - 30px)'}>
                          {PeerArray.map((element:any, index:any)=>(
                              <Sitem darkMode={darkMode} key={index} data={element} myid={myUserID} backgroundColour={'#26A69A'}/>
                              ))}
                        </Flex>
                      }
                    </Box>

                  
                </Box>
            </>
          ) : isTrueButton2 ? (
            <Log darkMode={darkMode} />
           
          ) : (
            <Statistics/>
          )}


          </Flex>


        </Box>
  );
};

export default Dashboard;
