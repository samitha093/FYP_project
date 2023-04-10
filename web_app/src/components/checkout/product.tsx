import React, { useEffect, useState } from 'react';
import { Box, Flex, Image, Text, useTheme } from '@chakra-ui/react';

interface ProductCardProps {
  product: {
    id: number;
    title: string;
    description: string;
    price: number;
    image: string;
  };
  darkMode: boolean;
  containerWidth:any
}

const ProductCard: React.FC<ProductCardProps> = ({ product, darkMode , containerWidth}) => {
  const theme = useTheme();

  return (
    <Box
      maxW={containerWidth}
      borderWidth="1px"
      borderRadius="lg"
      overflow="hidden"
      bg={darkMode ? theme.colors.gray[700] : 'white'}
      color={darkMode ? 'white' : 'gray.800'}
      mr={4}
      mb={4}
    >
      <Image src={product.image} alt={product.title} />
      <Box p="6">
        <Flex justify="space-between" align="baseline">
          <Text fontWeight="semibold" fontSize="xs" mr={2}>
            {product.title}
          </Text>
          <Text fontSize="lg" color="gray.500">
            ${product.price}
          </Text>
        </Flex>

        <Text mt={2} fontSize="s">
          {product.description}
        </Text>
      </Box>
    </Box>
  );
};

export default ProductCard;