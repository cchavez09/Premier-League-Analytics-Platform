// frontend/src/App.js
import React, { useEffect, useState } from 'react';
import Sidebar from './components/sidebar';
import Home from './pages/Home';
import Teams from "./components/TeamsFrontend";

function App() {
  return (
    <div style={{ display: "flex" }}>
      <Sidebar active="Home" />
      <Home />
    </div>
  );
}

export default App;
