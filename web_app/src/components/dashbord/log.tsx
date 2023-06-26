import React, { useEffect, useState } from 'react';
import {
  Table,
  Thead,
  Tbody,
  Tfoot,
  Tr,
  Th,
  Td,
  TableCaption,
  TableContainer,
  Container,
} from '@chakra-ui/react'

const Log = () => {

  //this is correct
  // const [logData, setLogData] = useState<Array<{
  //   iteration: number;
  //   localModel: { id: string; value: boolean; accuracy: number };
  //   receivedModel: Array<{ id: string; value: boolean; accuracy: number }>;
  //   aggregatedModel: { id: string; value: boolean; accuracy: number };
  // }>>([]);


  //this is for demo only
    const [logData, setLogData] = useState([
      {
        iteration: 1,
        localModel: {
          id: "0001",
          value: true,
          accuracy: 20
        },
        receivedModel: [
          {
            id: "00#1",
            value: true,
            accuracy: 30
          },
          {
            id: "00#2",
            value: false,
            accuracy: 5
          },
          {
            id: "00#3",
            value: false,
            accuracy: 60
          },
          {
            id: "00#4",
            value: true,
            accuracy: 0.28
          }
        ],
        aggregatedModel: {
          id: "0002",
          value: true,
          accuracy: 44
        }
      },
      {
        iteration: 2,
        localModel: {
          id: "0002",
          value: true,
          accuracy: 32
        },
        receivedModel: [
          {
            id: "00#8",
            value: true,
            accuracy: 38
          },
          {
            id: "00#7",
            value: true,
            accuracy: 25
          },
          {
            id: "00#3",
            value: false,
            accuracy: 8
          },
          {
            id: "00#4",
            value: true,
            accuracy: 40
          }
        ],
        aggregatedModel: {
          id: "0003",
          value: true,
          accuracy: 42
        }
      }, 
        {
        iteration: 3,
        localModel: {
          id: "0003",
          value: true,
          accuracy: 44
        },
        receivedModel: [
          {
            id: "00#5",
            value: true,
            accuracy: 38
          },
          {
            id: "00#6",
            value: true,
            accuracy: 45
          },
          {
            id: "00#4",
            value: false,
            accuracy: 75
          },
          {
            id: "00#2",
            value: false,
            accuracy: 10
          }
        ],
        aggregatedModel: {
          id: "0004",
          value: true,
          accuracy: 51
        }
      }
    ]);
  

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5001/logData');
      const data = await response.json();
      setLogData(data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  return (
    <div style={{ display: "flex", justifyContent: "center" }}>
      <Table size="sm">
        <Thead>
        <Tr>
            <Th>Iteration</Th>
            <Th>Local Model Id</Th>
            <Th>Local Model Accuracy</Th>
            <Th>Received Model Id</Th>
            <Th>Received Model Accuracy</Th>
            <Th>Received Model Value</Th>
            <Th>Aggregated Model Id</Th>
            <Th>Aggregated Model Accuracy</Th>
          </Tr>
        </Thead>
        <Tbody>
        {logData.map((log, index) => (
      <React.Fragment key={index}>
   <Tr>
  <Td>{log.iteration}</Td>
  <Td>{log.localModel.id}</Td>
  <Td>{log.localModel.accuracy}</Td>
  <Td style={{ backgroundColor: log.receivedModel[0].value === false ? "#91a3b0" : "white" }}>{log.receivedModel[0].id}</Td>
  <Td style={{ backgroundColor: log.receivedModel[0].value === false? "#91a3b0" : "white" }}>{log.receivedModel[0].accuracy}</Td>
  <Td style={{ backgroundColor: log.receivedModel[0].value === false ? "#91a3b0" : "white" }}>{log.receivedModel[0].value === false ? "Reject" : "Accept"}</Td>
  <Td>{log.aggregatedModel.id}</Td>
  <Td>{log.aggregatedModel.accuracy}</Td>
</Tr>
{log.receivedModel.slice(1).map((model, i) => (
  <Tr key={i}>
    <Td></Td>
    <Td></Td>
    <Td></Td>
    <Td style={{ backgroundColor: model.value === false ? "#91a3b0" : "white" }}>{model.id}</Td>
    <Td style={{ backgroundColor: model.value === false ? "#91a3b0" : "white" }}>{model.accuracy}</Td>
    <Td style={{ backgroundColor: model.value === false ? "#91a3b0" : "white" }}> {model.value === false ? "Reject" : "Accept"}</Td>
    <Td></Td>
    <Td></Td>
  </Tr>
 ))}
      </React.Fragment>
    ))}
        </Tbody>
      </Table>
    </div>
  );
  
};


export default Log;