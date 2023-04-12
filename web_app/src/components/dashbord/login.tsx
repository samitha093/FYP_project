import { useState } from 'react';
import { AbsoluteCenter, Box, Flex, Button, Alert, AlertIcon, AlertDescription } from '@chakra-ui/react';

import Dashboard from'./dashbord';

interface AppProps {
  darkMode: boolean;
}

const Login: React.FC<AppProps> = ({darkMode}) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [status, setStatus] = useState(false);

  const handleLogin = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!username || !password) {
      setErrorMessage('Please enter correct user name and password.');
    } else {
      setErrorMessage('');
      if(username == 'admin' && password == 'admin') {
        setStatus(true);
      }
    }
  };

  return (
    <Flex w={'100%'}>{status? <Dashboard darkMode={darkMode} /> :
      <AbsoluteCenter p="4" color={darkMode ? 'white' : 'gray.800'} axis="both">
        <Box p="4" borderRadius="md" boxShadow="0 0 10px rgba(0, 0, 0, 0.2)" minWidth={'400px'}>
          <form onSubmit={handleLogin}>
                <Flex direction="column" marginBottom="1rem">
                  <label style={{ textAlign: 'left' }}>Username:</label>
                  <input
                    type="text"
                    name="username"
                    value={username}
                    onChange={(event) => setUsername(event.target.value)}
                  />
                </Flex>
            <Flex direction="column" marginBottom="1rem">
                  <label style={{ textAlign: 'left' }}>Password:</label>
                  <input
                    type="password"
                    name="password"
                    value={password}
                    onChange={(event) => setPassword(event.target.value)}
                  />
                </Flex>
            {errorMessage && (
              <Alert status="error" mt="2" justifyContent="center">
                <AlertIcon />
                <AlertDescription color="red">{errorMessage}</AlertDescription>
              </Alert>
            )}
            <br />
            <Button type="submit" variant="solid" colorScheme="green" width="100%">
              Login
            </Button>
          </form>
        </Box>
      </AbsoluteCenter>
    }</Flex>
  );
};

export default Login;