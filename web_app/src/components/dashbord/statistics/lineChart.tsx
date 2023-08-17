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
interface modelAccuracyLineChartProps {
  aggregationLableArray: number[];
  localModelAccuracy: number[];

}
const LineChart: React.FC<modelAccuracyLineChartProps> = ({
  aggregationLableArray,
  localModelAccuracy,
}) => {

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Model Accuracy',
      },
    },
    scales: {
      x: {
        title: {
          display: true,
          text: 'X Axis Label', // Custom x-axis label
        },
        ticks: {
          // You can customize x-axis ticks here if needed
        },
      },
      y: {
        title: {
          display: true,
          text: 'Y Axis Label', // Custom y-axis label
        },
        ticks: {
          // You can customize y-axis ticks here if needed
        },
      },
    },
  };

const labels = aggregationLableArray;

 const data = {
    labels,
    datasets: [
      {
        label: 'Local Model Accuracy',
        data:localModelAccuracy,
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
      }
   
    ],
  };
  
  return (
    // <div></div>
    <Flex>
    <Flex flex={1}>
      <Line options={options} data={data} />
    </Flex>
  </Flex>
  );
}

export default LineChart;
