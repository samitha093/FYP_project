import { Box, Flex } from '@chakra-ui/react';
import axios from 'axios';
import QRCode from 'qrcode.react';
import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { io } from 'socket.io-client';

interface AppProps {
    darkMode: boolean;
}

const Mobile: React.FC<AppProps> = ({ darkMode }) => {
    const [ip, setIp] = useState("");
    const [profile, setProfile] = useState<boolean>(false);
    const [widthPercentage, setWidthPercentage] = useState<number>(0);
    const [content, setContent] = useState<boolean>(true);

    useEffect(() => {
        var hostname = 'http://'+ window.location.hostname+ ':5001';
        sessionStorage.setItem('host', hostname);
        axios.get(`${hostname}/getlocalip`)
        .then(response => {
            var uri = response.data + ":9999";
            setIp(uri);
        })
        .catch(error => {
            console.error(error);
        });
    }, []);

    useEffect(() => {
        if (profile) {
            const interval = setInterval(() => {
                setWidthPercentage(prevWidth => {
                    if (prevWidth < 50) {
                        return Math.min(prevWidth + 5, 50);
                    } else {
                        setContent(true);
                        clearInterval(interval);
                        return prevWidth;
                    }
                });
            }, 100); // Adjust the interval duration as needed
            return () => {
                clearInterval(interval);
            };
        } else {
            const interval = setInterval(() => {
                setWidthPercentage(prevWidth => {
                    if (prevWidth > 0) {
                        return Math.max(prevWidth - 5, 0);
                    } else {
                        setContent(false);
                        clearInterval(interval);
                        return prevWidth;
                    }
                });
            }, 100); // Adjust the interval duration as needed
            return () => {
                clearInterval(interval);
            };
        }
    }, [profile]);

      //subscribe to the socket.io events
  useEffect(() => {
    var hostname = 'http://'+ window.location.hostname+ ':5001';
    const socket = io(hostname);
    // Event handler when connected to the server
    socket.on('connect', () => {
      console.log('User Prifile = > connected to the python backend');
    });
     // Event handler for custom events from the server
    socket.on('server_message', (data) => {
      console.log('Received from server:', data);
    });
    socket.on('USER_PROFILE', (data) => {
      setTimeout(() => {
      // Update the nabourArray with new data after the delay
      console.log(data);
      if(data.length > 0){
        setProfile(true);
      }else{
        setProfile(false);
      }
      }, 3000);
    });
    // Clean up the socket connection when the component unmounts
    return () => {
      socket.disconnect();
    };
  }, []);

    function setProfileTrue() {
        setContent(false);
        setProfile(!profile);
    }

    return (
        <Flex
            direction="column"
            align="center"
            justify="center"
            h="100vh"
            w={'100%'}
            color={darkMode ? 'white' : 'gray.800'}
        >
            <Flex
                p={'5px'}
                justifyContent="center"
                maxWidth={'50%'}
                minWidth={'1050px'}
                minHeight={'600px'}
            >
                <Box
                    as={motion.div}
                    initial={{ flexBasis: '0%' }}
                    animate={{ flexBasis: `${widthPercentage}%` }}
                    flexDirection="column"
                    alignItems="center"
                    justifyContent="center"
                    backgroundColor={'#B2DFDB'}
                    minHeight={'500px'}
                    mt="auto"
                    mb="auto"
                    overflow={'hidden'}
                    style={{
                        borderTopLeftRadius: '30px',
                        borderBottomLeftRadius: '30px',
                    }}
                >
                    {content ? (
                        <Flex
                        h="100%"
                        flexDirection="column"
                        alignItems="center"
                        flexGrow={1}
                        mt={'20px'}
                        justifyContent="center">
                            User Conected ..
                        </Flex>
                    ) : null}
                </Box>
                <Flex
                    flexDirection="column"
                    flexBasis="50%"
                    alignItems="center"
                    justifyContent="center"
                    backgroundColor={'#00695C'}
                    minHeight={'200px'}
                    borderRadius={'25px'}
                >
                    <Box p="20px"
                        onClick={() => setProfileTrue()}
                        backgroundColor={'white'}
                    >
                        <QRCode value={ip} />
                    </Box>
                    <Box
                        color={'gray.300'}
                        fontSize={'20px'}
                        fontStyle={'bold'}
                        maxWidth={'60%'}
                        alignContent={'center'}
                        textAlign={'center'}
                        mt={'20px'}
                    >
                        Scan QR code to connect mobile app with your smart cart
                    </Box>
                </Flex>
            </Flex>
        </Flex>
    );
};

export default Mobile;
