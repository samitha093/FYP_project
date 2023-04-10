import { Flex, Image, IconButton, Hide } from '@chakra-ui/react';
import React, { useState, useEffect } from 'react';
import { ChevronLeftIcon, ChevronRightIcon } from '@chakra-ui/icons';

interface AppProps {
  darkMode: boolean;
}

const Slider: React.FC<AppProps> = ({ darkMode }) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [images, setImages] = useState([
    'https://via.placeholder.com/300x200?text=Image%201',
    'https://via.placeholder.com/300x200?text=Image%202',
    'https://via.placeholder.com/300x200?text=Image%203',
    'https://via.placeholder.com/300x200?text=Image%204',
    'https://via.placeholder.com/300x200?text=Image%205',
    'https://via.placeholder.com/300x200?text=Image%206',
    'https://via.placeholder.com/300x200?text=Image%207',
    'https://via.placeholder.com/300x200?text=Image%208',
    'https://via.placeholder.com/300x200?text=Image%209',
    'https://via.placeholder.com/300x200?text=Image%2010',
  ]);

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
              boxSize="200px"
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