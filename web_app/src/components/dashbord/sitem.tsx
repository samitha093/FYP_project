import { Center, Flex } from '@chakra-ui/react';
import React, { useEffect, useState } from 'react';

interface AppProps {
    darkMode: boolean;
    data:any;
    myid:any;
    backgroundColour:any;
}

const Sitem: React.FC<AppProps> = ({ darkMode,data,myid,backgroundColour }) => {
    const [ip, setIp] = useState('192.168.34.56');
    useEffect(() => {
        setIp(data);
        console.log(myid)
      }, []);
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
        mb={'10px'}
        backgroundColor={myid!=ip?backgroundColour:'#8E24AA'}>
        <Center margin={'30px'} h={'inherit'} w={'inherit'}
        color={darkMode? "white" : "black"}>
            {ip}
        </Center>
        </Flex>
    );
};

export default Sitem;
