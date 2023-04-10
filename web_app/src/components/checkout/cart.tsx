import { Box, Flex } from '@chakra-ui/react';
import React from 'react';

import CartProduct from './cartProduct';

interface AppCart {
    darkMode: boolean;
}

interface Product {
    id: number;
    title: string;
    price: number;
    qty: number;
    totalPrice: number;
}
  const productList: Product[] = [
    {
      id: 1,
      title: 'Product 1',
      price: 99.99,
      qty: 2,
      totalPrice: 188.99,
    },
    {
        id: 2,
        title: 'Product name 2',
        price: 99.99,
        qty: 2,
        totalPrice: 188.99,
    },
    {
        id: 3,
        title: 'Product name 3',
        price: 99.99,
        qty: 2,
        totalPrice: 188999.99,
    },
    {
        id: 1,
        title: 'Product 1',
        price: 99.99,
        qty: 2,
        totalPrice: 188.99,
      },
      {
          id: 2,
          title: 'Product name 2',
          price: 99.99,
          qty: 2,
          totalPrice: 188.99,
      },
      {
          id: 3,
          title: 'Product name 3',
          price: 99.99,
          qty: 2,
          totalPrice: 188999.99,
      },
      {
        id: 1,
        title: 'Product 1',
        price: 99.99,
        qty: 2,
        totalPrice: 188.99,
      },
      {
          id: 2,
          title: 'Product name 2',
          price: 99.99,
          qty: 2,
          totalPrice: 188.99,
      },
      {
          id: 3,
          title: 'Product name 3',
          price: 99.99,
          qty: 2,
          totalPrice: 188999.99,
      },
];

const Cart: React.FC<AppCart> = ({ darkMode }) => {
    return (
        <Flex direction="column" h='100%' w='100%' padding={'20px'}>
            <Box h={`calc(100% - 100px)`} w='100%' overflow={"auto"}
            borderBottom="1px" borderColor="gray.300" pb="20px" mb='10px'
            >
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
