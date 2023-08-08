import { Box, Button, Flex } from '@chakra-ui/react';
import React, { useEffect, useState } from 'react';
import { GiEmptyWoodBucketHandle } from 'react-icons/gi';
import Swal from 'sweetalert2'
import CartProduct from './cartProduct';
import axios from 'axios';
import Loading from '../module/loading';

interface AppCart {
    darkMode: boolean;
    products: any;
    totalBill: number;
    handleCheckout:any;
}

interface Product {
    id: number;
    title: string;
    price: number;
    qty: number;
    totalPrice: number;
    categoryNo:number
}


const Cart: React.FC<AppCart> = ({ darkMode, products, totalBill,handleCheckout }) => {
    const [productList, setproductList] = useState<Product[]>([]);
    const [loadingVisible, setLoadingVisible] = useState(false);

    // Function to show the loading component
    const showLoading = () => {
      setLoadingVisible(true);
    };

    // Function to hide the loading component
    const hideLoading = () => {
      setLoadingVisible(false);
    };
    useEffect(() => {
        setproductList(products);
    }, []);
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
    const handleClick = () => {

        if(totalBill == 0){
            Toast.fire({
                icon: 'error',
                title: 'Please add items to cart'
              })
        }
       else 
        {   showLoading()
            const categoryNumbers = productList.map((product) => product.categoryNo);
            const myHost = sessionStorage.getItem('host');
            axios.post(`${myHost}/getcheckoutdata`, {
                productList: JSON.stringify(categoryNumbers),
                
            })
              .then(response => {
                Toast.fire({
                    icon: 'success',
                    title: 'Checkout Successfull'
                  })
                console.log(response.data);
                setproductList([]);
                handleCheckout();
                hideLoading()
              })
              .catch(error => {
                console.log(error);
                Toast.fire({
                    icon: 'error',
                    title: 'Checkout Not Successfull'
                  })
                  hideLoading()
              });
        }
       
          
    };
    return (
        <Flex direction="column" h='100%' w='100%' padding={'20px'}>
            <Box h={`calc(100% - 100px)`} w='100%' overflow={"auto"}
                borderBottom="1px" borderColor="gray.300" pb="20px" mb='10px'
            >
                {productList.length === 0 ?
                    <Box h={'100%'} color={darkMode ? "gray.600" : 'gray.300'} display="flex" alignItems="center" justifyContent="center">
                        <GiEmptyWoodBucketHandle size={150} style={{ fill: darkMode ? "gray.600" : 'gray.300' }} />
                    </Box>
                    : null}
                {productList.map((product) => (
                    <CartProduct darkMode={darkMode} Product={product} />
                ))}
            </Box>
            
            <Button
                onClick={handleClick}
                h='100px'
                w='100%'
                bg='gray'
                borderRadius='10px'
                _hover={{ bg: 'lightblue' }}
            >
                <Flex flexDirection="column" alignItems="center">
                    <Box
                        style={{
                            fontSize: '25px',
                            fontWeight: 'bold',
                            marginBottom: '10px',
                        }}
                    >
                        Checkout Here
                    </Box>


                    <Box
                        style={{
                            fontSize: '45px',
                            fontWeight: 'bold',
                            color: 'green',
                            textAlign: 'center',
                        }}
                    >
                        LKR : {totalBill.toFixed(2)}
                    </Box>
                </Flex>
            </Button>
            <Loading visible={loadingVisible} /> 
        </Flex>
    );
};

export default Cart;
