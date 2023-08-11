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
import { Box, Flex } from '@chakra-ui/layout';
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

function ProgressBar() {
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
  const percentage = 66;
  return (
    <Box display="flex" justifyContent="center" alignItems="center" m="10px" height={"100%"}
    boxShadow="rgba(50, 50, 93, 0.25) 0px 6px 12px -2px, rgba(0, 0, 0, 0.3) 0px 3px 7px -3px"
     borderRadius={"20px"}
      >
      <Box display="flex" flexDirection="column" justifyContent="center" alignItems="center">
        <h2> Model Accuracy </h2>
        <Box maxW="50%" mt={'10px'}>
          <CircularProgressbar value={percentage} text={`${percentage}%`} />
        </Box>
      </Box>
    </Box>

  );
}
export default ProgressBar;
