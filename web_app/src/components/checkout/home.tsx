import { AbsoluteCenter, Box, Center, Flex } from '@chakra-ui/react';
import React, { useEffect, useState } from 'react';
import {BsShop, BsHandbag} from 'react-icons/bs'
import {MdMobileScreenShare} from "react-icons/md"

import Store from "./store";
import Checkout from "./checkout";
import Mobile from "./mobile";

interface HomeProps {
    darkMode: boolean;
}

const Home: React.FC<HomeProps> = ({ darkMode }) => {
    const [selectedBox, setSelectedBox] = useState<number | null>(2);

    const handleBoxClick = (index: number) => {
        setSelectedBox(index);
    };

    return (
      <Flex
        color={darkMode ? 'white' : 'gray.800'}
        p={4}
        h="calc(100vh - 75px)"
      >
        <Flex  w="200px" h="100%" >
            <Center color='white' ><Box>
            <Box
                    border="2px"
                    borderColor={darkMode ? "gray.600" : "gray.300"}
                    borderRadius="5px"
                    margin="5px"
                    padding="20px"
                    backgroundColor={selectedBox === 2 ? "green.600" : "transparent"}
                    color={selectedBox === 2 ? "white" : (darkMode ? 'white' : 'gray.600')}
                    _hover={{ backgroundColor: "green.600", cursor: "pointer", color: "white" }}
                    display="flex"
                    flexDirection="column"
                    justifyContent="center"
                    alignItems="center"
                    fontSize="3rem"
                    onClick={() => handleBoxClick(2)}
                >
                        <MdMobileScreenShare />
                        <Box mt={2} fontSize="1rem" color="inherit">Connect Mobile</Box>
                </Box>
                <Box
                    border="2px"
                    borderColor={darkMode ? "gray.600" : "gray.300"}
                    borderRadius="5px"
                    margin="5px"
                    padding="20px"
                    backgroundColor={selectedBox === 0 ? "green.600" : "transparent"}
                    color={selectedBox === 0 ? "white" : (darkMode ? 'white' : 'gray.600')}
                    _hover={{ backgroundColor: "green.600", cursor: "pointer", color: "white" }}
                    display="flex"
                    flexDirection="column"
                    justifyContent="center"
                    alignItems="center"
                    fontSize="3rem"
                    onClick={() => handleBoxClick(0)}
                >
                        <BsShop/>
                        <Box mt={2} fontSize="1rem" color="inherit">Store</Box>
                </Box>
                <Box
                    border="2px"
                    borderColor={darkMode ? "gray.600" : "gray.300"}
                    borderRadius="5px"
                    margin="5px"
                    padding="20px"
                    backgroundColor={selectedBox === 1 ? "green.600" : "transparent"}
                    color={selectedBox === 1 ? "white" : (darkMode ? 'white' : 'gray.600')}
                    _hover={{ backgroundColor: "green.600", cursor: "pointer", color: "white" }}
                    display="flex"
                    flexDirection="column"
                    justifyContent="center"
                    alignItems="center"
                    fontSize="3rem"
                    onClick={() => handleBoxClick(1)}
                >
                        <BsHandbag/>
                        <Box mt={2} fontSize="1rem" color="inherit">Checkout</Box>
                </Box>
            </Box></Center>
        </Flex >
        <Flex w="100%" h="100%">
        {selectedBox === 0?<Store darkMode={darkMode}/>:selectedBox === 1?<Checkout darkMode={darkMode}/>:selectedBox === 2?<Mobile darkMode={darkMode}/>:null}
        </Flex>
      </Flex>
    );
  };

export default Home;