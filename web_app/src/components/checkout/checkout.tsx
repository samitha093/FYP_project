import { Box, Flex } from '@chakra-ui/react';
import React from 'react';

import Item from "./item"
import Cart from "./cart"
import Slider from "./slider"

interface AppProps {
    darkMode: boolean;
}

const Checkout: React.FC<AppProps> = ({ darkMode }) => {
    return (
        <Flex w="100%" h="100%">
            <Box flex="1" h="100%" mx="20px" borderRadius="30px">
                <Box flex="1" w="100%" h="30%" border="2px" borderColor={darkMode ? "gray.600" : 'gray.300'} borderRadius="30px" mb="3%" overflow={"hidden"}>
                    <Slider darkMode={darkMode}/>
                </Box>
                <Box flex="1" w="100%" h="67%" border="2px" borderColor={darkMode ? "gray.600" : 'gray.300'} borderRadius="30px">
                    <Item darkMode={darkMode}/>
                </Box>
            </Box>
            <Box w="40%" h="100%" border="2px" borderColor={darkMode ? "gray.600" : 'gray.300'} borderRadius="30px">
                <Cart darkMode={darkMode}/>
            </Box>
        </Flex>
    );
};

export default Checkout;
