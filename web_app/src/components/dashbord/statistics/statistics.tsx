import React from 'react';
import { Flex, Grid, GridItem, Heading } from "@chakra-ui/react";
import  { useEffect, useState } from 'react';
import axios from 'axios';
import { Box,  } from '@chakra-ui/react';
import ProgressBar from './progressBar';
import LineChart from './lineChart';
import BarChart from './barChart';
import ModelPerformance from './modelPerformance';
import Role from './role';


function Statistics() {
 
  return (
    <div>
    <Grid templateColumns="repeat(4, 290px)" gap={4}>
      {/* First Row */}
      <GridItem bg="white.200" height="200px" width="100%" display="flex" justifyContent="center" alignItems="center">
    <ProgressBar />

</GridItem>

      <GridItem bg="white.200" height="200px">
       <ModelPerformance/>
      </GridItem>
      <GridItem bg="white.200" height="200px">
        <Role/>
      </GridItem>
      <GridItem bg="white.200" height="200px">
        Column 4
      </GridItem>

      {/* Second Row */}
      <GridItem colSpan={2} bg="white.200" height="300px">
       <BarChart/>
      </GridItem>
      <GridItem colSpan={2} bg="white.200" height="300px">
       <LineChart/>
      </GridItem>

       {/* third Row */}
       {/* <GridItem colSpan={2} bg="white.200" height="300px">
       <BarChart/>
      </GridItem>
      <GridItem colSpan={2} bg="white.200" height="300px">
       <LineChart/>
      </GridItem> */}
    </Grid>
  </div>
  );
}

export default Statistics;
