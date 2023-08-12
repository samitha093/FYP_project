import { Box } from '@chakra-ui/react';
import React from 'react';

interface RoleProps {
    modelCount: number;
}

const AggregationModelCount: React.FC<RoleProps> = ({ modelCount}) => {
  //use state boolen
  const [isShell, setIsShell] = React.useState<boolean>(false);

  const styles: React.CSSProperties = {
    fontSize: '24px',
    fontWeight: 'bold'
  };
  return (
    <Box display="flex" justifyContent="center" alignItems="center" height={"100%"}
      boxShadow="rgba(50, 50, 93, 0.25) 0px 6px 12px -2px, rgba(0, 0, 0, 0.3) 0px 3px 7px -3px"
      borderRadius={"20px"}
    >
      <Box display="flex" flexDirection="column" justifyContent="center" alignItems="center">
      <h2 style={{ fontWeight: 'bold' }} >Model Count</h2>

        {isShell?
          <Box
            mt="10px"
            w="200px"
            h="100px"
            backgroundColor="lightblue"
            display="flex"
            justifyContent="center"
            alignItems="center"
            borderRadius="10px"
            boxShadow="0px 4px 8px rgba(0, 0, 0, 0.1)"
          >
            <h1 style={styles}>SHELL</h1>
          </Box>
          : <Box
          mt="10px"
          w="100px"      // Make the width and height the same to create a circle
          h="100px"
          backgroundColor="lightblue"
          display="flex"
          justifyContent="center"
          alignItems="center"
          borderRadius="50%"  // Set border radius to 50% for a circular shape
          boxShadow="0px 4px 8px rgba(0, 0, 0, 0.1)"
        >
          <h1 style={styles}>{modelCount}</h1>
        </Box>
        }



      </Box>
    </Box>
  );
};

export default AggregationModelCount;
