import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { MapPin, Clock, Users, ArrowRight, CheckCircle } from 'lucide-react';
import axios from 'axios';

const ActivityPlanning = ({ selectedDestination, travelData }) => {
  const navigate = useNavigate();
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedActivities, setSelectedActivities] = useState([]);

  useEffect(() => {
    if (selectedDestination) {
      searchActivities();
    }
  }, [selectedDestination]);

  const searchActivities = async () => {
    if (!selectedDestination) return;

    setLoading(true);
    try {
      const response = await axios.post('/activities', {
        destination: selectedDestination.name,
        dates: '2024-12-01 to 2024-12-08',
        interests: selectedDestination.activities || []
      });

      if (response.data.success) {
        setActivities(response.data.activities);
      }
    } catch (error) {
      console.error('Error searching activities:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleActivityToggle = (activity) => {
    setSelectedActivities(prev => {
      const isSelected = prev.find(a => a.name === activity.name);
      if (isSelected) {
        return prev.filter(a => a.name !== activity.name);
      } else {
        return [...prev, activity];
      }
    });
  };

  const calculateTotalCost = () => {
    return selectedActivities.reduce((total, activity) => total + activity.price, 0);
  };

  const finishPlanning = () => {
    // Here you would typically save the complete trip plan
    alert('🎉 Your trip is planned! Check your email for the complete itinerary.');
    navigate('/');
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
          Activities in {selectedDestination.name}
        </h1>
        <p className="text-gray-600">
          Plan your perfect itinerary with exciting activities and experiences
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
            <p className="text-sm text-gray-600">Available Activities</p>
            <p className="text-2xl font-bold text-purple-600">
              {selectedDestination.activities?.length || 0}
            </p>
          </div>
        </div>
      </div>

      <div className="grid lg:grid-cols-3 gap-8">
        {/* Activities List */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-lg shadow-lg overflow-hidden">
            <div className="p-6 border-b">
              <h2 className="text-xl font-semibold text-gray-900">Available Activities</h2>
              <p className="text-gray-600">Select activities to add to your itinerary</p>
            </div>

            {loading ? (
              <div className="p-8 text-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
                <p className="text-gray-600">Loading activities...</p>
              </div>
            ) : activities.length > 0 ? (
              <div className="divide-y">
                {activities.map((activity, index) => {
                  const isSelected = selectedActivities.find(a => a.name === activity.name);
                  
                  return (
                    <div
                      key={index}
                      className={`p-6 cursor-pointer transition-colors ${
                        isSelected ? 'bg-primary-50 border-l-4 border-primary-600' : 'hover:bg-gray-50'
                      }`}
                      onClick={() => handleActivityToggle(activity)}
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-4">
                          <div className="flex-shrink-0">
                            {isSelected ? (
                              <CheckCircle className="h-6 w-6 text-primary-600" />
                            ) : (
                              <div className="w-6 h-6 border-2 border-gray-300 rounded-full"></div>
                            )}
                          </div>
                          
                          <div className="flex-1">
                            <h3 className="text-lg font-semibold text-gray-900">{activity.name}</h3>
                            <p className="text-gray-600 text-sm mb-2">{activity.description}</p>
                            
                            <div className="flex items-center space-x-4 text-sm text-gray-500">
                              <div className="flex items-center space-x-1">
                                <Clock className="h-4 w-4" />
                                <span>{activity.duration}</span>
                              </div>
                              <div className="flex items-center space-x-1">
                                <MapPin className="h-4 w-4" />
                                <span>{selectedDestination.name}</span>
                              </div>
                            </div>
                          </div>
                        </div>

                        <div className="text-right">
                          <p className="text-xl font-bold text-green-600">
                            {activity.currency} {activity.price}
                          </p>
                          <p className="text-sm text-gray-600">per person</p>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            ) : (
              <div className="p-8 text-center">
                <MapPin className="h-12 w-12 text-gray-300 mx-auto mb-4" />
                <p className="text-gray-600">No activities found for this destination.</p>
              </div>
            )}
          </div>
        </div>

        {/* Itinerary Summary */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg shadow-lg p-6 sticky top-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Your Itinerary</h2>
            
            {selectedActivities.length === 0 ? (
              <p className="text-gray-600 text-center py-8">
                Select activities to build your itinerary
              </p>
            ) : (
              <>
                <div className="space-y-3 mb-6">
                  {selectedActivities.map((activity, index) => (
                    <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                      <div className="flex-1">
                        <p className="font-medium text-gray-900">{activity.name}</p>
                        <p className="text-sm text-gray-600">{activity.duration}</p>
                      </div>
                      <p className="font-semibold text-green-600">
                        {activity.currency} {activity.price}
                      </p>
                    </div>
                  ))}
                </div>

                <div className="border-t pt-4">
                  <div className="flex justify-between items-center mb-4">
                    <span className="font-semibold text-gray-900">Total Cost:</span>
                    <span className="text-xl font-bold text-green-600">
                      USD {calculateTotalCost()}
                    </span>
                  </div>
                  
                  <button
                    onClick={finishPlanning}
                    className="w-full bg-primary-600 text-white py-3 rounded-lg hover:bg-primary-700 transition-colors flex items-center justify-center space-x-2"
                  >
                    <span>Complete Trip Planning</span>
                    <ArrowRight className="h-4 w-4" />
                  </button>
                </div>
              </>
            )}
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="mt-8 flex justify-between items-center">
        <button
          onClick={() => navigate('/hotels')}
          className="bg-gray-600 text-white px-6 py-3 rounded-lg hover:bg-gray-700 transition-colors"
        >
          Back to Hotels
        </button>
        
        <div className="text-right">
          <p className="text-sm text-gray-600 mb-2">
            Selected {selectedActivities.length} activities
          </p>
          <p className="text-lg font-semibold text-green-600">
            Total: USD {calculateTotalCost()}
          </p>
        </div>
      </div>

      {/* Trip Summary */}
      {selectedActivities.length > 0 && (
        <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
          <h3 className="font-semibold text-blue-800 mb-2">Your Complete Trip:</h3>
          <div className="grid md:grid-cols-3 gap-4 text-sm text-blue-700">
            <div>
              <strong>Destination:</strong> {selectedDestination.name}
            </div>
            <div>
              <strong>Activities:</strong> {selectedActivities.length} selected
            </div>
            <div>
              <strong>Total Cost:</strong> USD {calculateTotalCost()}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ActivityPlanning;
