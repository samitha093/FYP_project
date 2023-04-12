import { Box, Button, Center, Flex, Modal, ModalBody, ModalCloseButton, ModalContent, ModalHeader, ModalOverlay } from '@chakra-ui/react';
import React, { useEffect, useState } from 'react';
import { BsQrCodeScan } from 'react-icons/bs';

import Item from "./item"
import Cart from "./cart"
import Slider from "./slider"
import Scanner from './qr';
import { AddIcon } from '@chakra-ui/icons';

interface AppProps {
    darkMode: boolean;
}

interface Product {
    id: number;
    title: string;
    price: number;
    qty: number;
    totalPrice: number;
}

const Checkout: React.FC<AppProps> = ({ darkMode }) => {
    const [showScanner, setShowScanner] = useState(false);
    const openScanner = () => setShowScanner(true);
    const closeScanner = () => setShowScanner(false);
    const [qrData, setqrData] = useState("");
    const [product, setproduct] = useState(false);
    const [products, setProducts] = useState<Product[]>([]);

    const handleQR = (e: any) => {
        if (!(e === null || e === "")) {
            closeScanner();
            setqrData(e);
        }
      };
    const handleProduct = (e: any) => {
        setqrData("");
        setproduct(false);
      };
    const handleAddProduct = (e: any) => {
        const newProduct: Product = {
            id: 1,
            title: 'Product 1',
            price: 99.99,
            qty: 2,
            totalPrice: 188.99,
          };
          setProducts([...products, newProduct]);
      };
    useEffect(() => {
        if (!(qrData === null || qrData === "")) {
            setproduct(true);
        }
    }, [qrData]);
    return (
        <Flex w="100%" h="100%" overflow={'auto'}>
            <Box flex="1" h="100%" mx="20px" borderRadius="30px">
                <Box flex="1" w="100%" h="30%" border="2px" borderColor={darkMode ? "gray.600" : 'gray.300'} borderRadius="30px" mb="3%" overflow={"hidden"}>
                    <Slider darkMode={darkMode}/>
                </Box>
                <Box flex="1" w="100%" h="66%" border="2px" borderColor={darkMode ? "gray.600" : 'gray.300'} borderRadius="30px">
                    {product?
                    <Item darkMode={darkMode} handleProduct={handleProduct} handleAddProduct={handleAddProduct}/>
                    :
                    <Flex
                        justify="space-between"
                        align="center"
                        w={'calc(100% - 80px)'}
                        h={'calc(100% - 80px)'}
                        borderWidth="5px"
                        borderStyle="dashed"
                        borderColor={darkMode ? "gray.600" : 'gray.300'}
                        borderRadius="20px"
                        justifyContent="center"
                        _hover={{ cursor: 'pointer' }}
                        margin={'40px'}
                        onClick={openScanner}
                        >
                        <Flex margin="30px" h="inherit" w="inherit" color={darkMode ? "gray.600" : 'gray.300'} direction="column" alignItems="center" justifyContent="center">
                            <BsQrCodeScan size={64} style={{ fill: darkMode ? "gray.600" : 'gray.300' }} />
                            <Box mt={5} color={darkMode ? "gray.600" : 'gray.300'}
                            fontSize={30}>
                                Press here to scan QR code
                            </Box>
                        </Flex>
                        </Flex>
                    }
                </Box>
            </Box>
            <Box w="40%" h="100%" border="2px" borderColor={darkMode ? "gray.600" : 'gray.300'} borderRadius="30px">
                <Cart darkMode={darkMode} products={products} key={JSON.stringify(products)}/>
            </Box>
            <Modal closeOnOverlayClick={false} isOpen={showScanner} onClose={closeScanner}>
                <ModalOverlay />
                <ModalContent>
                    <ModalHeader>Scan QR Code</ModalHeader>
                    <ModalCloseButton />
                    <ModalBody>
                        <Scanner datasender={handleQR}/>
                    </ModalBody>
                </ModalContent>
            </Modal>
        </Flex>
    );
};

export default Checkout;
