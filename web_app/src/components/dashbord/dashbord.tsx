import { AbsoluteCenter, Box, Center, Flex , Button, VStack} from '@chakra-ui/react';
import { CalendarIcon, RepeatIcon, SettingsIcon } from "@chakra-ui/icons";
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
  var ischange = true;
  const [isTrueButton1, setIsTrueButton1] = useState(false);
  const [isTrueButton2, setIsTrueButton2] = useState(false);
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

  const handleClickButton1 = () =>{
    // console.log("Button1");
    setIsTrueButton1(true)
    setIsTrueButton2(false)
  }
  const handleClickButton2 = () =>{
    // console.log("Button2");
    setIsTrueButton1(false)
    setIsTrueButton2(true)
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

  const refreshNabourList =()=>{
    setNabourArray([])
    const myHost = sessionStorage.getItem('host');
      // get nabour list
      axios.get(`${myHost}/bridge/nabours`)
        .then(response => {
          setNabourArray(response.data)
          // console.log(response.data)
        })
        .catch(error => {
          console.error(error);
        });
  }
  const refreshLogDataList =()=>{
    setNabourArray([])
    const myHost = sessionStorage.getItem('host');
      // get nabour list
      axios.get(`${myHost}/bridge/nabours`)
        .then(response => {
          setNabourArray(response.data)
          // console.log(response.data)
        })
        .catch(error => {
          console.error(error);
        });
  }
    return (
        <Flex
          justify="space-between"
          align="center"
          w={'100%'}
          h={'100%'}
          flexDir={{ base: 'column', lg: 'row' }}
          overflow={'scroll'}
        >

<VStack spacing={6} margin={0} mr={4}>

<Button colorScheme="blue" onClick={handleClickButton2} height="60px" display="flex" alignItems="center">
  <SettingsIcon style={{ marginRight: '5px' }} />

</Button>

<Button colorScheme="blue" onClick={handleClickButton1} height="60px" display="flex" alignItems="center">
  <CalendarIcon style={{ marginRight: '5px' }} />
</Button>


        </VStack>

          <Button
            pos="fixed"
            bottom="7"
            right="7"
            borderRadius="50%"
            p="4"
            fontSize="3xl"
            width="80px"
            height="80px"
            bg="teal.500"
            color="white"
            boxShadow="lg"
            _hover={{ bg: "teal.700" }}
            onClick={
              
              refreshNabourList}
          >



            <RepeatIcon />
          </Button>
          {!isTrueButton1?
          <> 
                <Box border="1px solid" borderColor={darkMode ? "gray.600" : 'gray.300'} padding={'20px'}
                mr={{ base: '0', lg: '30px' }} w={{ base: '100%', lg: '60%' }} h={'100%'} minW={'300px'}
                overflow="auto">
                  <Flex
                      flexWrap="wrap"
                  >
                      <NetworkModule darkMode={darkMode}/>
                      {isBridge?<BridgeModule darkMode={darkMode}/>:null}
                      {isBridge?<NodeItem darkMode={darkMode} nodeArray={BoostrapArray}/>:null}
                      {BoostrapArray.map((element:any, index:any)=>(
                          <Item darkMode={darkMode} key={index} data={element} handledataremove={handleCloseClick} handlerdataUpdate={handledataUpdate}/>
                      ))}
                      {isBridge?<New darkMode={darkMode} handledataSave={handledataSave}/>:null}
                  </Flex>
                </Box>
                <Box border="1px solid" borderColor={darkMode ? "gray.600" : 'gray.300'} padding={'20px'}
                  w={{ base: '100%', lg: '40%' }} h={'100%'} minW={'300px'} mt={{ base: '30px', lg: '0px' }}
                  overflow="auto">
                  {NabourArray.length == 0 ?
                    <Center p='4' w={'100%'} h={'100%'}>
                      <Image
                        src={emptyimage}
                        alt="Description of the image"
                        boxSize="200px"
                        objectFit="cover"
                        opacity={0.4}
                      />
                    </Center>
                  :
                  <Flex flexWrap="wrap">
                    {NabourArray.map((element:any, index:any)=>(
                        <Sitem darkMode={darkMode} key={index} data={element}/>
                        ))}
                  </Flex>
                  }
                </Box>
          </>
          :<Log/>}
        </Flex>
  );
};

export default Dashboard;
