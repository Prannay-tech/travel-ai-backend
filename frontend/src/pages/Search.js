import React, { useState } from 'react';
import { useQuery } from 'react-query';
import { Search as SearchIcon, MapPin, Star, Plane, Filter } from 'lucide-react';
import axios from 'axios';
import toast from 'react-hot-toast';

const Search = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchType, setSearchType] = useState('places');
  const [filters, setFilters] = useState({
    minRating: 0,
    maxPrice: 1000,
    directFlights: false
  });

  const searchPlaces = async () => {
    if (!searchQuery.trim()) return [];
    
    try {
      const response = await axios.post('/search/places', {
        query: searchQuery,
        limit: 20,
        min_rating: filters.minRating
      });
      return response.data;
    } catch (error) {
      toast.error('Error searching places');
      return [];
    }
  };

  const searchFlights = async () => {
    if (!searchQuery.trim()) return [];
    
    try {
      // For demo purposes, using mock data
      // In real implementation, you'd parse the query to extract origin/destination
      const response = await axios.post('/search/flights', {
        origin: 'JFK-sky',
        destination: 'LAX-sky',
        departure_date: '2024-06-15'
      });
      return response.data;
    } catch (error) {
      toast.error('Error searching flights');
      return [];
    }
  };

  const { data: searchResults, isLoading, refetch } = useQuery(
    ['search', searchQuery, searchType, filters],
    searchType === 'places' ? searchPlaces : searchFlights,
    {
      enabled: false,
      retry: false
    }
  );

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      refetch();
    }
  };

  return (
    <div className="max-w-6xl mx-auto">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Smart Travel Search
        </h1>
        <p className="text-lg text-gray-600">
          Find places and flights using natural language queries
        </p>
      </div>

      {/* Search Form */}
      <div className="bg-white rounded-xl shadow-md p-6 mb-8">
        <form onSubmit={handleSearch} className="space-y-4">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1">
              <div className="relative">
                <SearchIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder={
                    searchType === 'places' 
                      ? "e.g., 'art museums in Paris' or 'historic landmarks'"
                      : "e.g., 'flights from New York to London'"
                  }
                  className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>
            
            <div className="flex gap-2">
              <select
                value={searchType}
                onChange={(e) => setSearchType(e.target.value)}
                className="px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="places">Places</option>
                <option value="flights">Flights</option>
              </select>
              
              <button
                type="submit"
                disabled={isLoading}
                className="px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
              >
                {isLoading ? 'Searching...' : 'Search'}
              </button>
            </div>
          </div>

          {/* Filters */}
          <div className="border-t pt-4">
            <div className="flex items-center gap-4 flex-wrap">
              <span className="text-sm font-medium text-gray-700">Filters:</span>
              
              {searchType === 'places' && (
                <div className="flex items-center gap-2">
                  <label className="text-sm text-gray-600">Min Rating:</label>
                  <select
                    value={filters.minRating}
                    onChange={(e) => setFilters({...filters, minRating: parseFloat(e.target.value)})}
                    className="px-2 py-1 border border-gray-300 rounded text-sm"
                  >
                    <option value={0}>Any</option>
                    <option value={5}>5+</option>
                    <option value={6}>6+</option>
                    <option value={7}>7+</option>
                    <option value={8}>8+</option>
                    <option value={9}>9+</option>
                  </select>
                </div>
              )}
              
              {searchType === 'flights' && (
                <div className="flex items-center gap-2">
                  <label className="text-sm text-gray-600">Max Price:</label>
                  <input
                    type="number"
                    value={filters.maxPrice}
                    onChange={(e) => setFilters({...filters, maxPrice: parseInt(e.target.value)})}
                    className="px-2 py-1 border border-gray-300 rounded text-sm w-20"
                  />
                </div>
              )}
            </div>
          </div>
        </form>
      </div>

      {/* Search Results */}
      {isLoading && (
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Searching...</p>
        </div>
      )}

      {searchResults && searchResults.length > 0 && (
        <div className="space-y-6">
          <h2 className="text-2xl font-semibold text-gray-900">
            Search Results ({searchResults.length})
          </h2>
          
          <div className="grid gap-6">
            {searchType === 'places' ? (
              searchResults.map((place) => (
                <PlaceCard key={place.place_id} place={place} />
              ))
            ) : (
              searchResults.map((flight) => (
                <FlightCard key={flight.quote_id} flight={flight} />
              ))
            )}
          </div>
        </div>
      )}

      {searchResults && searchResults.length === 0 && !isLoading && (
        <div className="text-center py-12">
          <SearchIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No results found</h3>
          <p className="text-gray-600">Try adjusting your search query or filters.</p>
        </div>
      )}
    </div>
  );
};

const PlaceCard = ({ place }) => (
  <div className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-lg transition-shadow">
    <div className="p-6">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-2">
            <h3 className="text-xl font-semibold text-gray-900">{place.name}</h3>
            <div className="flex items-center gap-1">
              <Star className="h-4 w-4 text-yellow-500 fill-current" />
              <span className="text-sm font-medium">{place.rate}</span>
            </div>
          </div>
          
          <div className="flex items-center gap-2 text-sm text-gray-600 mb-2">
            <MapPin className="h-4 w-4" />
            <span>{place.city}, {place.country}</span>
          </div>
          
          <p className="text-gray-700 mb-3">{place.description}</p>
          
          <div className="flex flex-wrap gap-2">
            {place.categories.split(',').slice(0, 3).map((category, index) => (
              <span
                key={index}
                className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full"
              >
                {category.trim()}
              </span>
            ))}
          </div>
        </div>
        
        {place.image && (
          <div className="ml-4">
            <img
              src={place.image}
              alt={place.name}
              className="w-24 h-24 object-cover rounded-lg"
            />
          </div>
        )}
      </div>
    </div>
  </div>
);

const FlightCard = ({ flight }) => (
  <div className="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-shadow">
    <div className="flex items-center justify-between">
      <div className="flex-1">
        <div className="flex items-center gap-4 mb-2">
          <h3 className="text-lg font-semibold text-gray-900">
            {flight.origin_id} → {flight.destination_id}
          </h3>
          <span className={`px-2 py-1 text-xs rounded-full ${
            flight.direct ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
          }`}>
            {flight.direct ? 'Direct' : `${flight.stops} stop${flight.stops !== 1 ? 's' : ''}`}
          </span>
        </div>
        
        <div className="flex items-center gap-4 text-sm text-gray-600">
          <span>Date: {flight.departure_date}</span>
          <span>Price: {flight.currency} {flight.min_price}</span>
        </div>
      </div>
      
      <div className="text-right">
        <div className="text-2xl font-bold text-blue-600">
          {flight.currency} {flight.min_price}
        </div>
        <button className="mt-2 px-4 py-2 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700 transition-colors">
          Book Now
        </button>
      </div>
    </div>
  </div>
);

export default Search; 