import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { MapPin, Star, Users, ArrowRight } from 'lucide-react';
import axios from 'axios';

const HotelSearch = ({ selectedDestination, travelData }) => {
  const navigate = useNavigate();
  const [hotels, setHotels] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedHotel, setSelectedHotel] = useState(null);

  useEffect(() => {
    if (selectedDestination) {
      searchHotels();
    }
  }, [selectedDestination]);

  const searchHotels = async () => {
    if (!selectedDestination) return;

    setLoading(true);
    try {
      const response = await axios.post('/hotels', {
        destination: selectedDestination.name,
        check_in: '2024-12-01', // This would come from user input
        check_out: '2024-12-08',
        guests: 1,
        rooms: 1,
        currency: selectedDestination.currency || 'USD'
      });

      if (response.data.success) {
        setHotels(response.data.hotels);
      }
    } catch (error) {
      console.error('Error searching hotels:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleHotelSelect = (hotel) => {
    setSelectedHotel(hotel);
  };

  const proceedToActivities = () => {
    if (selectedHotel) {
      navigate('/activities');
    }
  };

  if (!selectedDestination) {
    return (
      <div className="text-center py-16">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">No destination selected</h2>
        <p className="text-gray-600 mb-6">Please select a destination first.</p>
        <button
          onClick={() => navigate('/destinations')}
          className="bg-primary-600 text-white px-6 py-3 rounded-lg hover:bg-primary-700 transition-colors"
        >
          Choose Destination
        </button>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          Hotels in {selectedDestination.name}
        </h1>
        <p className="text-gray-600">
          Choose your accommodation for your stay in {selectedDestination.country}
        </p>
      </div>

      {/* Destination Info */}
      <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <img
              src={selectedDestination.image}
              alt={selectedDestination.name}
              className="w-16 h-16 rounded-lg object-cover"
            />
            <div>
              <h3 className="text-xl font-bold text-gray-900">{selectedDestination.name}</h3>
              <p className="text-gray-600">{selectedDestination.country}</p>
            </div>
          </div>
          <div className="text-right">
            <p className="text-sm text-gray-600">Estimated Daily Cost</p>
            <p className="text-2xl font-bold text-green-600">
              {selectedDestination.currency} {selectedDestination.daily_cost_converted}
            </p>
          </div>
        </div>
      </div>

      {/* Hotel Search Results */}
      <div className="bg-white rounded-lg shadow-lg overflow-hidden">
        <div className="p-6 border-b">
          <h2 className="text-xl font-semibold text-gray-900">Available Hotels</h2>
          <p className="text-gray-600">Select your preferred accommodation</p>
        </div>

        {loading ? (
          <div className="p-8 text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Searching for hotels...</p>
          </div>
        ) : hotels.length > 0 ? (
          <div className="divide-y">
            {hotels.map((hotel, index) => (
              <div
                key={index}
                className={`p-6 cursor-pointer transition-colors ${
                  selectedHotel === hotel
                    ? 'bg-primary-50 border-l-4 border-primary-600'
                    : 'hover:bg-gray-50'
                }`}
                onClick={() => handleHotelSelect(hotel)}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-6">
                    {/* Hotel Info */}
                    <div className="text-center">
                      <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center mb-2">
                        <Users className="h-6 w-6 text-primary-600" />
                      </div>
                      <p className="text-sm font-semibold text-gray-900">{hotel.name}</p>
                      <div className="flex items-center justify-center space-x-1 mt-1">
                        {[...Array(5)].map((_, i) => (
                          <Star
                            key={i}
                            className={`h-3 w-3 ${
                              i < Math.floor(hotel.rating)
                                ? 'text-yellow-400 fill-current'
                                : 'text-gray-300'
                            }`}
                          />
                        ))}
                        <span className="text-xs text-gray-600 ml-1">{hotel.rating}</span>
                      </div>
                    </div>

                    {/* Location */}
                    <div className="flex items-center space-x-2">
                      <MapPin className="h-4 w-4 text-gray-400" />
                      <span className="text-sm text-gray-600">{hotel.location}</span>
                    </div>

                    {/* Amenities */}
                    <div className="flex items-center space-x-2">
                      {hotel.amenities.map((amenity, idx) => (
                        <span
                          key={idx}
                          className="bg-gray-100 text-gray-700 px-2 py-1 rounded text-xs"
                        >
                          {amenity}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* Price and Selection */}
                  <div className="text-right">
                    <p className="text-2xl font-bold text-green-600">
                      {hotel.currency} {hotel.price_per_night}
                    </p>
                    <p className="text-sm text-gray-600">per night</p>
                    {selectedHotel === hotel && (
                      <div className="mt-2">
                        <span className="bg-primary-600 text-white px-3 py-1 rounded-full text-xs">
                          Selected
                        </span>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="p-8 text-center">
            <Users className="h-12 w-12 text-gray-300 mx-auto mb-4" />
            <p className="text-gray-600">No hotels found for the selected dates.</p>
          </div>
        )}
      </div>

      {/* Action Buttons */}
      <div className="mt-8 flex justify-between items-center">
        <button
          onClick={() => navigate('/flights')}
          className="bg-gray-600 text-white px-6 py-3 rounded-lg hover:bg-gray-700 transition-colors"
        >
          Back to Flights
        </button>
        
        <button
          onClick={proceedToActivities}
          disabled={!selectedHotel}
          className="bg-primary-600 text-white px-6 py-3 rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center space-x-2"
        >
          <span>Continue to Activities</span>
          <ArrowRight className="h-4 w-4" />
        </button>
      </div>

      {/* Selected Hotel Summary */}
      {selectedHotel && (
        <div className="mt-6 bg-green-50 border border-green-200 rounded-lg p-4">
          <h3 className="font-semibold text-green-800 mb-2">Selected Hotel:</h3>
          <p className="text-green-700">
            {selectedHotel.name} - {selectedHotel.currency} {selectedHotel.price_per_night} per night
          </p>
        </div>
      )}
    </div>
  );
};

export default HotelSearch;
