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
import { it } from 'node:test';


function Statistics() {
  const statisticData = {
    aggregationLableArray: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
    receivedModelArray: [7, 5, 8, 4, 5, 6, 8, 7, 5, 8, 4, 5, 6, 8],
    rejectedModelArray: [2, 3, 0, 5, 4, 3, 1, 2, 3, 0, 5, 4, 3, 1],
    localModelAccuracy: [12, 23, 30, 35, 38, 44, 50, 55, 61, 75, 80, 89, 90, 91],
    modelFinalAccuracy: 80,
    role: "SHELL",
    iteration: 10,
    time: 20,
  };
  

  return (
    <div>
    <Grid templateColumns="repeat(4, 290px)" gap={4}>
      {/* First Row */}
      <GridItem bg="white.200" height="200px" width="100%" display="flex" justifyContent="center" alignItems="center">
    <ProgressBar
    modelFinalAccuracy={statisticData.modelFinalAccuracy}
    />

</GridItem>

      <GridItem bg="white.200" height="200px">
       <ModelPerformance
       iteration={statisticData.iteration}
       time={statisticData.time}
       />
      </GridItem>
      <GridItem bg="white.200" height="200px">
        <Role
        role={statisticData.role}
        />
      </GridItem>
      <GridItem bg="white.200" height="200px">
        Column 4
      </GridItem>

      {/* Second Row */}
      <GridItem colSpan={2} bg="white.200" height="300px">
      <BarChart
            aggregationLableArray={statisticData.aggregationLableArray}
            receivedModelArray={statisticData.receivedModelArray}
            rejectedModelArray={statisticData.rejectedModelArray}
          />
      </GridItem>
      <GridItem colSpan={2} bg="white.200" height="300px">
       <LineChart
        aggregationLableArray={statisticData.aggregationLableArray}
        localModelAccuracy={statisticData.localModelAccuracy}
       />
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
