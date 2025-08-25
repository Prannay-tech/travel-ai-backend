import axios from 'axios';

// API Base URL
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
apiClient.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('API Response Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// API Service Functions
export const apiService = {
  // Health Check
  healthCheck: async () => {
    try {
      const response = await apiClient.get('/health');
      return response.data;
    } catch (error) {
      throw new Error('Backend service is not available');
    }
  },

  // AI Chat
  chatWithAI: async (message, conversationHistory = []) => {
    try {
      const response = await apiClient.post('/chat', {
        message,
        conversation_history: conversationHistory
      });
      return response.data;
    } catch (error) {
      throw new Error('Failed to communicate with AI service');
    }
  },

  // Get Travel Recommendations
  getRecommendations: async (preferences) => {
    try {
      const response = await apiClient.post('/recommendations', preferences);
      return response.data;
    } catch (error) {
      throw new Error('Failed to get travel recommendations');
    }
  },

  // Search Flights
  searchFlights: async (searchParams) => {
    try {
      const response = await apiClient.post('/flights', searchParams);
      return response.data;
    } catch (error) {
      throw new Error('Failed to search flights');
    }
  },

  // Search Hotels
  searchHotels: async (searchParams) => {
    try {
      const response = await apiClient.post('/hotels', searchParams);
      return response.data;
    } catch (error) {
      throw new Error('Failed to search hotels');
    }
  },

  // Search Activities
  searchActivities: async (searchParams) => {
    try {
      const response = await apiClient.post('/activities', searchParams);
      return response.data;
    } catch (error) {
      throw new Error('Failed to search activities');
    }
  },

  // Get All Destinations
  getAllDestinations: async () => {
    try {
      const response = await apiClient.get('/destinations');
      return response.data;
    } catch (error) {
      throw new Error('Failed to get destinations');
    }
  },

  // Currency Conversion
  convertCurrency: async (amount, fromCurrency, toCurrency) => {
    try {
      const response = await apiClient.get('/currency/convert', {
        params: {
          amount,
          from_currency: fromCurrency,
          to_currency: toCurrency
        }
      });
      return response.data;
    } catch (error) {
      throw new Error('Failed to convert currency');
    }
  }
};

// Utility Functions
export const formatPrice = (price, currency = 'USD') => {
  if (typeof price === 'object' && price[currency]) {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: currency
    }).format(price[currency]);
  }
  
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: currency
  }).format(price || 0);
};

export const formatDuration = (duration) => {
  if (!duration) return 'N/A';
  return duration;
};

export const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
};

export const getDestinationImage = (destination) => {
  return destination.image || 'https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=800';
};

export const getRatingStars = (rating) => {
  const stars = [];
  const fullStars = Math.floor(rating);
  const hasHalfStar = rating % 1 !== 0;

  for (let i = 0; i < fullStars; i++) {
    stars.push('★');
  }
  
  if (hasHalfStar) {
    stars.push('☆');
  }

  return stars.join('');
};

// Error handling utilities
export const handleApiError = (error) => {
  if (error.response) {
    // Server responded with error status
    const message = error.response.data?.detail || error.response.data?.message || 'Server error';
    return `Error: ${message}`;
  } else if (error.request) {
    // Request was made but no response received
    return 'Error: No response from server. Please check your connection.';
  } else {
    // Something else happened
    return `Error: ${error.message}`;
  }
};

export default apiService;
