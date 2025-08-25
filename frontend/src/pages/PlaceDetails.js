import React from 'react';
import { useParams } from 'react-router-dom';
import { useQuery } from 'react-query';
import { MapPin, Star, Clock, DollarSign, ExternalLink, ArrowLeft } from 'lucide-react';
import { Link } from 'react-router-dom';
import axios from 'axios';

const PlaceDetails = () => {
  const { placeId } = useParams();

  const { data: place, isLoading, error } = useQuery(
    ['place', placeId],
    async () => {
      const response = await axios.get(`/places/${placeId}`);
      return response.data;
    },
    {
      retry: false,
      staleTime: 5 * 60 * 1000 // 5 minutes
    }
  );

  if (isLoading) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading place details...</p>
        </div>
      </div>
    );
  }

  if (error || !place) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="text-center py-12">
          <h2 className="text-2xl font-semibold text-gray-900 mb-4">Place Not Found</h2>
          <p className="text-gray-600 mb-6">The place you're looking for doesn't exist or has been removed.</p>
          <Link
            to="/search"
            className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Search
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      {/* Back Button */}
      <Link
        to="/search"
        className="inline-flex items-center text-blue-600 hover:text-blue-700 mb-6 transition-colors"
      >
        <ArrowLeft className="h-4 w-4 mr-2" />
        Back to Search
      </Link>

      {/* Place Header */}
      <div className="bg-white rounded-xl shadow-md overflow-hidden mb-8">
        <div className="relative h-64 md:h-80">
          {place.image ? (
            <img
              src={place.image}
              alt={place.name}
              className="w-full h-full object-cover"
            />
          ) : (
            <div className="w-full h-full bg-gray-200 flex items-center justify-center">
              <span className="text-gray-500">No image available</span>
            </div>
          )}
          <div className="absolute top-4 right-4 bg-white bg-opacity-90 rounded-full px-3 py-1 flex items-center">
            <Star className="h-4 w-4 text-yellow-500 fill-current" />
            <span className="ml-1 font-semibold">{place.rate}</span>
          </div>
        </div>

        <div className="p-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">{place.name}</h1>
          
          <div className="flex items-center gap-2 text-gray-600 mb-4">
            <MapPin className="h-5 w-5" />
            <span>{place.city}, {place.country}</span>
          </div>

          <p className="text-gray-700 text-lg leading-relaxed mb-6">
            {place.description}
          </p>

          {/* Quick Info */}
          <div className="grid md:grid-cols-3 gap-4 mb-6">
            {place.opening_hours && (
              <div className="flex items-center gap-2">
                <Clock className="h-5 w-5 text-gray-400" />
                <div>
                  <div className="text-sm font-medium text-gray-900">Opening Hours</div>
                  <div className="text-sm text-gray-600">{place.opening_hours}</div>
                </div>
              </div>
            )}
            
            {place.ticket_price && (
              <div className="flex items-center gap-2">
                <DollarSign className="h-5 w-5 text-gray-400" />
                <div>
                  <div className="text-sm font-medium text-gray-900">Ticket Price</div>
                  <div className="text-sm text-gray-600">{place.ticket_price}</div>
                </div>
              </div>
            )}
            
            {place.type && (
              <div className="flex items-center gap-2">
                <div className="w-5 h-5 bg-blue-100 rounded-full flex items-center justify-center">
                  <span className="text-xs text-blue-600 font-semibold">
                    {place.type.charAt(0).toUpperCase()}
                  </span>
                </div>
                <div>
                  <div className="text-sm font-medium text-gray-900">Type</div>
                  <div className="text-sm text-gray-600 capitalize">{place.type}</div>
                </div>
              </div>
            )}
          </div>

          {/* Categories */}
          {place.categories && (
            <div className="mb-6">
              <h3 className="text-sm font-medium text-gray-900 mb-2">Categories</h3>
              <div className="flex flex-wrap gap-2">
                {place.categories.split(',').map((category, index) => (
                  <span
                    key={index}
                    className="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full"
                  >
                    {category.trim()}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* External Link */}
          {place.url && (
            <a
              href={place.url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              <ExternalLink className="h-4 w-4 mr-2" />
              Visit Official Website
            </a>
          )}
        </div>
      </div>

      {/* Location Details */}
      <div className="bg-white rounded-xl shadow-md p-6 mb-8">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">Location Details</h2>
        
        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-3">Address</h3>
            <div className="space-y-1 text-gray-600">
              {place.street && <div>{place.house_number} {place.street}</div>}
              {place.city && <div>{place.city}</div>}
              {place.state && <div>{place.state}</div>}
              {place.postcode && <div>{place.postcode}</div>}
              {place.country && <div>{place.country}</div>}
            </div>
          </div>
          
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-3">Coordinates</h3>
            <div className="space-y-1 text-gray-600">
              <div>Latitude: {place.latitude}</div>
              <div>Longitude: {place.longitude}</div>
            </div>
          </div>
        </div>
      </div>

      {/* Nearby Places */}
      {place.nearby_places && place.nearby_places.length > 0 && (
        <div className="bg-white rounded-xl shadow-md p-6">
          <h2 className="text-2xl font-semibold text-gray-900 mb-4">Nearby Places</h2>
          
          <div className="grid md:grid-cols-2 gap-4">
            {place.nearby_places.map((nearby, index) => (
              <div key={index} className="border border-gray-200 rounded-lg p-4">
                <h3 className="font-medium text-gray-900 mb-1">{nearby.name}</h3>
                <p className="text-sm text-gray-600">{nearby.distance} away</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default PlaceDetails; 