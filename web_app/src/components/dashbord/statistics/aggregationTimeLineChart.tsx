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
  aggregationTimeArray: number[];

}
const AggregationTimeLineChart: React.FC<modelAccuracyLineChartProps> = ({
  aggregationLableArray,
  aggregationTimeArray,
}) => {

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Aggregation Time Analysis',
      },
    },
  };

const labels = aggregationLableArray;

 const data = {
    labels,
    datasets: [
      {
        label: 'Local Model Accuracy',
        data:aggregationTimeArray,
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

export default AggregationTimeLineChart;
