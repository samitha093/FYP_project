import { AbsoluteCenter, Box, Center, Flex } from '@chakra-ui/react';
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

  useEffect(() => {
    const myHost = sessionStorage.getItem('host');
    axios.get(`${myHost}/bridge/hello`)
      .then(response => {
        setIsBridge(true)
      })
      .catch(error => {
        console.error(error);
      });
  }, []);

  useEffect(() => {
    const myHost = sessionStorage.getItem('host');
    axios.get(`${myHost}/bridge/nabours`)
      .then(response => {
        setNabourArray(response.data.message)
      })
      .catch(error => {
        console.error(error);
      });
  }, []);

  const handledataSave = (e: any) => {
    // setBoostrapArray([...BoostrapArray, e])
    const myHost = sessionStorage.getItem('host');
    axios.post(`${myHost}/bridge/boostrap`, {
      ip: e.ip,
      port: e.port
    })
      .then(response => {
        console.log(response);
        //asign update array to setBoostrapArray
      })
      .catch(error => {
        console.log(error);
      });
  };

    return (
        <Flex
          justify="space-between"
          align="center"
          w={'100%'}
          h={'100%'}
          flexDir={{ base: 'column', lg: 'row' }}
          overflow={'scroll'}
        >
          <Box border="1px solid" borderColor={darkMode ? "gray.600" : 'gray.300'} padding={'20px'}
          mr={{ base: '0', lg: '30px' }} w={{ base: '100%', lg: '60%' }} h={'100%'} minW={'300px'}>
            <Flex
                flexWrap="wrap"
            >
                <NetworkModule darkMode={darkMode}/>
                {isBridge?<BridgeModule darkMode={darkMode}/>:null}
                {isBridge?<NodeItem darkMode={darkMode}/>:null}
                {BoostrapArray.map((element:any, index:any)=>(
                    <Item darkMode={darkMode} key={index} data={element}/>
                ))}
                {isBridge?<New darkMode={darkMode} handledataSave={handledataSave}/>:null}
            </Flex>
          </Box>
          <Box border="1px solid" borderColor={darkMode ? "gray.600" : 'gray.300'} padding={'20px'}
            w={{ base: '100%', lg: '40%' }} h={'100%'} minW={'300px'} mt={{ base: '30px', lg: '0px' }}>
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
        </Flex>
  );
};

export default Dashboard;
