import { AbsoluteCenter, Box, Flex } from '@chakra-ui/react';
import React from 'react';

import Login from './login';

interface SettingsProps {
    darkMode: boolean;
}

const Settings: React.FC<SettingsProps> = ({ darkMode }) => {
    return (
        <Flex color={darkMode ? 'white' : 'gray.800'} p={4} h="calc(100vh - 75px)" w={'100%'}>
            <Login darkMode={darkMode} />
        </Flex>
    );
};

export default Settings;
