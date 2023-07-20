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
  },
  {
    "iteration": 2,
    "localModel": {
      "id": "1",
      "value": "True",
      "accuracy": 26.2
    },
    "receivedModel": [
      {
        "id": "DEU8m9Me3RVzD07h",
        "value": true,
        "accuracy": 22.8
      },
      {
        "id": "2a4e0yBIBRAYlc1u",
        "value": true,
        "accuracy": 23.0
      },
      {
        "id": "DEU8m9Me3RVzD07h",
        "value": true,
        "accuracy": 22.8
      },
      {
        "id": "A7Gi5H4JyuLGwPSO",
        "value": true,
        "accuracy": 20.89
      }
    ],
    "aggregatedModel": {
      "id": "2",
      "value": "True",
      "accuracy": 27.2
    }
  },
  {
    "iteration": 3,
    "localModel": {
      "id": "2",
      "value": "True",
      "accuracy": 27.3
    },
    "receivedModel": [
      {
        "id": "H4OVk5JCAlPeCGYm",
        "value": true,
        "accuracy": 30.3
      },
      {
        "id": "XaJAbJO7No3wN6Lb",
        "value": true,
        "accuracy": 26.9
      },
      {
        "id": "iVtMotQpNfcQo5Om",
        "value": true,
        "accuracy": 22.9
      },
      {
        "id": "2a4e0yBIBRAYlc1u",
        "value": true,
        "accuracy": 23.0
      }
    ],
    "aggregatedModel": {
      "id": "3",
      "value": "True",
      "accuracy": 27.4
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
   
      <div style={{ maxHeight: '500px', overflowY: 'auto' }}>
        {logData.map((data, index) => (
          <LogRow key={index} rowData={data} />
        ))}
      </div>

    </div>
  );
};

export default Log;
