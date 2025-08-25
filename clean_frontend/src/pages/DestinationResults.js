import React from 'react';
import { useNavigate } from 'react-router-dom';
import { MapPin, Star, Calendar, Plane, ArrowRight } from 'lucide-react';

const DestinationResults = ({ travelData, setSelectedDestination }) => {
  const navigate = useNavigate();

  if (!travelData || !travelData.destinations) {
    return (
      <div className="text-center py-16">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">No destinations found</h2>
        <p className="text-gray-600 mb-6">Please start by chatting with our AI to get personalized recommendations.</p>
        <button
          onClick={() => navigate('/chat')}
          className="bg-primary-600 text-white px-6 py-3 rounded-lg hover:bg-primary-700 transition-colors"
        >
          Start Planning
        </button>
      </div>
    );
  }

  const handleDestinationSelect = (destination) => {
    setSelectedDestination(destination);
    navigate('/flights');
  };

  return (
    <div className="max-w-6xl mx-auto">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          Your Perfect Destinations
        </h1>
        <p className="text-gray-600">
          Based on your preferences, here are the top {travelData.destinations.length} destinations for you
        </p>
      </div>

      {/* Summary */}
      {travelData.summary && (
        <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Trip Summary</h2>
          <div className="grid md:grid-cols-4 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-primary-600">{travelData.summary.total_destinations}</div>
              <div className="text-sm text-gray-600">Destinations</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">
                {travelData.summary.currency} {travelData.summary.average_daily_cost}
              </div>
              <div className="text-sm text-gray-600">Avg Daily Cost</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">
                {travelData.summary.currency} {travelData.summary.average_flight_cost}
              </div>
              <div className="text-sm text-gray-600">Avg Flight Cost</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-purple-600 capitalize">
                {travelData.summary.travel_type}
              </div>
              <div className="text-sm text-gray-600">Travel Type</div>
            </div>
          </div>
        </div>
      )}

      {/* Destinations Grid */}
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {travelData.destinations.map((destination, index) => (
          <div
            key={index}
            className="bg-white rounded-lg shadow-lg overflow-hidden destination-card cursor-pointer"
            onClick={() => handleDestinationSelect(destination)}
          >
            {/* Image */}
            <div className="h-48 bg-gray-200 relative">
              <img
                src={destination.image}
                alt={destination.name}
                className="w-full h-full object-cover"
                onError={(e) => {
                  e.target.src = 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4';
                }}
              />
              <div className="absolute top-4 right-4 bg-white px-2 py-1 rounded-full text-sm font-semibold text-gray-800">
                {destination.rating}/10
              </div>
            </div>

            {/* Content */}
            <div className="p-6">
              <div className="flex items-start justify-between mb-2">
                <h3 className="text-xl font-bold text-gray-900">{destination.name}</h3>
                <div className="flex items-center text-yellow-500">
                  <Star className="h-4 w-4 fill-current" />
                  <span className="ml-1 text-sm">{destination.rating}</span>
                </div>
              </div>

              <div className="flex items-center text-gray-600 mb-3">
                <MapPin className="h-4 w-4 mr-1" />
                <span className="text-sm">
                  {destination.state && `${destination.state}, `}{destination.country}
                </span>
              </div>

              <p className="text-gray-600 text-sm mb-4 line-clamp-2">
                {destination.description}
              </p>

              {/* Highlights */}
              <div className="mb-4">
                <h4 className="text-sm font-semibold text-gray-900 mb-2">Highlights:</h4>
                <div className="flex flex-wrap gap-1">
                  {destination.highlights.slice(0, 3).map((highlight, idx) => (
                    <span
                      key={idx}
                      className="bg-primary-100 text-primary-800 text-xs px-2 py-1 rounded"
                    >
                      {highlight}
                    </span>
                  ))}
                </div>
              </div>

              {/* Pricing */}
              <div className="border-t pt-4">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm text-gray-600">Daily Cost:</span>
                  <span className="font-semibold text-green-600">
                    {destination.currency} {destination.daily_cost_converted}
                  </span>
                </div>
                <div className="flex justify-between items-center mb-4">
                  <span className="text-sm text-gray-600">Flight Cost:</span>
                  <span className="font-semibold text-blue-600">
                    {destination.currency} {destination.flight_cost_converted}
                  </span>
                </div>
                <button className="w-full bg-primary-600 text-white py-2 rounded-lg hover:bg-primary-700 transition-colors flex items-center justify-center space-x-2">
                  <span>Select Destination</span>
                  <ArrowRight className="h-4 w-4" />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Next Steps */}
      <div className="mt-12 text-center">
        <h3 className="text-xl font-semibold text-gray-900 mb-4">What's Next?</h3>
        <p className="text-gray-600 mb-6">
          Select a destination to start booking your flights, hotels, and activities
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <div className="flex items-center space-x-2 text-gray-600">
            <Plane className="h-5 w-5 text-primary-600" />
            <span>1. Book Flights</span>
          </div>
          <div className="flex items-center space-x-2 text-gray-600">
            <Calendar className="h-5 w-5 text-primary-600" />
            <span>2. Find Hotels</span>
          </div>
          <div className="flex items-center space-x-2 text-gray-600">
            <MapPin className="h-5 w-5 text-primary-600" />
            <span>3. Plan Activities</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DestinationResults;
