import React, { useEffect, useState } from 'react';
import axios from 'axios';
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
  const [logData, setLogData] = useState<Array<{
    iteration: number;
    localModel: { id: string; value: boolean; accuracy: number };
    receivedModel: Array<{ id: string; value: boolean; accuracy: number }>;
    aggregatedModel: { id: string; value: boolean; accuracy: number };
  }>>([]);

  useEffect(() => {
    const myHost = sessionStorage.getItem('host');
    axios.get(`${myHost}/logData`)
      .then(response => {
        const data =  response.data();
        setLogData(data);
      })
      .catch(error => {
        console.error(error);
      });
  }, []);


  return (
<div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
  <h1 style={{ marginBottom: "20px" }}>Log Data</h1>
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