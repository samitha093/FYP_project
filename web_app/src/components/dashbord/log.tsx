import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Box, Center, Grid, GridItem } from '@chakra-ui/react';
import LogRow from './logRow';
import { Image } from '@chakra-ui/react';

import emptyimage from '../../\assets/empty2.png';

interface AppProps {
  darkMode: boolean;
}

const Log: React.FC<AppProps> = ({ darkMode }) => {
  const [logData, setLogData] = useState([]);

  useEffect(() => {
    const myHost = sessionStorage.getItem('host');
    axios.get(`${myHost}/logData`)
      .then(response => {
        const data = response.data;
        setLogData(data);
      })
      .catch(error => {
        console.error(error);
      });
  }, []);

  return (
    <Box border="1px solid" borderColor={darkMode ? "gray.600" : 'gray.300'} 
      mr={{ base: '0', lg: '30px' }} w={'100%'} h={'100%'} minW={'300px'}
      overflow="auto">
      <Grid templateColumns='repeat(8, 1fr)' gap={1}>
        <GridItem w='100%' h='auto' bg='blue.100' textAlign='center' pt='20px' pb='20px'>
          Iteration
        </GridItem>
        <GridItem w='100%' h='auto' bg='blue.100' textAlign='center' pt='20px' pb='20px'>
          Local Model Id
        </GridItem>
        <GridItem w='100%' h='auto' bg='blue.100' textAlign='center' pt='20px' pb='20px'>
          Local Model Accuracy
        </GridItem>
        <GridItem w='100%' h='auto' bg='blue.100' textAlign='center' pt='20px' pb='20px'>
          Receive Model Id
        </GridItem>
        <GridItem w='100%' h='auto' bg='blue.100' textAlign='center' pt='20px' pb='20px'>
          Receive Model Accuracy
        </GridItem>
        <GridItem w='100%' h='auto' bg='blue.100' textAlign='center' pt='20px' pb='20px'>
          Receive Model Value
        </GridItem>
        <GridItem w='100%' h='auto' bg='blue.100' textAlign='center' pt='20px' pb='20px'>
          Aggregated Model Id
        </GridItem>
        <GridItem w='100%' h='auto' bg='blue.100' textAlign='center' pt='20px' pb='20px'>
          Aggregated Model Accuracy
        </GridItem>
      </Grid>
   
      <Box
        h='calc(100% - 70px)'
        overflowY='auto'
        display='flex'
        justifyContent='center'
        alignItems='center'
        >
        {logData.length === 0 ? (
          <Center>
            <Image
              src={emptyimage}
              alt="Description of the image"
              boxSize="200px"
              objectFit="cover"
              opacity={0.4}
            />
          </Center>
        ) : (
          logData.map((data, index) => (
            <LogRow key={index} rowData={data} />
          ))
        )}
      </Box>

    </Box>
  );
};

export default Log;
