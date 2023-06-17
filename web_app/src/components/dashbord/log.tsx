import React, { useEffect, useState } from 'react';

const Log = () => {
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
    <div>
      <h1>Welcome to the Log Dashboard!</h1>
      {logData.length ? (
        <table>
          <thead>
            <tr>
              <th>Iteration</th>
              <th>Local Model Id</th>
              <th>Local Model Accuracy</th>
              <th>Received Model Id</th>
              <th>Received Model Accuracy</th>
              <th>Aggregated Model Id</th>
              <th>Aggregated Model Accuracy</th>
            </tr>
          </thead>
          <tbody>
            {logData.map((log, index) => (
              <tr key={index}>
                <td>{log.iteration}</td>
                <td>{log.localModel.id}</td>
                <td>{log.localModel.accuracy}</td>
                <td>
                  <ul>
                    {log.receivedModel.map((model, i) => (
                      <li key={i}>{`${model.id} (${model.accuracy})`}</li>
                    ))}
                  </ul>
                </td>
                <td>{log.aggregatedModel.id}</td>
                <td>{log.aggregatedModel.accuracy}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>Loading log data...</p>
      )}
    </div>
  );
};

export default Log;
