import React from 'react';
import { Line } from 'react-chartjs-2';
import { Flex } from '@chakra-ui/layout';

interface modelAccuracyLineChartProps {
  aggregationLableArray: number[];
  aggregationTimeArray: number[];
}

const AggregationTimeLineChart: React.FC<modelAccuracyLineChartProps> = ({
  aggregationLableArray,
  aggregationTimeArray,
}) => {
  const maxDataValue = Math.max(...aggregationTimeArray);
  const yMaxValue = Math.ceil(maxDataValue) + 0.5; // Set y-axis max value

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
    scales: {
      x: {
        title: {
          display: true,
          text: 'Number of Iterations',
        },
        ticks: {},
      },
      y: {
        title: {
          display: true,
          text: 'Time In Minutes',
        },
        ticks: {},
        max: yMaxValue,
      },
    },
  };

  const labels = aggregationLableArray;

  const data = {
    labels,
    datasets: [
      {
        label: 'Local Model Kernal Time',
        data: aggregationTimeArray,
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
      },
    ],
  };

  return (
    <Flex>
      <Flex flex={1}>
        <Line options={options} data={data} />
      </Flex>
    </Flex>
  );
};

export default AggregationTimeLineChart;
