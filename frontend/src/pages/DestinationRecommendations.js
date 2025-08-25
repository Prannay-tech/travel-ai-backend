import React, { useState, useEffect } from 'react';
import { Search, MapPin, Calendar, DollarSign, Home, Activity, ArrowRight, Star } from 'lucide-react';
import axios from 'axios';

const DestinationRecommendations = () => {
  const [filters, setFilters] = useState({
    type: '',
    budget: '',
    startDate: '',
    endDate: '',
    stayType: '',
    activities: ''
  });
  
  const [destinations, setDestinations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedDestination, setSelectedDestination] = useState(null);
  const [showDetails, setShowDetails] = useState(false);

  const destinationTypes = [
    { value: 'beach', label: '🏝️ Beach', icon: '🏝️' },
    { value: 'mountain', label: '⛰️ Mountain', icon: '⛰️' },
    { value: 'city', label: '🏙️ City', icon: '🏙️' },
    { value: 'countryside', label: '🌾 Countryside', icon: '🌾' },
    { value: 'island', label: '🏖️ Island', icon: '🏖️' }
  ];

  const stayTypes = [
    { value: 'hotel', label: '🏨 Hotel' },
    { value: 'airbnb', label: '🏠 Airbnb' },
    { value: 'resort', label: '🏖️ Resort' },
    { value: 'hostel', label: '🛏️ Hostel' }
  ];

  const activityOptions = [
    'outdoor', 'water_sports', 'cultural', 'food', 'adventure', 'relaxation', 'shopping', 'hiking'
  ];

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  };

  const getRecommendations = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      Object.entries(filters).forEach(([key, value]) => {
        if (value) params.append(key, value);
      });

      const response = await axios.get(`/api/recommend?${params}`);
      setDestinations(response.data);
    } catch (error) {
      console.error('Error fetching recommendations:', error);
      // Fallback to mock data
      setDestinations([
        {
          id: "bali-id",
          name: "Bali",
          country: "Indonesia",
          kind: "beach",
          cost_day_usd: 120.0,
          description: "Tropical paradise with beautiful beaches and rich culture",
          image_url: "https://images.unsplash.com/photo-1537953773345-d172ccf13cf1?w=800&h=600&fit=crop",
          total_cost_estimate: 840.0,
          similarity_score: 0.95
        },
        {
          id: "cancun-id",
          name: "Cancun",
          country: "Mexico",
          kind: "beach",
          cost_day_usd: 150.0,
          description: "Famous beach destination with crystal clear waters",
          image_url: "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800&h=600&fit=crop",
          total_cost_estimate: 1050.0,
          similarity_score: 0.92
        },
        {
          id: "oahu-id",
          name: "Oahu",
          country: "USA",
          kind: "island",
          cost_day_usd: 200.0,
          description: "Hawaiian island with stunning beaches and surf culture",
          image_url: "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&h=600&fit=crop",
          total_cost_estimate: 1400.0,
          similarity_score: 0.88
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const getDestinationDetails = async (destinationId) => {
    try {
      const response = await axios.get(`/api/details/${destinationId}`);
      setSelectedDestination(response.data);
      setShowDetails(true);
    } catch (error) {
      console.error('Error fetching destination details:', error);
    }
  };

  useEffect(() => {
    // Auto-fetch recommendations when filters change
    if (filters.type || filters.budget) {
      getRecommendations();
    }
  }, [filters.type, filters.budget]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            AI Travel Recommendations
          </h1>
          <p className="text-lg text-gray-600">
            Discover your perfect destination with AI-powered suggestions
          </p>
        </div>

        {/* Filters */}
        <div className="bg-white rounded-2xl shadow-lg p-6 mb-8">
          <h2 className="text-xl font-semibold mb-4 flex items-center">
            <Search className="w-5 h-5 mr-2" />
            Find Your Perfect Trip
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {/* Destination Type */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Destination Type
              </label>
              <select
                value={filters.type}
                onChange={(e) => handleFilterChange('type', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">Any type</option>
                {destinationTypes.map(type => (
                  <option key={type.value} value={type.value}>
                    {type.label}
                  </option>
                ))}
              </select>
            </div>

            {/* Budget */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <DollarSign className="w-4 h-4 inline mr-1" />
                Budget (USD)
              </label>
              <input
                type="number"
                placeholder="e.g., 1500"
                value={filters.budget}
                onChange={(e) => handleFilterChange('budget', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            {/* Stay Type */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <Home className="w-4 h-4 inline mr-1" />
                Stay Type
              </label>
              <select
                value={filters.stayType}
                onChange={(e) => handleFilterChange('stayType', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">Any accommodation</option>
                {stayTypes.map(type => (
                  <option key={type.value} value={type.value}>
                    {type.label}
                  </option>
                ))}
              </select>
            </div>

            {/* Start Date */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <Calendar className="w-4 h-4 inline mr-1" />
                Start Date
              </label>
              <input
                type="date"
                value={filters.startDate}
                onChange={(e) => handleFilterChange('startDate', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            {/* End Date */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <Calendar className="w-4 h-4 inline mr-1" />
                End Date
              </label>
              <input
                type="date"
                value={filters.endDate}
                onChange={(e) => handleFilterChange('endDate', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            {/* Activities */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <Activity className="w-4 h-4 inline mr-1" />
                Activities
              </label>
              <select
                value={filters.activities}
                onChange={(e) => handleFilterChange('activities', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">Any activities</option>
                {activityOptions.map(activity => (
                  <option key={activity} value={activity}>
                    {activity.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="mt-6 text-center">
            <button
              onClick={getRecommendations}
              disabled={loading}
              className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-lg font-semibold transition-colors disabled:opacity-50"
            >
              {loading ? 'Finding destinations...' : 'Get Recommendations'}
            </button>
          </div>
        </div>

        {/* Results */}
        {destinations.length > 0 && (
          <div className="space-y-6">
            <h2 className="text-2xl font-semibold text-gray-900">
              Recommended Destinations ({destinations.length})
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {destinations.map((destination) => (
                <div
                  key={destination.id}
                  className="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow cursor-pointer"
                  onClick={() => getDestinationDetails(destination.id)}
                >
                  <div className="relative h-48">
                    <img
                      src={destination.image_url}
                      alt={destination.name}
                      className="w-full h-full object-cover"
                    />
                    <div className="absolute top-3 right-3 bg-white px-2 py-1 rounded-full text-sm font-semibold text-gray-700">
                      ${destination.cost_day_usd}/day
                    </div>
                    <div className="absolute bottom-3 left-3 bg-black bg-opacity-50 text-white px-2 py-1 rounded-full text-xs">
                      {destination.kind}
                    </div>
                  </div>
                  
                  <div className="p-6">
                    <div className="flex items-start justify-between mb-2">
                      <h3 className="text-xl font-semibold text-gray-900">
                        {destination.name}
                      </h3>
                      <div className="flex items-center text-yellow-500">
                        <Star className="w-4 h-4 fill-current" />
                        <span className="ml-1 text-sm font-medium">
                          {(destination.similarity_score * 5).toFixed(1)}
                        </span>
                      </div>
                    </div>
                    
                    <p className="text-gray-600 mb-3 flex items-center">
                      <MapPin className="w-4 h-4 mr-1" />
                      {destination.country}
                    </p>
                    
                    <p className="text-gray-700 text-sm mb-4 line-clamp-2">
                      {destination.description}
                    </p>
                    
                    <div className="flex items-center justify-between">
                      <div className="text-lg font-bold text-green-600">
                        ${destination.total_cost_estimate}
                      </div>
                      <button className="flex items-center text-blue-600 hover:text-blue-700 font-semibold">
                        View Details
                        <ArrowRight className="w-4 h-4 ml-1" />
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Destination Details Modal */}
        {showDetails && selectedDestination && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
              <div className="p-6">
                <div className="flex justify-between items-start mb-6">
                  <h2 className="text-3xl font-bold text-gray-900">
                    {selectedDestination.destination.name}
                  </h2>
                  <button
                    onClick={() => setShowDetails(false)}
                    className="text-gray-500 hover:text-gray-700 text-2xl"
                  >
                    ×
                  </button>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                  {/* Destination Info */}
                  <div>
                    <img
                      src={selectedDestination.destination.image_url}
                      alt={selectedDestination.destination.name}
                      className="w-full h-64 object-cover rounded-lg mb-4"
                    />
                    <p className="text-gray-700 mb-4">
                      {selectedDestination.destination.description}
                    </p>
                    <div className="bg-blue-50 p-4 rounded-lg">
                      <h3 className="font-semibold text-blue-900 mb-2">Cost Breakdown</h3>
                      <p className="text-blue-800">
                        Daily cost: ${selectedDestination.destination.cost_day_usd}
                      </p>
                    </div>
                  </div>

                  {/* Details */}
                  <div className="space-y-6">
                    {/* Transport Options */}
                    <div>
                      <h3 className="text-xl font-semibold mb-3">Transport Options</h3>
                      <div className="space-y-2">
                        {selectedDestination.transport_options.map((transport, index) => (
                          <div key={index} className="bg-gray-50 p-3 rounded-lg">
                            <div className="flex justify-between items-center">
                              <span className="font-medium">{transport.mode}</span>
                              <span className="text-green-600 font-semibold">
                                ${transport.avg_price_usd}
                              </span>
                            </div>
                            <p className="text-sm text-gray-600">{transport.description}</p>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Accommodations */}
                    <div>
                      <h3 className="text-xl font-semibold mb-3">Accommodations</h3>
                      <div className="space-y-2">
                        {selectedDestination.accommodations.map((acc, index) => (
                          <div key={index} className="bg-gray-50 p-3 rounded-lg">
                            <div className="flex justify-between items-center">
                              <span className="font-medium">{acc.type}</span>
                              <span className="text-green-600 font-semibold">
                                ${acc.avg_price_usd}
                              </span>
                            </div>
                            <p className="text-sm text-gray-600">{acc.description}</p>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Activities */}
                    <div>
                      <h3 className="text-xl font-semibold mb-3">Activities</h3>
                      <div className="space-y-2">
                        {selectedDestination.activities.map((activity, index) => (
                          <div key={index} className="bg-gray-50 p-3 rounded-lg">
                            <div className="flex justify-between items-center">
                              <span className="font-medium">{activity.title}</span>
                              <span className="text-green-600 font-semibold">
                                ${activity.avg_price_usd}
                              </span>
                            </div>
                            <p className="text-sm text-gray-600">{activity.description}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default DestinationRecommendations; 