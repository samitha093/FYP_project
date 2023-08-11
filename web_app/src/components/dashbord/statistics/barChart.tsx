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
import { Flex } from '@chakra-ui/layout';
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

function BarChart() {
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

  return (
    <Flex>
    <Flex flex={1}>
      <Bar options={options} data={data} />
    </Flex>
  </Flex>
  );
}

export default BarChart;
