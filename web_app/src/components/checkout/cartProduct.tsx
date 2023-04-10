import { Box, Flex } from '@chakra-ui/react';
import React, { useEffect, useState } from 'react';

interface AppProps {
    Product :{
        id: number;
        title: string;
        price: number;
        qty: number;
        totalPrice: number;
    };
    darkMode: boolean;
}

const CartProduct: React.FC<AppProps> = ({ darkMode,Product }) => {
    return (
        <Box w={'100%'} borderWidth="1px"
        borderRadius="lg"
        mb={'10px'}
        padding={'10px'}
        color={darkMode ? 'white' : 'gray.800'}
        >
            {Product.title}
            <Flex w={'100%'} direction="row">
                <Box w={'50%'}>
                    LKR : 
                    {Product.price}
                </Box>
                <Box w={'50%'}>
                    Qty :
                    {Product.qty}
                </Box>
                <Box w={'50%'} color={'orange.600'}>
                    Total :
                    <span style={{ fontSize: '22px', fontWeight: 'bold' }}>{Product.totalPrice}</span>
                </Box>
            </Flex>
        </Box>
    );
};

export default CartProduct;
