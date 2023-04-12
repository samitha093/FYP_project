import { Center, Flex } from '@chakra-ui/react';
import React from 'react';

interface AppProps {
    darkMode: boolean;
}

const Sitem: React.FC<AppProps> = ({ darkMode }) => {
    return (
        <Flex justify="space-between"
        align="center"
        w={{ base: `calc(50% - 10px)`}}
        h={'100px'}
        borderWidth="2px"
        borderStyle="solid"
        borderColor={darkMode ? "gray.600" : 'gray.300'}
        borderRadius={'20px'}
        justifyContent="center"
        _hover={{ cursor: 'pointer' }}
        mr={'10px'}
        mb={'10px'}>
        <Center margin={'30px'} h={'inherit'} w={'inherit'}
        color={darkMode? "white" : "black"}>
            192.168.23.45:6788
        </Center>
        </Flex>
    );
};

export default Sitem;
