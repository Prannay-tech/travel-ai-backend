import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Plane, Clock, ArrowRight } from 'lucide-react';
import axios from 'axios';

const FlightSearch = ({ selectedDestination, travelData }) => {
  const navigate = useNavigate();
  const [flights, setFlights] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedFlight, setSelectedFlight] = useState(null);

  useEffect(() => {
    if (selectedDestination) {
      searchFlights();
    }
  }, [selectedDestination]);

  const searchFlights = async () => {
    if (!selectedDestination) return;

    setLoading(true);
    try {
      const response = await axios.post('/flights', {
        origin: travelData?.summary?.travel_from || 'New York',
        destination: selectedDestination.name,
        departure_date: '2024-12-01', // This would come from user input
        passengers: 1,
        currency: selectedDestination.currency || 'USD'
      });

      if (response.data.success) {
        setFlights(response.data.flights);
      }
    } catch (error) {
      console.error('Error searching flights:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFlightSelect = (flight) => {
    setSelectedFlight(flight);
  };

  const proceedToHotels = () => {
    if (selectedFlight) {
      navigate('/hotels');
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
          Flight Options to {selectedDestination.name}
        </h1>
        <p className="text-gray-600">
          Choose your preferred flight for your trip to {selectedDestination.country}
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
            <p className="text-sm text-gray-600">Estimated Flight Cost</p>
            <p className="text-2xl font-bold text-blue-600">
              {selectedDestination.currency} {selectedDestination.flight_cost_converted}
            </p>
          </div>
        </div>
      </div>

      {/* Flight Search Results */}
      <div className="bg-white rounded-lg shadow-lg overflow-hidden">
        <div className="p-6 border-b">
          <h2 className="text-xl font-semibold text-gray-900">Available Flights</h2>
          <p className="text-gray-600">Select your preferred flight option</p>
        </div>

        {loading ? (
          <div className="p-8 text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Searching for flights...</p>
          </div>
        ) : flights.length > 0 ? (
          <div className="divide-y">
            {flights.map((flight, index) => (
              <div
                key={index}
                className={`p-6 cursor-pointer transition-colors ${
                  selectedFlight === flight
                    ? 'bg-primary-50 border-l-4 border-primary-600'
                    : 'hover:bg-gray-50'
                }`}
                onClick={() => handleFlightSelect(flight)}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-6">
                    {/* Airline Info */}
                    <div className="text-center">
                      <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center mb-2">
                        <Plane className="h-6 w-6 text-primary-600" />
                      </div>
                      <p className="text-sm font-semibold text-gray-900">{flight.airline}</p>
                      <p className="text-xs text-gray-600">{flight.flight_number}</p>
                    </div>

                    {/* Flight Times */}
                    <div className="flex items-center space-x-4">
                      <div className="text-center">
                        <p className="text-lg font-bold text-gray-900">{flight.departure_time}</p>
                        <p className="text-sm text-gray-600">Departure</p>
                      </div>
                      <div className="flex items-center space-x-2">
                        <div className="w-16 h-px bg-gray-300"></div>
                        <Clock className="h-4 w-4 text-gray-400" />
                        <span className="text-sm text-gray-600">{flight.duration}</span>
                      </div>
                      <div className="text-center">
                        <p className="text-lg font-bold text-gray-900">{flight.arrival_time}</p>
                        <p className="text-sm text-gray-600">Arrival</p>
                      </div>
                    </div>

                    {/* Flight Details */}
                    <div className="text-center">
                      <p className="text-sm text-gray-600">Stops</p>
                      <p className="font-semibold text-gray-900">
                        {flight.stops === 0 ? 'Direct' : `${flight.stops} stop${flight.stops > 1 ? 's' : ''}`}
                      </p>
                    </div>
                  </div>

                  {/* Price and Selection */}
                  <div className="text-right">
                    <p className="text-2xl font-bold text-green-600">
                      {flight.currency} {flight.price}
                    </p>
                    <p className="text-sm text-gray-600">per passenger</p>
                    {selectedFlight === flight && (
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
            <Plane className="h-12 w-12 text-gray-300 mx-auto mb-4" />
            <p className="text-gray-600">No flights found for the selected dates.</p>
          </div>
        )}
      </div>

      {/* Action Buttons */}
      <div className="mt-8 flex justify-between items-center">
        <button
          onClick={() => navigate('/destinations')}
          className="bg-gray-600 text-white px-6 py-3 rounded-lg hover:bg-gray-700 transition-colors"
        >
          Back to Destinations
        </button>
        
        <button
          onClick={proceedToHotels}
          disabled={!selectedFlight}
          className="bg-primary-600 text-white px-6 py-3 rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center space-x-2"
        >
          <span>Continue to Hotels</span>
          <ArrowRight className="h-4 w-4" />
        </button>
      </div>

      {/* Selected Flight Summary */}
      {selectedFlight && (
        <div className="mt-6 bg-green-50 border border-green-200 rounded-lg p-4">
          <h3 className="font-semibold text-green-800 mb-2">Selected Flight:</h3>
          <p className="text-green-700">
            {selectedFlight.airline} {selectedFlight.flight_number} - {selectedFlight.currency} {selectedFlight.price}
          </p>
        </div>
      )}
    </div>
  );
};

export default FlightSearch;
