
import React from 'react'
import { Box, Flex, Grid, GridItem, } from '@chakra-ui/layout';
import { Text } from '@chakra-ui/react';

interface ModelPerformanceProps {
  iteration: number;
  time: number;
}

const ModelPerformance: React.FC<ModelPerformanceProps> = ({
  iteration,
  time  
}) => {
  
  return (
    <Box display="flex" justifyContent="center" alignItems="center" height={"100%"}
      boxShadow="rgba(50, 50, 93, 0.25) 0px 6px 12px -2px, rgba(0, 0, 0, 0.3) 0px 3px 7px -3px"
      borderRadius={"20px"}
    >
      <Box display="flex" flexDirection="column" justifyContent="center" alignItems="center">
        <h2 style={{ fontWeight: 'bold' }}>System Performance </h2>
        <Box w={"auto"}>
          <Grid templateRows="repeat(2, 2fr)" templateColumns="repeat(2, 2fr)" gap={4} >
            <GridItem bg="white.200" mt={'10px'} >Iterations</GridItem>
            <GridItem bg="white.200"  mt={'10px'}>Time(min)</GridItem>
            <GridItem bg="white.200" mt={'-30px'} display="flex" flexDirection="column" justifyContent="center" alignItems="center">
              <Text fontWeight="bold" fontSize="50px">{iteration}</Text>
            </GridItem>

            <GridItem bg="white.200" mt={'-30px'} display="flex" flexDirection="column" justifyContent="center" alignItems="center">
              <Text fontWeight="bold" fontSize="50px">{time}</Text>
            </GridItem>

          </Grid>
        </Box>
      </Box>
    </Box>

  )
}

export default ModelPerformance