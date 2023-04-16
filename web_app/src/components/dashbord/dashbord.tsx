import { Box, Flex } from '@chakra-ui/react';
import React from 'react';

import New from './new';
import Item from './item';
import Sitem from './sitem';
import Tcpitem from './tcpitem';
import NodeItem from './node'

interface AppProps {
    darkMode: boolean;
}

const Dashboard: React.FC<AppProps> = ({ darkMode }) => {
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
                <Tcpitem darkMode={darkMode}/>
                <NodeItem darkMode={darkMode}/>
                <Item darkMode={darkMode}/>
                <Item darkMode={darkMode}/>
                <Item darkMode={darkMode}/>
                <Item darkMode={darkMode}/>
                <Item darkMode={darkMode}/>
                <Item darkMode={darkMode}/>
                <New darkMode={darkMode}/>
            </Flex>
          </Box>
            <Box border="1px solid" borderColor={darkMode ? "gray.600" : 'gray.300'} padding={'20px'}
            w={{ base: '100%', lg: '40%' }} h={'100%'} minW={'300px'} mt={{ base: '30px', lg: '0px' }}>
                <Flex
                flexWrap="wrap"
            >
                <Sitem darkMode={darkMode}/>
                <Sitem darkMode={darkMode}/>
                <Sitem darkMode={darkMode}/>
            </Flex>
            </Box>
        </Flex>
      );
};

export default Dashboard;
