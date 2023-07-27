import React, { useEffect, useState } from "react";
import { Flex, Modal, ModalBody, ModalCloseButton, ModalContent, ModalHeader, ModalOverlay, useTheme } from "@chakra-ui/react";
import { AnimatePresence, motion } from "framer-motion";
import QRCode from 'qrcode.react';
import "./App.css";

import Nav from "./components/navbar/nav";
import Settings from "./components/dashbord/settings";
import Home from "./components/checkout/home"
import axios from "axios";


function App() {
  const [darkMode, setDarkMode] = useState(false);
  const [settings, setSettings] = useState(false);
  const [showScanner, setShowScanner] = useState(true);
  const openScanner = () => setShowScanner(true);
  const closeScanner = () => setShowScanner(false);
  const [ip, setIp] = useState("");

  const theme = useTheme();

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  const toggleSettings = () => {
    setSettings(!settings);
  };
useEffect(() => {
  var hostname = 'http://'+ window.location.hostname+ ':5001';
  // sessionStorage.setItem('host', 'http://'+hostname+':'+ window.location.port+'/api');
  sessionStorage.setItem('host', hostname);
  axios.get(`${hostname}/getlocalip`)
  .then(response => {
    var uri = response.data + ":9999";
    setIp(uri);
    // console.log(response.data);
  })
  .catch(error => {
    console.error(error);
  });

}, []);
  return (
    <div style={{ backgroundColor: darkMode ? theme.colors.gray[700] : "white", height:"100vh" ,overflow: 'hidden' }} >
      <Nav darkMode={darkMode} toggleDarkMode={toggleDarkMode} settings={settings} toggleSettings={toggleSettings} />
      <div className="main-content" style={{ overflow: 'hidden' }}>
        <AnimatePresence>
          {settings ? (
              <Settings darkMode={darkMode} />
          ) : (
              <Home darkMode={darkMode} />
          )}
        </AnimatePresence>
      </div>
      <>
      <Flex w="100%" h="100%" align="center" justify="center" overflow="auto">
        <Modal closeOnOverlayClick={false} isOpen={showScanner} onClose={closeScanner}>
          <ModalOverlay />
          <ModalContent>
            <ModalHeader>Connect your Mobile Device</ModalHeader>
            <ModalCloseButton />
            <ModalBody>
              <Flex align="center" justify="center" mb={10}>
                <QRCode value={ip} />
              </Flex>
            </ModalBody>
          </ModalContent>
        </Modal>
      </Flex>
      </>
    </div>
  );
}

export default App;