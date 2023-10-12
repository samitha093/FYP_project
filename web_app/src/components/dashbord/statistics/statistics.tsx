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
import Loading from '../../module/loading';
import AggregationModelCount from './aggregationModelCount';
import AggregationTimeLineChart from './aggregationTimeLineChart';
import { io } from 'socket.io-client';

interface StatisticData {
  modelFinalAccuracy: number;
  iteration: number;
  time: number;
  role: string;
  aggregationLableArray: number[];
  receivedModelArray: number[];
  rejectedModelArray: number[];
  localModelAccuracy: number[];
  aggregationTimeArray: number[];
  modelCount :number
}
const initialStatisticData: StatisticData = {
  modelFinalAccuracy: 0,
  iteration: 0,
  time: 0,
  role: 'SHELL',
  aggregationLableArray: [],
  receivedModelArray: [],
  rejectedModelArray: [],
  localModelAccuracy: [],
  aggregationTimeArray:[],
  modelCount:0
};

function Statistics() {
  const [loadingVisible, setLoadingVisible] = useState(false);
  const [statisticData, setStatisticData] = useState<StatisticData>(initialStatisticData);
  //for testing dummy data
  const statisticData1 = {
    aggregationLableArray: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
    //values between 2 and 6
    receivedModelArray:    [2,2,2,2,3,4,3,5,4,5,3,4,5,6],
    rejectedModelArray: [0,0,0,0,1,2,1,3,2,3,1,2,3,4],
    localModelAccuracy: [12, 23, 30, 35, 38, 44, 50, 55, 61,68, 75, 81,84],
    aggregationTimeArray: [2,3,2.5,3.5,3,2,4,2.5,4,2,3.5,3,4,2.5,3,2.5,3.5,3,2,4,2.5,4,2,3.5,3,4,2.5],
    modelFinalAccuracy: 84,
    role: "SHELL",
    iteration: 13,
    time: 45,
    modelCount: 2
  };

  
  // Function to show the loading component
  const showLoading = () => {
    setLoadingVisible(true);
  };

  // Function to hide the loading component
  const hideLoading = () => {
    setLoadingVisible(false);
  };
  useEffect(() => {
    showLoading()
    const myHost = sessionStorage.getItem('host');
    axios.get(`${myHost}/getStatisticData`)
      .then(response => {
        const data = response.data;
        // console.log("Static data ")
        // console.log(data)
        //convert time to minutes  & rount to integer
        // data['time'] = Math.round(data['time']/60);
        setStatisticData(data);
        hideLoading()
      })
      .catch(error => {
        console.error(error);
        setStatisticData(initialStatisticData);
        hideLoading()
      });
  }, []);

   //subscribe to the socket.io events
   useEffect(() => {
    var hostname = 'http://'+ window.location.hostname+ ':5001';
    const socket = io(hostname);
    // Event handler when connected to the server
    socket.on('connect', () => {
      console.log('Dashboard = > connected to the python backend');
    });
     // Event handler for custom events from the server
    socket.on('server_message', (data) => {
      console.log('Received from server:', data);
    });
    socket.on('STATISTIC', (data) => {
      // setStatisticData(initialStatisticData)
      setTimeout(() => {
      // Update the nabourArray with new data after the delay
      setStatisticData(data);
      }, 3000);
    });
    // Clean up the socket connection when the component unmounts
    return () => {
      socket.disconnect();
    };
  }, []);

  return (
    <Box border="1px solid" borderColor={"gray.300" } 
    mr={{ base: '0', lg: '30px' }} w={'100%'} h={'100%'} minW={'300px'}
    pt={'20px'} pl={'5px'} pr={'10px'}
    overflow="auto">
    <div >
    <Grid templateColumns="repeat(4, 24%)" gap={4}>
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
        <AggregationModelCount
         modelCount={statisticData.modelCount}
        />
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

    {/* Third Row */}
      <GridItem colSpan={2} bg="white.200" height="300px" mt={'0px'}>
      <AggregationTimeLineChart
        aggregationLableArray={statisticData.aggregationLableArray}
        aggregationTimeArray={statisticData.aggregationTimeArray}
       />
      </GridItem>
      <GridItem colSpan={2} bg="white.200" height="300px">
      {/* <LineChart
        aggregationLableArray={statisticData.aggregationLableArray}
        localModelAccuracy={statisticData.localModelAccuracy}
       /> */}
      </GridItem> 
    </Grid>
  </div>
  </Box>
  );
}

export default Statistics;
