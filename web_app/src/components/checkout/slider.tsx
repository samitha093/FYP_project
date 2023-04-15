import { Flex, Image, IconButton, Hide } from '@chakra-ui/react';
import React, { useState, useEffect } from 'react';
import { ChevronLeftIcon, ChevronRightIcon } from '@chakra-ui/icons';
import axios from 'axios';

interface AppProps {
  darkMode: boolean;
}


const Slider: React.FC<AppProps> = ({ darkMode }) => {
  const [currentIndex, setCurrentIndex] = useState(0);

  const [images, setImages] = useState([]);


  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentIndex((currentIndex + 1) % images.length);
    }, 3000);
    return () => clearInterval(interval);
  }, [currentIndex, images.length]);

  const handlePrev = () => {
    setCurrentIndex((currentIndex - 1 + images.length) % images.length);
  };

  const handleNext = () => {
    setCurrentIndex((currentIndex + 1) % images.length);
  };

  useEffect(() => {
    axios.get('http://127.0.0.1:5001/threandsImages')
      .then(response => {
        setImages(response.data);
      })
      .catch(error => {
        console.error(error);
      });
  }, []);
  
  return (
    <Flex alignItems="center" justifyContent="center" flexDirection="column" w={'100%'} h={'100%'} >
      <Flex alignItems="center" justifyContent="center">
        <IconButton
          aria-label="Previous"
          icon={<ChevronLeftIcon />}
          onClick={handlePrev}
          mr={2}
        />

        {[2, 1, 0].map((offset) => {
          const index = (currentIndex + offset) % images.length;
          return (
            <Image
              key={index}
              src={images[index]}
              alt={`Image ${index + 1}`}
              boxSize="150px"
              objectFit="cover"
              mr={2}
            />
          );
        })}
        <IconButton
          aria-label="Next"
          icon={<ChevronRightIcon />}
          onClick={handleNext}
          ml={2}
        />
      </Flex>
    </Flex>
  );
};

export default Slider;