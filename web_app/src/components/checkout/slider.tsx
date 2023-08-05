import { Flex, Image, IconButton } from '@chakra-ui/react';
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
    const myHost = sessionStorage.getItem('host');
    axios
      .get(`${myHost}/threandsImages`)
      .then(response => {
        const imageUrls = response.data.map((item: { ImageUrl: any; }) => item.ImageUrl);
        setImages(imageUrls);
      })
      .catch(error => {
        console.log("Error when loading recommend items")
      });
  }, []);

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
  const visibleImages = [
    images[(currentIndex + images.length - 1) % images.length],
    images[currentIndex],
    images[(currentIndex + 1) % images.length],
  ];
  return (
    <Flex alignItems="center" justifyContent="center" flexDirection="column" w={'100%'} h={'100%'} >
      <Flex alignItems="center" justifyContent="center">
        <IconButton
          aria-label="Previous"
          icon={<ChevronLeftIcon />}
          onClick={handlePrev}
          mr={2}
        />
        {visibleImages.map((image, index) => (
          <Image
            key={index}
            src={image}
            alt={`Image ${index + 1}`}
            boxSize="150px"
            objectFit="cover"
            mr={2}
          />
        ))}

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
