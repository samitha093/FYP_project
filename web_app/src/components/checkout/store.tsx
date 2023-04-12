import React, { useEffect, useRef, useState } from 'react';
import { Box, Flex, Image, Text, useTheme } from '@chakra-ui/react';
import ProductCard from './product';

interface AppProps {
  darkMode: boolean;
}

interface Product {
  id: number;
  title: string;
  description: string;
  price: number;
  image: string;
}

const productList: Product[] = [
  {
    id: 1,
    title: 'Product 1',
    description: 'Product 1 description',
    price: 99.99,
    image: 'https://via.placeholder.com/400x400',
  },
  {
    id: 2,
    title: 'Product 2',
    description: 'Product 2 description',
    price: 149.99,
    image: 'https://via.placeholder.com/400x400',
  },
  {
    id: 3,
    title: 'Product 3',
    description: 'Product 3 description',
    price: 199.99,
    image: 'https://via.placeholder.com/400x400',
  },
  {
    id: 4,
    title: 'Product 2',
    description: 'Product 2 description',
    price: 149.99,
    image: 'https://via.placeholder.com/400x400',
  },
  {
    id: 5,
    title: 'Product 3',
    description: 'Product 3 description',
    price: 199.99,
    image: 'https://via.placeholder.com/400x400',
  },
  {
    id: 6,
    title: 'Product 2',
    description: 'Product 2 description',
    price: 149.99,
    image: 'https://via.placeholder.com/400x400',
  },
  {
    id: 7,
    title: 'Product 3',
    description: 'Product 3 description',
    price: 199.99,
    image: 'https://via.placeholder.com/400x400',
  }
];

const Store: React.FC<AppProps> = ({ darkMode }) => {
    const theme = useTheme();
    const [maxItemsPerRow, setMaxItemsPerRow] = useState(1);
    const [containerWidth, setContainerWidth] = useState("");
    const [key, setKey] = useState(0);
    const flexRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const containerWidth = flexRef.current?.offsetWidth;
        if (containerWidth) {
          let initWidth = containerWidth -50
          let calWidth = 0
          let calItem = 0
          let balance = initWidth
          for (let i = 300; i< 401 ; i++){
              let x = initWidth/i
              let y = initWidth%i
              if (y < balance){
                  balance = y
                  calWidth = i - 10
                  calItem = Math.floor(x)
              }
          }
          let stringValue = calWidth + "px";
          setContainerWidth(stringValue)
        }
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

    const cardWidth = `${100 / maxItemsPerRow}%`;

    return (
      <Flex
        direction="column"
        align="center"
        justify="center"
        h="100vh"
        color={darkMode ? 'white' : 'gray.800'}
      >
        <Box w="100%" px={4} pb={8} overflow="auto">
          <Flex justify="space-between" align="center" mb={20}>
            <Box>
              <Text fontSize="2xl" fontWeight="bold" mb={8}>
                Recomanded products
              </Text>
              <Flex
                ref={flexRef}
                flexWrap="wrap"
                align="center"
                id="product-container"
                >
                {productList.map((product) => (
                  <ProductCard key={product.id} product={product} darkMode={darkMode} containerWidth={containerWidth}/>
                ))}
              </Flex>
            </Box>
          </Flex>
        </Box>
      </Flex>
    );
  };

export default Store;