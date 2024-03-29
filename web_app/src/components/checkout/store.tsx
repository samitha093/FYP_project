import React, { useEffect, useRef, useState } from 'react';
import { Box, Flex, Image, Text, useTheme } from '@chakra-ui/react';
import ProductCard from './product';
import axios from 'axios';
import Loading from '../module/loading';

interface AppProps {
  darkMode: boolean;
}

interface Product {
  _id: string;
  ItemId: number;
  ItemName: string;
  ItemCategory: number;
  ItemPrice: number;
  ImageUrl: string;
}



const Store: React.FC<AppProps> = ({ darkMode }) => {
    const theme = useTheme();
    const [maxItemsPerRow, setMaxItemsPerRow] = useState(1);
    const [containerWidth, setContainerWidth] = useState("");
    const [key, setKey] = useState(0);
    const flexRef = useRef<HTMLDivElement>(null);
    const [loadingVisible, setLoadingVisible] = useState(false);

    // Function to show the loading component
    const showLoading = () => {
      setLoadingVisible(true);
    };

    // Function to hide the loading component
    const hideLoading = () => {
      setLoadingVisible(false);
    };

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


     const [productList, setProductList] = useState<Product[]>([]);

     useEffect(() => {
      showLoading()
      const myHost = sessionStorage.getItem('host');
       axios.get<Product[]>(`${myHost}/threands`)
         .then(response => {
          //  console.log(response.data);
           setProductList(response.data);
           hideLoading()
         })
         .catch(error => {
           console.log(error);
           hideLoading()
         });
     }, []);
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
              Recommended Products
              </Text>
              <Flex
                ref={flexRef}
                flexWrap="wrap"
                align="center"
                id="product-container"
                >
                {productList.map((product) => (
                  <ProductCard key={product._id} product={product} darkMode={darkMode} containerWidth={containerWidth}/>
                ))}
              </Flex>
            </Box>
          </Flex>
        </Box>
        <Loading visible={loadingVisible} /> 
      </Flex>
      
    );
  };

export default Store;