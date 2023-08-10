import React, { useEffect, useState } from "react";
import { Flex, Modal, ModalBody, ModalCloseButton, ModalContent, ModalHeader, ModalOverlay, useTheme } from "@chakra-ui/react";
import { AnimatePresence, motion } from "framer-motion";
import QRCode from 'qrcode.react';
import "./App.css";

import Nav from "./components/navbar/nav";
import Settings from "./components/dashbord/settings";
import Home from "./components/checkout/home"
import axios from "axios";
import Loading from "./components/module/loading";


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
  return (
    <div style={{ backgroundColor: darkMode ? theme.colors.gray[700] : "white", height:"100vh" ,overflow: 'hidden' }} >
      <Loading visible={false} /> {/* To show the spinner */}

     
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
    </div>
  );
}

export default App;