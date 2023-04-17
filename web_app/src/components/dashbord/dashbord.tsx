import { Box, Flex } from '@chakra-ui/react';
import React, { useState, useEffect } from 'react';
import axios from 'axios';

import New from './new';
import Item from './item';
import Sitem from './sitem';
import Tcpitem from './tcpitem';

interface AppProps {
    darkMode: boolean;
    

}

interface portIp {
  ip: string;
  port: string;
  index: string;
}

const Dashboard: React.FC<AppProps> = ({ darkMode  }) => {
  const [portIpList, setPortIpList] = useState<portIp[]>([]);
 
  // const ipAdd="125.212.325.23"
// get port ip list
  useEffect(() => {
    axios.get('http://127.0.0.1:5001/getPortIp')
      .then(response => {
        setPortIpList(response.data);
        console.log("Port IP");
        console.log(response.data);
      })
      .catch(error => {
        console.error(error);
      });
  }, []);

//add port ip list
  const data = {
    port: '8000',
    ip: '125.215.11'
  };
  
  axios.post('http://127.0.0.1:5001/addPortIp', data)
    .then(response => {
      console.log("add post response")
      console.log(response.data);
    })
    .catch(error => {
      console.error(error);
    });
//update port ip list
const updateData = {
  index :'1',
  port: '2500',
  ip: '125.215.11'
};

axios.post('http://127.0.0.1:5001/updatePortIp', updateData)
  .then(response => {
    console.log("update post response")
    console.log(response.data);
  })
  .catch(error => {
    console.error(error);
  });


  return (
    <Flex
      justify="space-between"
      align="center"
      w={'100%'}
      h={'100%'}
      flexDir={{ base: 'column', lg: 'row' }}
      overflow={'scroll'}
    >
      <Box
        border="1px solid"
        borderColor={darkMode ? 'gray.600' : 'gray.300'}
        padding={'20px'}
        mr={{ base: '0', lg: '30px' }}
        w={{ base: '100%', lg: '60%' }}
        h={'100%'}
        minW={'300px'}
      >
        <Flex flexWrap="wrap">
          <Tcpitem darkMode={darkMode} />
          <Item darkMode={darkMode} />
        </Flex>
      </Box>
      <Box
        border="1px solid"
        borderColor={darkMode ? 'gray.600' : 'gray.300'}
        padding={'20px'}
        w={{ base: '100%', lg: '40%' }}
        h={'100%'}
        minW={'300px'}
        mt={{ base: '30px', lg: '0px' }}
      >
        <Flex flexWrap="wrap">
          <Sitem darkMode={darkMode} />
          <Sitem darkMode={darkMode} />
          <Sitem darkMode={darkMode} />
        </Flex>
      </Box>
    </Flex>
  );
};

export default Dashboard;
