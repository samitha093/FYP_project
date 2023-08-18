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
import { Bar } from 'react-chartjs-2';
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

interface BarChartProps {
  aggregationLableArray: number[];
  receivedModelArray: number[];
  rejectedModelArray: number[];
}

const BarChart: React.FC<BarChartProps> = ({
  aggregationLableArray,
  receivedModelArray,
  rejectedModelArray,
}) => {
  const maxDataValue = Math.max(...receivedModelArray, ...rejectedModelArray);

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Received Model vs Rejected Model',
      },
    },
    scales: {
      x: {
        title: {
          display: true,
          text: 'Number of Iterations', // Custom x-axis label
        },
        ticks: {},
      },
      y: {
        title: {
          display: true,
          text: 'Model Count', // Custom y-axis label
        },
        ticks: {},
        max: maxDataValue + 1, // Set the y-axis limit
      },
    },
  };

  const labels = aggregationLableArray;

  const data = {
    labels,
    datasets: [
      {
        label: 'Rejected Model',
        data: rejectedModelArray,
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
      },
      {
        label: 'Received Model',
        data: receivedModelArray,
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
};

export default BarChart;
