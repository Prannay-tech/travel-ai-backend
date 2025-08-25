import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Search from './pages/Search';
import Recommendations from './pages/Recommendations';
import PlaceDetails from './pages/PlaceDetails';
import DestinationRecommendations from './pages/DestinationRecommendations';

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <main className="container mx-auto px-4 py-8">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/search" element={<Search />} />
          <Route path="/recommendations" element={<Recommendations />} />
          <Route path="/places/:placeId" element={<PlaceDetails />} />
          <Route path="/destinations" element={<DestinationRecommendations />} />
        </Routes>
      </main>
    </div>
  );
}

export default App; 