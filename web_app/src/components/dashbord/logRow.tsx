import React from 'react';
import { Grid, GridItem } from '@chakra-ui/react';

// Define the type for the receivedModel objects
interface ReceivedData {
  id: string;
  value: boolean;
  accuracy: number;
}

interface LogRowProps {
  rowData: {
    iteration: number;
    localModel: {
      id: string;
      value: string;
      accuracy: number;
    };
    receivedModel: ReceivedData[]; // Use the ReceivedData type for receivedModel array
    aggregatedModel: {
      id: string;
      value: string;
      accuracy: number;
    };
  };
}

const LogRow: React.FC<LogRowProps> = ({ rowData }) => {
  return (
    <div style={{
      border: '1px solid lightgray', 
      padding: '2px',
    }}>
      <Grid templateColumns='repeat(8, 1fr)' gap={1}>
        <GridItem w='100%' h='auto' textAlign='center'>
          {rowData.iteration}
        </GridItem>
        <GridItem w='100%' h='auto' textAlign='center'>
          {rowData.localModel.id}
        </GridItem>
        <GridItem w='100%' h='auto' textAlign='center'>
          {rowData.localModel.accuracy}
        </GridItem>


        <GridItem w='100%' h='auto' textAlign='center'>
          {rowData.receivedModel[0].id}
        </GridItem>
        <GridItem w='100%' h='auto' textAlign='center'>
        {rowData.receivedModel[0].accuracy}
        </GridItem>
        <GridItem w='100%' h='auto' textAlign='center'>
        {rowData.receivedModel[0].value.toString()}
        </GridItem>

        <GridItem w='100%' h='auto' textAlign='center'>
          {rowData.aggregatedModel.id}
        </GridItem>
        <GridItem w='100%' h='auto' textAlign='center'>
          {rowData.aggregatedModel.accuracy}
        </GridItem>
      </Grid>
    </div>
  );
};

export default LogRow;
