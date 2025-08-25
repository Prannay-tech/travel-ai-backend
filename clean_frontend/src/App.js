import React, { useState } from 'react';
import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import ChatInterface from './components/ChatInterface';
import DestinationResults from './pages/DestinationResults';
import FlightSearch from './pages/FlightSearch';
import HotelSearch from './pages/HotelSearch';
import ActivityPlanning from './pages/ActivityPlanning';
import './App.css';

function App() {
  const [travelData, setTravelData] = useState(null);
  const [selectedDestination, setSelectedDestination] = useState(null);

  return (
    <div className="min-h-screen bg-dark-gradient text-gray-100">
      <Navbar />
      <main className="container mx-auto px-4 py-8">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route 
            path="/chat" 
            element={
              <ChatInterface 
                setTravelData={setTravelData}
                setSelectedDestination={setSelectedDestination}
              />
            } 
          />
          <Route 
            path="/destinations" 
            element={
              <DestinationResults 
                travelData={travelData}
                setSelectedDestination={setSelectedDestination}
              />
            } 
          />
          <Route 
            path="/flights" 
            element={
              <FlightSearch 
                selectedDestination={selectedDestination}
                travelData={travelData}
              />
            } 
          />
          <Route 
            path="/hotels" 
            element={
              <HotelSearch 
                selectedDestination={selectedDestination}
                travelData={travelData}
              />
            } 
          />
          <Route 
            path="/activities" 
            element={
              <ActivityPlanning 
                selectedDestination={selectedDestination}
                travelData={travelData}
              />
            } 
          />
        </Routes>
      </main>
    </div>
  );
}

export default App;
