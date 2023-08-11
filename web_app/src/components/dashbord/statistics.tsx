import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar, Line } from 'react-chartjs-2';
import faker from 'faker';
import { CircularProgressbar } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

function Statistics() {
  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Chart.js Bar Chart',
      },
    },
  };

  const options2 = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Chart.js Line Chart',
      },
    },
  };
const labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July'];

 const data = {
    labels,
    datasets: [
      {
        label: 'Dataset 1',
        data: labels.map(() => faker.datatype.number({ min: 0, max: 1000 })),
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
      },
      {
        label: 'Dataset 2',
        data: labels.map(() => faker.datatype.number({ min: 0, max: 1000 })),
        backgroundColor: 'rgba(53, 162, 235, 0.5)',
      },
    ],
  };
  
  const data1 = {
    labels: ['Item 1', 'Item 2', 'Item 3', 'Item 4', 'Item 5', 'Item 6', 'Item 7', 'Item 8', 'Item 9', 'Item 10', 'Item 11', 'Item 12'],
    datasets: [
      {
        data: [10, 19, 29, 40, 48, 55, 60, 71, 74, 78, 85, 88], // These are the data points for the chart
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
      },
    ],
  };
  const percentage = 66;

  return (
    <div>
      <div style={{ display: 'flex', flexDirection: 'row' }}>
        <div style={{ flex: 1, maxWidth: '50%', paddingRight: '10px' }}>
          <h2> Chart Example</h2>
          <div>
            <Bar options={options} data={data} />
          </div>
        </div>
        <div style={{ flex: 1, maxWidth: '50%', paddingLeft: '10px' }}>
          <h2>Line Chart Example</h2>
          <div>
            <Line options={options2} data={data1} />
          </div>
        </div>
      </div>
      <div style={{ display: 'flex', flexDirection: 'row' }}>
        {/* Repeat the same structure for the second row of charts */}
        <div style={{ flex: 1, maxWidth: '100%', paddingRight: '10px' }}>
          <h2>Progress bar</h2>
          <div style={{ width: '200px', height: '200px' }}>
            <CircularProgressbar value={percentage} text={`${percentage}%`} />
          </div>

        </div>
        <div style={{ flex: 1, maxWidth: '50%', paddingLeft: '10px' }}>
          <h2>Test</h2>
          <div>
           
          </div>
        </div>
      </div>
    </div>
  );
}

export default Statistics;
