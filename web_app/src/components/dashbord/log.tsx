import React, { useEffect, useState } from 'react';
import { Container, Table } from 'react-bootstrap';

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
          value: "True",
          accuracy: 0.58
        },
        receivedModel: [
          {
            id: "0001",
            value: "True",
            accuracy: 0.88
          },
          {
            id: "0002",
            value: "True",
            accuracy: 0.88
          },
          {
            id: "0003",
            value: "False",
            accuracy: 0.88
          },
          {
            id: "0004",
            value: "True",
            accuracy: 0.88
          }
        ],
        aggregatedModel: {
          id: "0005",
          value: "True",
          accuracy: 0.92
        }
      },
      {
        iteration: 1,
        localModel: {
          id: "0001",
          value: "False",
          accuracy: 0.58
        },
        receivedModel: [
          {
            id: "0001",
            value: "True",
            accuracy: 0.88
          },
          {
            id: "0002",
            value: "True",
            accuracy: 0.88
          },
          {
            id: "0003",
            value: "False",
            accuracy: 0.88
          },
          {
            id: "0004",
            value: "True",
            accuracy: 0.88
          }
        ],
        aggregatedModel: {
          id: "0005",
          value: "True",
          accuracy: 0.92
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
    <Container>
    <h1 className="text-center text-primary fw-bold">Welcome to the Log Dashboard!</h1>

    {logData.length ? (
      <Table striped bordered responsive className="mt-3" style={{ margin: '0 auto' }}>
  <thead className="thead-dark">
    <tr className="text-center align-middle">
      <th>Iteration</th>
      <th>Local Model Id</th>
      <th>Local Model Accuracy</th>
      <th>Received Model Id</th>
      <th>Received Model Accuracy</th>
      <th>Received Model Value</th>
      <th>Aggregated Model Id</th>
      <th>Aggregated Model Accuracy</th>
    </tr>
  </thead>
  <tbody>
    {logData.map((log, index) => (
      <React.Fragment key={index}>
        <tr>
          <td>{log.iteration}</td>
          <td>{log.localModel.id}</td>
          <td>{log.localModel.accuracy}</td>
          <td></td>
          <td></td>
          <td></td>
          <td>{log.aggregatedModel.id}</td>
          <td>{log.aggregatedModel.accuracy}</td>
        </tr>
        {log.receivedModel.map((model, i) => (
          <tr key={i}>
            <td></td>
            <td></td>
            <td></td>
            <td style={{ backgroundColor: model.value === "False" ? "red" : "white" }}>{model.id}</td>
            <td style={{ backgroundColor: model.value === "False" ? "red" : "white" }}>{model.accuracy}</td>
            <td style={{ backgroundColor: model.value === "False" ? "red" : "white" }}>{model.value}</td>
            <td></td>
            <td></td>
          </tr>
        ))}
      </React.Fragment>
    ))}
  </tbody>
</Table>


    ) : (
      <p>Loading log data...</p>
    )}
  </Container>
);
};


export default Log;
