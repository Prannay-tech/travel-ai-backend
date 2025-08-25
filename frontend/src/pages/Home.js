import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Plane, Search, Sparkles, Star, TrendingUp, MessageCircle } from 'lucide-react';
import TravelChat from '../components/TravelChat';
import FloatingChatButton from '../components/FloatingChatButton';

const Home = () => {
  const [showChat, setShowChat] = useState(false);
  const navigate = useNavigate();

  const handleRecommendationsReady = (travelData) => {
    // Store the travel data and navigate to recommendations
    localStorage.setItem('travelPreferences', JSON.stringify(travelData));
    setShowChat(false);
    navigate('/recommendations', { state: { travelData } });
  };

  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <section className="text-center py-16 bg-gradient-to-br from-blue-50 to-indigo-100 rounded-2xl">
        <div className="max-w-4xl mx-auto px-4">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            Discover Your Perfect Trip with{' '}
            <span className="text-blue-600">AI</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Get personalized travel recommendations powered by artificial intelligence. 
            Find the best places to visit and flights to book based on your preferences.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button
              onClick={() => setShowChat(true)}
              className="inline-flex items-center justify-center px-8 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition-colors"
            >
              <MessageCircle className="h-5 w-5 mr-2" />
              Chat with AI Assistant
            </button>
            <Link
              to="/search"
              className="inline-flex items-center justify-center px-8 py-3 bg-white text-blue-600 font-semibold rounded-lg border-2 border-blue-600 hover:bg-blue-50 transition-colors"
            >
              <Search className="h-5 w-5 mr-2" />
              Search Destinations
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-12">
        <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
          Why Choose Travel AI?
        </h2>
        <div className="grid md:grid-cols-3 gap-8">
          <div className="text-center p-6 bg-white rounded-xl shadow-md">
            <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Sparkles className="h-8 w-8 text-blue-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              AI-Powered Recommendations
            </h3>
            <p className="text-gray-600">
              Get personalized travel suggestions based on your interests, budget, and preferences.
            </p>
          </div>
          
          <div className="text-center p-6 bg-white rounded-xl shadow-md">
            <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Search className="h-8 w-8 text-green-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              Smart Search
            </h3>
            <p className="text-gray-600">
              Find places and flights using natural language queries with semantic search.
            </p>
          </div>
          
          <div className="text-center p-6 bg-white rounded-xl shadow-md">
            <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <TrendingUp className="h-8 w-8 text-purple-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              Real-time Data
            </h3>
            <p className="text-gray-600">
              Access up-to-date information about places, flights, and travel trends.
            </p>
          </div>
        </div>
      </section>

      {/* Popular Destinations */}
      <section className="py-12">
        <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
          Popular Destinations
        </h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {[
            {
              name: 'Paris, France',
              image: 'https://images.unsplash.com/photo-1502602898536-47ad22581b52?w=400',
              rating: 8.5,
              description: 'The City of Light'
            },
            {
              name: 'Tokyo, Japan',
              image: 'https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=400',
              rating: 8.8,
              description: 'Modern meets traditional'
            },
            {
              name: 'New York, USA',
              image: 'https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?w=400',
              rating: 8.3,
              description: 'The Big Apple'
            },
            {
              name: 'Rome, Italy',
              image: 'https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=400',
              rating: 8.7,
              description: 'Eternal City'
            }
          ].map((destination, index) => (
            <div key={index} className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-lg transition-shadow">
              <div className="h-48 bg-gray-200 relative">
                <img
                  src={destination.image}
                  alt={destination.name}
                  className="w-full h-full object-cover"
                />
                <div className="absolute top-2 right-2 bg-white bg-opacity-90 rounded-full px-2 py-1 flex items-center">
                  <Star className="h-4 w-4 text-yellow-500 fill-current" />
                  <span className="ml-1 text-sm font-semibold">{destination.rating}</span>
                </div>
              </div>
              <div className="p-4">
                <h3 className="font-semibold text-gray-900 mb-1">{destination.name}</h3>
                <p className="text-sm text-gray-600">{destination.description}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* CTA Section */}
      <section className="text-center py-12 bg-blue-600 rounded-2xl text-white">
        <h2 className="text-3xl font-bold mb-4">
          Ready to Plan Your Next Adventure?
        </h2>
        <p className="text-xl mb-8 opacity-90">
          Let AI help you discover amazing destinations and find the best deals.
        </p>
        <Link
          to="/recommendations"
          className="inline-flex items-center justify-center px-8 py-3 bg-white text-blue-600 font-semibold rounded-lg hover:bg-gray-100 transition-colors"
        >
          <Plane className="h-5 w-5 mr-2" />
          Start Planning Now
        </Link>
      </section>
      
      {/* Chat Modal */}
      {showChat && (
        <TravelChat
          onClose={() => setShowChat(false)}
          onRecommendationsReady={handleRecommendationsReady}
        />
      )}
      
      {/* Floating Chat Button */}
      <FloatingChatButton
        onClick={() => setShowChat(true)}
        isVisible={!showChat}
      />
    </div>
  );
};

export default Home; 