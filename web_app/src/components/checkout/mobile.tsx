import { Box, Flex, FormControl, FormHelperText, FormLabel, Input, Spinner } from '@chakra-ui/react';
import axios from 'axios';
import QRCode from 'qrcode.react';
import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { io } from 'socket.io-client';
import bgimage1 from '../../\assets/bg.png';
import {HiOutlineUser} from "react-icons/hi";
import Swal from 'sweetalert2';

//1366x768
interface AppProps {
    darkMode: boolean;
}

const Mobile: React.FC<AppProps> = ({ darkMode }) => {
    const [ip, setIp] = useState("");
    const [profile, setProfile] = useState<boolean>(false);
    const [widthPercentage, setWidthPercentage] = useState<number>(0);
    const [content, setContent] = useState<boolean>(false);
    const [userdata, setUserdat] = useState([]);

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
      setUserdat(data)
      if(data.length > 0){
        if(profile == false){
        }
        setProfile(true);
      }else{
        setContent(false);
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
        var hostname = 'http://'+ window.location.hostname+ ':5001';
        axios.get(`${hostname}/mobileDisconect`)
        .then(response => {
            Toast.fire({
                icon: 'success',
                title: 'Mobile device disconnected!'
            })
        })
        .catch(error => {
            Toast.fire({
                icon: 'error',
                title: 'Something went wrong!'
            })
            console.error(error);
        });
    }

    const Toast = Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true,
        didOpen: (toast) => {
          toast.addEventListener('mouseenter', Swal.stopTimer)
          toast.addEventListener('mouseleave', Swal.resumeTimer)
        }
      })

    return (
        <Flex
            direction="column"
            align="center"
            justify="center"
            justifyContent="center"
            alignItems="center"
            h="100vh"
            w={'100%'}
            color={darkMode ? 'white' : 'gray.800'}
            backgroundImage={bgimage1}
            backgroundSize="auto 100%"
            backgroundRepeat="no-repeat"
            backgroundPosition="center"
            zIndex={1}
        >
            <Flex
                p={'5px'}
                justifyContent="center"
                w={'80%'}
                height={'70%'}
                mt="auto"
                mb="auto"
            >
            <Box
                as={motion.div}
                initial={{ flexBasis: '0%' }}
                animate={{ flexBasis: `${widthPercentage}%` }}
                flexDirection="column"
                alignItems="center"
                justifyContent="center"
                backgroundColor={'#B2DFDB'}
                overflowY={'auto'}
                mt="auto"
                mb="auto"
                height={'80%'}
                style={{
                    borderTopLeftRadius: '30px',
                    borderBottomLeftRadius: '30px',
                }}
            >
                {content ? (
                    <Flex
                        flexDirection="column"
                        alignItems="center"
                        flexGrow={1}
                        mt={'20px'}
                        justifyContent="center"
                        padding={'30px'}
                    >
                        <FormControl color={'gray.600'}>
                            <FormLabel>User name : </FormLabel>
                            <Input color={'black'} type='text' mb={'10px'} defaultValue={userdata[0]}/>
                            <FormLabel>Email : </FormLabel>
                            <Input color={'black'} type='email' mb={'10px'} defaultValue={userdata[2]}/>
                            <FormLabel>Address : </FormLabel>
                            <Input color={'black'} type='text' mb={'10px'} defaultValue={userdata[4]}/>
                            <FormLabel>Gender : </FormLabel>
                            <Input color={'black'} type='text' mb={'10px'} defaultValue={userdata[1]}/>
                            <FormLabel>Age : </FormLabel>
                            <Input color={'black'} type='text' mb={'10px'} defaultValue={userdata[3]}/>
                        </FormControl>
                    </Flex>
                ) : null}
            </Box>

                <Flex
                    flexDirection="column"
                    flexBasis="50%"
                    alignItems="center"
                    justifyContent="center"
                    backgroundColor={'#00695C'}
                    borderRadius={'25px'}
                >
                    <Box p="20px"
                        onClick={() => setProfileTrue()}
                        backgroundColor={'white'}
                        cursor={'pointer'}
                    >
                        {ip == ""?<>
                            <Spinner
                            thickness='4px'
                            speed='0.65s'
                            emptyColor='gray.200'
                            color='blue.500'
                            size='xl'
                            />
                        </>:profile?<HiOutlineUser size={130}/>:<QRCode value={ip} />}
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
                        {profile?<>Click profile icon to manual disconect from smart cart</>:<>Scan QR code to connect mobile app with your smart cart</>}
                    </Box>
                </Flex>
            </Flex>
        </Flex>
    );
};

export default Mobile;
