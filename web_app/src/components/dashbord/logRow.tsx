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
        kernalTime: number;
        totalKernalTime: number
    };
}

const LogRow: React.FC<LogRowProps> = ({ rowData }) => {
    return (
        <div style={{
            border: '1px solid lightgray',
            padding: '2px',
        }}>
            <Grid templateColumns='repeat(10, 1fr)' gap={1}>
                <GridItem
                    w='100%'
                    h='auto'
                    textAlign='center'
                    style={{
                        display: 'flex',
                        justifyContent: 'center',
                        alignItems: 'center',
                        height: '100%', // This ensures the GridItem takes the full height
                    }}
                >
                    {rowData.iteration}
                </GridItem>

                <GridItem
                    w='100%'
                    h='auto'
                    textAlign='center'
                    style={{
                        display: 'flex',
                        justifyContent: 'center',
                        alignItems: 'center',
                        height: '100%', // This ensures the GridItem takes the full height
                    }}
                >
                    {rowData.localModel.id}
                </GridItem>
                <GridItem
                    w='100%'
                    h='auto'
                    textAlign='center'
                    style={{
                        display: 'flex',
                        justifyContent: 'center',
                        alignItems: 'center',
                        height: '100%', // This ensures the GridItem takes the full height
                    }}
                >
                    {rowData.localModel.accuracy}
                </GridItem>


                <GridItem w='100%' h='auto' textAlign='center'>
                    {rowData.receivedModel.map((item, index) => (
                        <div key={index}
                            style={{
                                margin: '10px', // Add padding to create some space around the content
                            }}>
                            {item.id}
                        </div>
                    ))}
                </GridItem>
                <GridItem w='100%' h='auto' textAlign='center'>
                    {rowData.receivedModel.map((item, index) => (
                        <div key={index}
                            style={{
                                margin: '10px', // Add padding to create some space around the content
                            }}>
                            {item.accuracy}
                        </div>
                    ))}
                </GridItem>
                <GridItem w='100%' h='auto' textAlign='center'>
                    {rowData.receivedModel.map((item, index) => (
                        <div
                            key={index}
                            style={{
                                color: item.value ? '#558B2F' : '#FF5722',
                                backgroundColor: item.value ? '#DCEDC8' : '#FFCCBC',
                                borderRadius: '5px',
                                margin: '10px', // Add padding to create some space around the content
                            }}
                        >
                            {item.value.toString()}
                        </div>
                    ))}
                </GridItem>

                <GridItem
                    w='100%'
                    h='auto'
                    textAlign='center'
                    style={{
                        display: 'flex',
                        justifyContent: 'center',
                        alignItems: 'center',
                        height: '100%', // This ensures the GridItem takes the full height
                    }}
                >
                    {rowData.aggregatedModel.id}
                </GridItem>
                <GridItem
                    w='100%'
                    h='auto'
                    textAlign='center'
                    style={{
                        display: 'flex',
                        justifyContent: 'center',
                        alignItems: 'center',
                        height: '100%', // This ensures the GridItem takes the full height
                    }}
                >
                    {rowData.aggregatedModel.accuracy}
                </GridItem>
                <GridItem
                    w='100%'
                    h='auto'
                    textAlign='center'
                    style={{
                        display: 'flex',
                        justifyContent: 'center',
                        alignItems: 'center',
                        height: '100%', // This ensures the GridItem takes the full height
                    }}
                >
                    {rowData.kernalTime}
                </GridItem>
                <GridItem
                    w='100%'
                    h='auto'
                    textAlign='center'
                    style={{
                        display: 'flex',
                        justifyContent: 'center',
                        alignItems: 'center',
                        height: '100%', // This ensures the GridItem takes the full height
                    }}
                >
                    {rowData.totalKernalTime}
                </GridItem>
            </Grid>
        </div>
    );
};

export default LogRow;
