import React, { useEffect, useState } from "react";
import { useTheme } from "@chakra-ui/react";
import { AnimatePresence, motion } from "framer-motion";
import "./App.css";

import Nav from "./components/navbar/nav";
import Settings from "./components/dashbord/settings";
import Home from "./components/checkout/home"


function App() {
  const [darkMode, setDarkMode] = useState(false);
  const [settings, setSettings] = useState(false);
  const theme = useTheme();
  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  const toggleSettings = () => {
    setSettings(!settings);
  };
useEffect(() => {
  var hostname = window.location.hostname;
  // sessionStorage.setItem('host', 'http://'+hostname+':'+ window.location.port+'/api');
  sessionStorage.setItem('host', 'http://'+hostname+':5001');
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
    </div>
  );
}

export default App;