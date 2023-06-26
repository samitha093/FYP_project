import React, { useEffect, useState } from 'react';
// import { Container, Table } from 'react-bootstrap';

const Log = () => {

  //this is correct
  const [logData, setLogData] = useState<Array<{
    iteration: number;
    localModel: { id: string; value: boolean; accuracy: number };
    receivedModel: Array<{ id: string; value: boolean; accuracy: number }>;
    aggregatedModel: { id: string; value: boolean; accuracy: number };
  }>>([]);


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
    <div>test</div>
//     <Container>
//     <h1 className="text-center text-primary fw-bold">Log</h1>

//     {logData.length ? (
//       <Table striped bordered responsive className="mt-3" style={{ margin: '0 auto' }}>
//   <thead className="thead-dark">
//     <tr className="text-center align-middle">
//       <th>Iteration</th>
//       <th>Local Model Id</th>
//       <th>Local Model Accuracy</th>
//       <th>Received Model Id</th>
//       <th>Received Model Accuracy</th>
//       <th>Received Model Value</th>
//       <th>Aggregated Model Id</th>
//       <th>Aggregated Model Accuracy</th>
//     </tr>
//   </thead>
//   <tbody>
//     {logData.map((log, index) => (
//       <React.Fragment key={index}>
//        <tr>
//   <td>{log.iteration}</td>
//   <td>{log.localModel.id}</td>
//   <td>{log.localModel.accuracy}</td>
//   <td style={{ backgroundColor: log.receivedModel[0].value === false ? "red" : "white" }}>{log.receivedModel[0].id}</td>
//   <td style={{ backgroundColor: log.receivedModel[0].value === false? "red" : "white" }}>{log.receivedModel[0].accuracy}</td>
//   <td style={{ backgroundColor: log.receivedModel[0].value === false ? "red" : "white" }}>{log.receivedModel[0].value === false ? "Reject" : "Accept"}</td>
//   <td>{log.aggregatedModel.id}</td>
//   <td>{log.aggregatedModel.accuracy}</td>
// </tr>
// {log.receivedModel.slice(1).map((model, i) => (
//   <tr key={i}>
//     <td></td>
//     <td></td>
//     <td></td>
//     <td style={{ backgroundColor: model.value === false ? "red" : "white" }}>{model.id}</td>
//     <td style={{ backgroundColor: model.value === false ? "red" : "white" }}>{model.accuracy}</td>
//     <td style={{ backgroundColor: model.value === false ? "red" : "white" }}> {model.value === false ? "Reject" : "Accept"}</td>
//     <td></td>
//     <td></td>
//   </tr>

//         ))}
//       </React.Fragment>
//     ))}
//   </tbody>
// </Table>


//     ) : (
//       <p>Loading log data...</p>
//     )}
//   </Container>
);
};


export default Log;


