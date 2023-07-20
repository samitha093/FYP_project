import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Grid, GridItem } from '@chakra-ui/react';
import LogRow from './logRow';

const Log = () => {
  const [logData, setLogData] = useState([]);

  useEffect(() => {
    const myHost = sessionStorage.getItem('host');
    axios.get(`${myHost}/logData`)
      .then(response => {
        const data = response.data;
        setLogData(data);
      })
      .catch(error => {
        console.error(error);
      });
  }, []);
const dataset=[
  {
    "iteration": 1,
    "localModel": {
      "id": "0",
      "value": "True",
      "accuracy": 32.89
    },
    "receivedModel": [
      {
        "id": "cARCIDktu5Fo36Yq",
        "value": true,
        "accuracy": 19.6
      },
      {
        "id": "UtauKEmm5KTF6hH6",
        "value": true,
        "accuracy": 23.4
      },
      {
        "id": "cARCIDktu5Fo36Yq",
        "value": true,
        "accuracy": 19.6
      },
      {
        "id": "QcZ7TpgokwqLPMDO",
        "value": false,
        "accuracy": 11.7
      },
      {
        "id": "bvIAXjVi0ONvTzbb",
        "value": true,
        "accuracy": 29.29
      }
    ],
    "aggregatedModel": {
      "id": "1",
      "value": "True",
      "accuracy": 19.19
    }
  }
  
  
]
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
      {dataset.map((data, index) => (
        <LogRow key={index} rowData={data} />
      ))}
    </div>
  );
};

export default Log;
