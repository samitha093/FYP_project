import React, { useEffect, useState } from 'react';
import { Box, Flex, Image, Text, useTheme } from '@chakra-ui/react';

interface ProductCardProps {
  product: {
    _id: string;
    ItemId: number;
    ItemName: string;
    ItemCategory: number;
    ItemPrice: number;
    ImageUrl: string;
  };
  darkMode: boolean;
  containerWidth:any
}

const ProductCard: React.FC<ProductCardProps> = ({ product, darkMode , containerWidth}) => {
  const theme = useTheme();

  return (
    <Box
    width="250px"
    borderWidth="1px"
    borderRadius="lg"
    overflow="hidden"
    bg={darkMode ? theme.colors.gray[700] : 'white'}
    color={darkMode ? 'white' : 'gray.800'}
    mr={4}
    mb={4}
  >
  
  <Image src={product.ImageUrl} alt={product.ItemName} style={{width: '300px', height: '300px'}} />

      <Box p="6">
        <Flex justify="space-between" align="baseline">
          <Text fontWeight="semibold" fontSize="xs" mr={2}>
            {product.ItemName}
          </Text>
          <Text fontSize="lg" color="gray.500">
            ${product.ItemPrice}
          </Text>
        </Flex>

        <Text mt={2} fontSize="s">
          {product.ItemCategory}
        </Text>
      </Box>
    </Box>
  );
};

export default ProductCard;