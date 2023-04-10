import React from 'react';
import { MoonIcon, SunIcon, SettingsIcon } from '@chakra-ui/icons';
import { Flex, Box, IconButton, Icon } from '@chakra-ui/react';
import { FaHome } from 'react-icons/fa'

interface NavProps {
  darkMode: boolean;
  toggleDarkMode: () => void;
  settings: boolean;
  toggleSettings: () => void;
}

const Nav: React.FC<NavProps> = ({ darkMode, toggleDarkMode ,settings ,toggleSettings}) => {
  return (
    <Flex
      alignItems="center"
      justifyContent="space-between"
      bg={darkMode ? 'gray.700' : 'white'}
      color={darkMode ? 'white' : 'gray.800'}
      py={4}
      px={6}
      boxShadow="0 1px 2px rgba(0, 0, 0, 0.05), 0 2px 4px rgba(0, 0, 0, 0.05), 0 4px 8px rgba(0, 0, 0, 0.05), 0 8px 16px rgba(0, 0, 0, 0.05), 0 16px 32px rgba(0, 0, 0, 0.05), 0 32px 64px rgba(0, 0, 0, 0.05), 0 64px 128px rgba(0, 0, 0, 0.05)"
    >
      <Box display="flex" alignItems="center">
        <img src="/logo.svg" alt="Super M" className="h-8 w-8 mr-2" />
      </Box>
      <Box display="flex" alignItems="center">
        <IconButton
          aria-label="Toggle dark mode"
          icon={darkMode ? <SunIcon /> : <MoonIcon />}
          mr={4}
          onClick={toggleDarkMode}
          variant="ghost"
          _hover={{ bg: darkMode ? 'gray.700' : 'white' }}
        />
        <IconButton
          aria-label="Open settings menu"
          icon={settings?<FaHome/>: <SettingsIcon/>}
          onClick={toggleSettings}
          variant="ghost"
          _hover={{ bg: darkMode ? 'gray.700' : 'white' }}
        />
      </Box>
    </Flex>
  );
};

export default Nav;