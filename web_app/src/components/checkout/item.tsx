import { Box, Button, Center, Flex, Image, Input } from '@chakra-ui/react';
import React, { useEffect, useState } from 'react';
import { debounce } from 'lodash'
import qr from './qr'


interface AppProps {
    darkMode: boolean;
    handleProduct:any;
    handleAddProduct:any;
    item:any;
  

}

const Item: React.FC<AppProps> = ({ darkMode, handleProduct, handleAddProduct,item}) => {
    const [quantity, setQuantity] = useState(1);
    const [key, setKey] = useState(0);
    const [Overflow, setOverflow] = useState(false);
    const [totalPrice, setTotalPrice] = useState(item.price);


    const handleQuantityChange = (event:any) => {
        setQuantity(event.target.value);
   
    };

    const handleIncrement = () => {
        var totalQuantity=quantity + 1;
        setQuantity(totalQuantity);
        var totalVal =item.price*totalQuantity;
        setTotalPrice(totalVal);
        
    };

    const handleDecrement = () => {
        if (quantity > 1) {
        var totalQuantity=quantity - 1;
        setQuantity(totalQuantity);
        var totalVal =item.price*totalQuantity;
        setTotalPrice(totalVal);
        }
    };
    const handleOverflow = debounce(() => {
        const secondBox = document.getElementById("second-box");
        const parentBox = document.getElementById("parent-box");
        if (secondBox && parentBox) {
          const isOverflowing = secondBox.scrollWidth > secondBox.clientWidth + 1 || secondBox.scrollHeight > secondBox.clientHeight + 1;
          const widthInPixels = secondBox.getBoundingClientRect().width;
          const heightInPixels = secondBox.getBoundingClientRect().height;
          console.log("overflow",isOverflowing," width ",widthInPixels, "Height", heightInPixels);
          setOverflow(isOverflowing)
        }
      }, 100);
      useEffect(() => {
        window.addEventListener("resize", handleOverflow);
           const secondBox = document.getElementById("second-box");
           if (secondBox) {
               secondBox.addEventListener("scroll", handleOverflow);
           }
           handleOverflow();
           return () => {
               window.removeEventListener("resize", handleOverflow);
               if (secondBox) {
               secondBox.removeEventListener("scroll", handleOverflow);
               }
           };
       }, []);
    useEffect(() => {
     window.addEventListener("resize", handleOverflow);
        const secondBox = document.getElementById("second-box");
        if (secondBox) {
            secondBox.addEventListener("scroll", handleOverflow);
        }
        handleOverflow();
        return () => {
            window.removeEventListener("resize", handleOverflow);
            if (secondBox) {
            secondBox.removeEventListener("scroll", handleOverflow);
            }
        };
    }, [key]);
    useEffect(() => {
        const handleResize = () => {
            setKey(window.innerWidth);
        };
        window.addEventListener("resize", handleResize);
        return () => {
          window.removeEventListener("resize", handleResize);
        };
      }, []);
    return (
        <Flex id="parent-box" direction="row" h="100%" flexWrap="wrap" overflow="auto" justifyContent="center" alignItems="center">
            <Box id="first-box" w='60%' h={Overflow?'60%':'100%'}   borderRadius="30px" overflow="hidden" mt={Overflow?25:0}>
                <Center h="100%" color='white'>
                <img src={item.url}
                 alt='product image' width='200' height='400' />
                </Center>
            </Box>
            <Box id="second-box" w={Overflow?'100%':'40%'} h='100%' borderRadius="30px" padding="20px">
                <Flex direction="column" justifyContent="center" alignItems="center" h="100%">
                    <Box fontSize="20px" mb="15px">{item.title}</Box>
                    <Box fontSize="30px" color="#4CAF50" mb="15px">Price: {item.price}</Box>
                    <Flex alignItems="center" mb={25}>
                    <Box fontSize="20px" mr="5px">
                        Quantity:
                    </Box>
                    <Button onClick={handleDecrement} size="md">-</Button>
                    <Input
                        type="number"
                        value={quantity}
                        onChange={handleQuantityChange}
                        w="50px"
                        mx="2px"
                        textAlign="center"
                        color={darkMode? "white" : "black"}
                        fontSize="20px"
                    />
                    <Button onClick={handleIncrement} size="md">+</Button>
                    </Flex>
                    <Box fontSize="35px" textAlign="center" color="orange" mb="20px">Total: {totalPrice}</Box>
                    <Flex justifyContent="center">
                    <Button colorScheme="orange" size="lg" mr={5} onClick={() => handleAddProduct(quantity)}>
                        Add to Cart
                    </Button>
                    <Button colorScheme="red" size="lg" onClick={handleProduct}>
                        Remove
                    </Button>
                    </Flex>
                </Flex>
            </Box>
        </Flex>
    );
};

export default Item;