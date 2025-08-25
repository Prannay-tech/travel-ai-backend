import axios from 'axios';

// Create axios instance with base configuration
const apiService = axios.create({
  // Temporarily use local backend while we troubleshoot Supabase
  baseURL: 'http://localhost:8000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  }
});

// Request interceptor for logging
apiService.interceptors.request.use(
  (config) => {
    console.log('API Request:', config.method?.toUpperCase(), config.url);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiService.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.status, response.config.url);
    return response;
  },
  (error) => {
    console.error('API Response Error:', error.response?.status, error.response?.data);
    return Promise.reject(error);
  }
);

// Health check endpoint
export const checkHealth = () => apiService.get('/health');

// Chat with AI endpoint
export const chatWithAI = (message, conversationHistory = []) => 
  apiService.post('/chat', { message, conversation_history: conversationHistory });

// Flight search endpoint
export const searchFlights = (searchParams) => 
  apiService.post('/flights', searchParams);

// Currency conversion endpoint
export const convertCurrency = (amount, fromCurrency, toCurrency) => 
  apiService.get(`/currency/convert?amount=${amount}&from_currency=${fromCurrency}&to_currency=${toCurrency}`);

// Weather endpoint
export const getWeather = (location) => 
  apiService.get(`/weather/${encodeURIComponent(location)}`);

// Mock data for destinations (since we don't have a real API for this yet)
export const getDestinationRecommendations = (preferences) => {
  // This would ideally call a real API, but for now we'll use mock data
  return Promise.resolve({
    data: {
      recommendations: [
        {
          id: 1,
          name: "Bali, Indonesia",
          type: "beach",
          description: "Tropical paradise with beautiful beaches and rich culture",
          image: "https://images.unsplash.com/photo-1537953773345-d172ccf13cf1?w=800",
          budget_range: { min: 800, max: 1500 },
          best_time: "April to October",
          highlights: ["Beaches", "Temples", "Rice Terraces", "Waterfalls"],
          average_temperature: "28°C",
          currency: "IDR"
        },
        {
          id: 2,
          name: "Swiss Alps",
          type: "mountain",
          description: "Breathtaking mountain scenery and world-class skiing",
          image: "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800",
          budget_range: { min: 1200, max: 2500 },
          best_time: "December to March (skiing), June to September (hiking)",
          highlights: ["Skiing", "Hiking", "Lakes", "Chocolate"],
          average_temperature: "5°C",
          currency: "CHF"
        },
        {
          id: 3,
          name: "Tokyo, Japan",
          type: "city",
          description: "Ultra-modern metropolis with rich traditions",
          image: "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=800",
          budget_range: { min: 1500, max: 3000 },
          best_time: "March to May (cherry blossoms), September to November",
          highlights: ["Technology", "Temples", "Food", "Shopping"],
          average_temperature: "15°C",
          currency: "JPY"
        },
        {
          id: 4,
          name: "Rome, Italy",
          type: "historic",
          description: "Eternal city with ancient ruins and Renaissance art",
          image: "https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=800",
          budget_range: { min: 1000, max: 2000 },
          best_time: "April to June, September to October",
          highlights: ["Colosseum", "Vatican", "Pizza", "Art"],
          average_temperature: "18°C",
          currency: "EUR"
        },
        {
          id: 5,
          name: "Santorini, Greece",
          type: "beach",
          description: "Stunning volcanic island with white-washed buildings",
          image: "https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?w=800",
          budget_range: { min: 1200, max: 2500 },
          best_time: "June to September",
          highlights: ["Sunsets", "Beaches", "Wine", "Architecture"],
          average_temperature: "24°C",
          currency: "EUR"
        }
      ]
    }
  });
};

// Mock data for hotels
export const searchHotels = (destination, checkIn, checkOut, guests) => {
  return Promise.resolve({
    data: {
      hotels: [
        {
          id: 1,
          name: "Luxury Resort & Spa",
          rating: 4.8,
          price_per_night: { USD: 250, EUR: 210, GBP: 185 },
          image: "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800",
          amenities: ["Pool", "Spa", "Restaurant", "Free WiFi"],
          location: "Beachfront",
          booking_link: "https://booking.com/hotel1"
        },
        {
          id: 2,
          name: "Boutique Hotel",
          rating: 4.5,
          price_per_night: { USD: 180, EUR: 150, GBP: 130 },
          image: "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800",
          amenities: ["Restaurant", "Bar", "Free WiFi", "Gym"],
          location: "City Center",
          booking_link: "https://booking.com/hotel2"
        }
      ]
    }
  });
};

// Mock data for activities
export const getActivities = (destination) => {
  return Promise.resolve({
    data: {
      activities: [
        {
          id: 1,
          name: "Guided City Tour",
          type: "Cultural",
          duration: "3 hours",
          price: { USD: 45, EUR: 38, GBP: 33 },
          rating: 4.7,
          image: "https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=800",
          description: "Explore the city's most famous landmarks with a local guide"
        },
        {
          id: 2,
          name: "Adventure Hiking",
          type: "Adventure",
          duration: "6 hours",
          price: { USD: 75, EUR: 63, GBP: 55 },
          rating: 4.9,
          image: "https://images.unsplash.com/photo-1551632811-561732d1e306?w=800",
          description: "Challenging hike through scenic mountain trails"
        }
      ]
    }
  });
};

export default apiService;
      