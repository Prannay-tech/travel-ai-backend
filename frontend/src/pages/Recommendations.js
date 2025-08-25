import React, { useState, useEffect } from 'react';
import { useMutation } from 'react-query';
import { useLocation } from 'react-router-dom';
import { Sparkles, MapPin, Star, Plane, Calendar, DollarSign, Clock, MessageCircle } from 'lucide-react';
// import axios from 'axios'; // Will be used when backend is connected
import toast from 'react-hot-toast';
import { generateRecommendations } from '../utils/mockRecommendations';

const Recommendations = () => {
  const location = useLocation();
  const [formData, setFormData] = useState({
    user_preferences: '',
    budget: '',
    duration: '',
    interests: []
  });

  const [recommendations, setRecommendations] = useState(null);
  const [travelDataFromChat, setTravelDataFromChat] = useState(null);

  // Check if we have travel data from chat
  useEffect(() => {
    if (location.state?.travelData) {
      setTravelDataFromChat(location.state.travelData);
      // Pre-fill form with chat data
      setFormData({
        user_preferences: location.state.travelData.destination || '',
        budget: location.state.travelData.budget || '',
        duration: '7', // Default duration
        interests: []
      });
    } else {
      // Check localStorage for saved preferences
      const savedPreferences = localStorage.getItem('travelPreferences');
      if (savedPreferences) {
        const parsedData = JSON.parse(savedPreferences);
        setTravelDataFromChat(parsedData);
        setFormData({
          user_preferences: parsedData.destination || '',
          budget: parsedData.budget || '',
          duration: '7',
          interests: []
        });
      }
    }
  }, [location.state]);

  const getRecommendations = async (data) => {
    try {
      // Use mock recommendations for now
      // const response = await axios.post('/recommendations', data);
      // return response.data;
      
      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Generate mock recommendations
      const mockData = generateRecommendations(data);
      return mockData;
    } catch (error) {
      toast.error('Error getting recommendations');
      throw error;
    }
  };

  const { mutate: fetchRecommendations, isLoading } = useMutation(
    getRecommendations,
    {
      onSuccess: (data) => {
        setRecommendations(data);
        toast.success('Recommendations generated successfully!');
      },
      onError: () => {
        toast.error('Failed to generate recommendations');
      }
    }
  );

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!formData.user_preferences.trim()) {
      toast.error('Please describe your travel preferences');
      return;
    }
    
    // If we have chat data, use it to enhance the recommendations
    const enhancedData = {
      ...formData,
      destination: travelDataFromChat?.destination || formData.user_preferences,
      budget: travelDataFromChat?.budget || formData.budget,
      travelDates: travelDataFromChat?.travelDates || '',
      currentLocation: travelDataFromChat?.currentLocation || '',
      preferences: travelDataFromChat?.preferences || '',
      currency: travelDataFromChat?.currency || 'USD',
      travelType: travelDataFromChat?.travelType || 'international'
    };
    
    fetchRecommendations(enhancedData);
  };

  const handleInterestToggle = (interest) => {
    setFormData(prev => ({
      ...prev,
      interests: prev.interests.includes(interest)
        ? prev.interests.filter(i => i !== interest)
        : [...prev.interests, interest]
    }));
  };

  const interestOptions = [
    'Culture & History',
    'Nature & Outdoors',
    'Food & Dining',
    'Adventure & Sports',
    'Relaxation & Wellness',
    'Shopping',
    'Nightlife',
    'Family Activities'
  ];

  return (
    <div className="max-w-6xl mx-auto">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          AI Travel Recommendations
        </h1>
        <p className="text-lg text-gray-600">
          Tell us about your preferences and let AI create your perfect itinerary
        </p>
      </div>

      {/* Chat Data Summary */}
      {travelDataFromChat && (
        <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl p-6 mb-8">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-gray-900 flex items-center">
              <MessageCircle className="h-5 w-5 mr-2 text-blue-600" />
              Your Chat Preferences
            </h2>
            <button
              onClick={() => {
                setTravelDataFromChat(null);
                localStorage.removeItem('travelPreferences');
              }}
              className="text-sm text-gray-500 hover:text-gray-700"
            >
              Clear
            </button>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-6 gap-4">
            {travelDataFromChat.destination && (
              <div className="bg-white rounded-lg p-3">
                <div className="flex items-center text-sm text-gray-600 mb-1">
                  <MapPin className="h-4 w-4 mr-1" />
                  Destination Type
                </div>
                <div className="font-medium text-gray-900">{travelDataFromChat.destination}</div>
              </div>
            )}
            {travelDataFromChat.travelType && (
              <div className="bg-white rounded-lg p-3">
                <div className="flex items-center text-sm text-gray-600 mb-1">
                  <Plane className="h-4 w-4 mr-1" />
                  Travel Type
                </div>
                <div className="font-medium text-gray-900 capitalize">{travelDataFromChat.travelType}</div>
              </div>
            )}
            {travelDataFromChat.budget && (
              <div className="bg-white rounded-lg p-3">
                <div className="flex items-center text-sm text-gray-600 mb-1">
                  <DollarSign className="h-4 w-4 mr-1" />
                  Budget
                </div>
                <div className="font-medium text-gray-900">{travelDataFromChat.budget}</div>
              </div>
            )}
            {travelDataFromChat.currency && (
              <div className="bg-white rounded-lg p-3">
                <div className="flex items-center text-sm text-gray-600 mb-1">
                  <DollarSign className="h-4 w-4 mr-1" />
                  Currency
                </div>
                <div className="font-medium text-gray-900">{travelDataFromChat.currency}</div>
              </div>
            )}
            {travelDataFromChat.travelDates && (
              <div className="bg-white rounded-lg p-3">
                <div className="flex items-center text-sm text-gray-600 mb-1">
                  <Calendar className="h-4 w-4 mr-1" />
                  Travel Dates
                </div>
                <div className="font-medium text-gray-900">{travelDataFromChat.travelDates}</div>
              </div>
            )}
            {travelDataFromChat.currentLocation && (
              <div className="bg-white rounded-lg p-3">
                <div className="flex items-center text-sm text-gray-600 mb-1">
                  <Plane className="h-4 w-4 mr-1" />
                  Traveling From
                </div>
                <div className="font-medium text-gray-900">{travelDataFromChat.currentLocation}</div>
              </div>
            )}
          </div>
        </div>
      )}

      <div className="grid lg:grid-cols-2 gap-8">
        {/* Form Section */}
        <div className="bg-white rounded-xl shadow-md p-6">
          <h2 className="text-2xl font-semibold text-gray-900 mb-6">
            Your Travel Preferences
          </h2>
          
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Travel Description */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Describe your ideal trip
              </label>
              <textarea
                value={formData.user_preferences}
                onChange={(e) => setFormData({...formData, user_preferences: e.target.value})}
                placeholder="e.g., I want to explore European cities with rich history, enjoy local cuisine, and visit museums. I prefer walking tours and cultural experiences."
                rows={4}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
            </div>

            {/* Budget */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Budget (USD)
              </label>
              <div className="relative">
                <DollarSign className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                <input
                  type="number"
                  value={formData.budget}
                  onChange={(e) => setFormData({...formData, budget: e.target.value})}
                  placeholder="e.g., 3000"
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>

            {/* Duration */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Trip Duration (days)
              </label>
              <div className="relative">
                <Clock className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                <input
                  type="number"
                  value={formData.duration}
                  onChange={(e) => setFormData({...formData, duration: e.target.value})}
                  placeholder="e.g., 7"
                  min="1"
                  max="30"
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>

            {/* Interests */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Interests (select all that apply)
              </label>
              <div className="grid grid-cols-2 gap-2">
                {interestOptions.map((interest) => (
                  <label key={interest} className="flex items-center">
                    <input
                      type="checkbox"
                      checked={formData.interests.includes(interest)}
                      onChange={() => handleInterestToggle(interest)}
                      className="mr-2 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                    />
                    <span className="text-sm text-gray-700">{interest}</span>
                  </label>
                ))}
              </div>
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full flex items-center justify-center px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
            >
              {isLoading ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                  Generating Recommendations...
                </>
              ) : (
                <>
                  <Sparkles className="h-5 w-5 mr-2" />
                  Get AI Recommendations
                </>
              )}
            </button>
          </form>
        </div>

        {/* Results Section */}
        <div className="bg-white rounded-xl shadow-md p-6">
          <h2 className="text-2xl font-semibold text-gray-900 mb-6">
            Your Personalized Recommendations
          </h2>
          
          {isLoading && (
            <div className="text-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
              <p className="text-gray-600">AI is analyzing your preferences...</p>
            </div>
          )}

          {recommendations && (
            <div className="space-y-6">
              {/* Summary */}
              {recommendations.summary && (
                <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-4 mb-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-3">
                    Trip Summary
                  </h3>
                  <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
                    <div>
                      <p className="text-sm text-gray-600">Travel Type</p>
                      <p className="font-medium capitalize">{recommendations.summary.travelType}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Currency</p>
                      <p className="font-medium">{recommendations.summary.currency}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Best Time to Visit</p>
                      <p className="font-medium">{recommendations.summary.bestTimeToVisit}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Destinations Found</p>
                      <p className="font-medium">{recommendations.summary.totalDestinations}</p>
                    </div>
                  </div>
                  <div className="grid md:grid-cols-2 gap-4 mb-4">
                    <div>
                      <p className="text-sm text-gray-600">Average Daily Cost</p>
                      <p className="font-medium">{recommendations.summary.currency} {Math.round(recommendations.summary.averageCost)}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Average Flight Cost</p>
                      <p className="font-medium">{recommendations.summary.currency} {Math.round(recommendations.summary.averageFlightCost)}</p>
                    </div>
                  </div>
                  {recommendations.summary.travelTips && recommendations.summary.travelTips.length > 0 && (
                    <div className="mt-4">
                      <p className="text-sm text-gray-600 mb-2">Travel Tips:</p>
                      <ul className="space-y-1">
                        {recommendations.summary.travelTips.map((tip, index) => (
                          <li key={index} className="flex items-start gap-2 text-sm">
                            <span className="w-1.5 h-1.5 bg-blue-600 rounded-full mt-2 flex-shrink-0"></span>
                            <span>{tip}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              )}

              {/* Places */}
              {recommendations.places && recommendations.places.length > 0 && (
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-3">
                    Recommended Destinations
                  </h3>
                  <div className="grid md:grid-cols-2 gap-4">
                    {recommendations.places.map((place, index) => (
                      <div key={index} className="border border-gray-200 rounded-lg overflow-hidden hover:shadow-md transition-shadow">
                        <div className="h-48 bg-gray-200 relative">
                          <img
                            src={place.image}
                            alt={place.name}
                            className="w-full h-full object-cover"
                          />
                          <div className="absolute top-2 right-2 bg-white bg-opacity-90 rounded-full px-2 py-1 flex items-center">
                            <Star className="h-4 w-4 text-yellow-500 fill-current" />
                            <span className="ml-1 text-sm font-semibold">{place.rating}</span>
                          </div>
                        </div>
                        <div className="p-4">
                          <h4 className="font-semibold text-gray-900 mb-1">{place.name}</h4>
                          <p className="text-sm text-gray-600 mb-2">{place.country}</p>
                          <p className="text-sm text-gray-700 mb-3">{place.description}</p>
                          <div className="flex justify-between items-center">
                            <div className="text-sm text-gray-600">
                              <DollarSign className="h-4 w-4 inline mr-1" />
                              {place.currency || 'USD'} {place.cost_day_converted || place.cost_day_usd}/day
                            </div>
                            <div className="text-xs text-gray-500">
                              {place.weather}
                            </div>
                          </div>
                          {place.highlights && (
                            <div className="mt-3">
                              <p className="text-xs text-gray-600 mb-1">Highlights:</p>
                              <div className="flex flex-wrap gap-1">
                                {place.highlights.slice(0, 3).map((highlight, idx) => (
                                  <span key={idx} className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">
                                    {highlight}
                                  </span>
                                ))}
                              </div>
                            </div>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Weather */}
              {recommendations.weather && (
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-3">
                    Weather Information
                  </h3>
                  <div className="bg-blue-50 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-3">
                      <div>
                        <p className="text-sm text-gray-600">Current Weather</p>
                        <p className="text-2xl font-bold">{recommendations.weather.current.temperature}</p>
                        <p className="text-sm text-gray-600">{recommendations.weather.current.condition}</p>
                      </div>
                      <div className="text-right">
                        <p className="text-sm text-gray-600">Humidity</p>
                        <p className="font-medium">{recommendations.weather.current.humidity}</p>
                      </div>
                    </div>
                    {recommendations.weather.forecast && (
                      <div>
                        <p className="text-sm text-gray-600 mb-2">3-Day Forecast</p>
                        <div className="flex space-x-4">
                          {recommendations.weather.forecast.map((day, index) => (
                            <div key={index} className="text-center">
                              <p className="text-xs text-gray-600">{day.day}</p>
                              <p className="font-medium">{day.temp}</p>
                              <p className="text-xs text-gray-500">{day.condition}</p>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Holidays */}
              {recommendations.holidays && recommendations.holidays.length > 0 && (
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-3">
                    Upcoming Holidays & Events
                  </h3>
                  <div className="space-y-2">
                    {recommendations.holidays.map((holiday, index) => (
                      <div key={index} className="flex items-center justify-between bg-yellow-50 rounded-lg p-3">
                        <div>
                          <p className="font-medium text-gray-900">{holiday.name}</p>
                          <p className="text-sm text-gray-600">{holiday.description}</p>
                        </div>
                        <div className="text-sm text-gray-500">
                          {new Date(holiday.date).toLocaleDateString()}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {!isLoading && !recommendations && (
            <div className="text-center py-12 text-gray-500">
              <Sparkles className="h-12 w-12 mx-auto mb-4 text-gray-300" />
              <p>Fill out the form to get personalized recommendations</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Recommendations; 