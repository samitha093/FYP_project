import { Box, Flex } from '@chakra-ui/react';
import React, { useEffect, useState } from 'react';
import { GiEmptyWoodBucketHandle } from 'react-icons/gi';

import CartProduct from './cartProduct';

interface AppCart {
    darkMode: boolean;
    products:any;
}

interface Product {
    id: number;
    title: string;
    price: number;
    qty: number;
    totalPrice: number;
}

const Cart: React.FC<AppCart> = ({ darkMode , products}) => {
    const [productList, setproductList] = useState<Product[]>([]);
    useEffect(() => {
        setproductList(products);
      }, []);
    return (
        <Flex direction="column" h='100%' w='100%' padding={'20px'}>
            <Box h={`calc(100% - 100px)`} w='100%' overflow={"auto"}
            borderBottom="1px" borderColor="gray.300" pb="20px" mb='10px'
            >
                {productList.length === 0?
                <Box h={'100%'} color={darkMode ? "gray.600" : 'gray.300'} display="flex" alignItems="center" justifyContent="center">
                    <GiEmptyWoodBucketHandle size={150} style={{ fill: darkMode ? "gray.600" : 'gray.300' }} />
                </Box>
                :null}
                {productList.map((product) => (
                  <CartProduct darkMode={darkMode} Product={product} />
                ))}
            </Box>
            <Box h='100px' w='100%'>
                <Box
                    style={{
                    fontSize: '25px',
                    fontWeight: 'bold',
                    }}
                >
                Total Bill
                </Box>
                <Box
                    style={{
                    fontSize: '45px',
                    fontWeight: 'bold',
                    color: 'green',
                    textAlign: 'center',
                    }}
                >
                    LKR : 250000
                </Box>
            </Box>
        </Flex>
    );
};

export default Cart;
