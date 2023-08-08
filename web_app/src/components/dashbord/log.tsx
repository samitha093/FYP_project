import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Grid, GridItem } from '@chakra-ui/react';
import LogRow from './logRow';
import Loading from '../module/loading';

const Log = () => {
  const [logData, setLogData] = useState([]);
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
    showLoading()
    const myHost = sessionStorage.getItem('host');
    axios.get(`${myHost}/logData`)
      .then(response => {
        const data = response.data;
        setLogData(data);
        hideLoading()
      })
      .catch(error => {
        console.error(error);
        hideLoading()
      });
  }, []);

  return (
    <div>
      <Grid templateColumns='repeat(8, 1fr)' gap={1}>
        <GridItem w='100%' h='auto' bg='blue.100' textAlign='center'>
          Iteration
        </GridItem>
        <GridItem w='100%' h='auto' bg='blue.100' textAlign='center'>
          Local Model Id
        </GridItem>
        <GridItem w='100%' h='auto' bg='blue.100' textAlign='center'>
          Local Model Accuracy
        </GridItem>
        <GridItem w='100%' h='auto' bg='blue.100' textAlign='center'>
          Receive Model Id
        </GridItem>
        <GridItem w='100%' h='auto' bg='blue.100' textAlign='center'>
          Receive Model Accuracy
        </GridItem>
        <GridItem w='100%' h='auto' bg='blue.100' textAlign='center'>
          Receive Model Value
        </GridItem>
        <GridItem w='100%' h='auto' bg='blue.100' textAlign='center'>
          Aggregated Model Id
        </GridItem>
        <GridItem w='100%' h='auto' bg='blue.100' textAlign='center'>
          Aggregated Model Accuracy
        </GridItem>
      </Grid>
   
      <div style={{ maxHeight: '500px', overflowY: 'auto' }}>
        {logData.map((data, index) => (
          <LogRow key={index} rowData={data} />
        ))}
      </div>
      <Loading visible={loadingVisible} /> 

    </div>
  );
};

export default Log;
