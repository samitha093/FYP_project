import { AbsoluteCenter, Box, Flex } from '@chakra-ui/react';
import React from 'react';

interface SettingsProps {
    darkMode: boolean;
}

const Settings: React.FC<SettingsProps> = ({ darkMode }) => {
    return (
        <Flex color={darkMode ? 'white' : 'gray.800'} p={4} h="calc(100vh - 75px)">
            <AbsoluteCenter p='4' color='white' axis='both'>
            <Box
                p='4'
                borderRadius='md'
                boxShadow='0 0 10px rgba(0, 0, 0, 0.2)'
            >
                heloooooooow
            </Box>
        </AbsoluteCenter>
        </Flex>
    );
};

export default Settings;
