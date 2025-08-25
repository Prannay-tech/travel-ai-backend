// Mock recommendation system for frontend development
// This will be replaced with actual API calls when backend is connected

// Import the real-world data function
import { generateRealWorldRecommendations } from './realWorldData';

const beachDestinations = [
  {
    name: "Bali, Indonesia",
    country: "Indonesia",
    description: "Tropical paradise with stunning beaches, rich culture, and affordable luxury",
    image: "https://images.unsplash.com/photo-1537953773345-d172ccf13cf1?w=400",
    rating: 9.2,
    cost_day_usd: 80,
    weather: "Tropical, 25-32°C year-round",
    highlights: ["Beach resorts", "Cultural temples", "Rice terraces", "Water sports"],
    best_time: "April to October"
  },
  {
    name: "Maldives",
    country: "Maldives",
    description: "Ultimate luxury beach destination with overwater bungalows",
    image: "https://images.unsplash.com/photo-1514282401047-d79a71a590e8?w=400",
    rating: 9.5,
    cost_day_usd: 300,
    weather: "Tropical, 25-30°C year-round",
    highlights: ["Overwater bungalows", "Crystal clear waters", "Snorkeling", "Luxury resorts"],
    best_time: "November to April"
  },
  {
    name: "Thailand Islands",
    country: "Thailand",
    description: "Beautiful islands with white sand beaches and vibrant culture",
    image: "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=400",
    rating: 8.8,
    cost_day_usd: 60,
    weather: "Tropical, 25-35°C",
    highlights: ["Phi Phi Islands", "Full Moon Party", "Thai cuisine", "Island hopping"],
    best_time: "November to April"
  },
  {
    name: "Hawaii, USA",
    country: "USA",
    description: "Pacific paradise with diverse landscapes and rich culture",
    image: "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400",
    rating: 9.0,
    cost_day_usd: 200,
    weather: "Tropical, 20-30°C year-round",
    highlights: ["Volcanoes", "Surfing", "Hula culture", "Island diversity"],
    best_time: "April to October"
  }
];

const mountainDestinations = [
  {
    name: "Swiss Alps",
    country: "Switzerland",
    description: "Majestic mountains with world-class skiing and hiking",
    image: "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400",
    rating: 9.3,
    cost_day_usd: 250,
    weather: "Alpine, varies by season",
    highlights: ["Skiing", "Hiking", "Chocolate", "Scenic trains"],
    best_time: "December to March (skiing), June to September (hiking)"
  },
  {
    name: "Banff National Park",
    country: "Canada",
    description: "Stunning Canadian Rockies with pristine wilderness",
    image: "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400",
    rating: 9.1,
    cost_day_usd: 150,
    weather: "Mountain, varies by season",
    highlights: ["Lake Louise", "Wildlife", "Hiking", "Hot springs"],
    best_time: "June to September"
  },
  {
    name: "Nepal Himalayas",
    country: "Nepal",
    description: "Adventure paradise with the world's highest peaks",
    image: "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400",
    rating: 8.9,
    cost_day_usd: 40,
    weather: "Mountain, varies by altitude",
    highlights: ["Everest Base Camp", "Trekking", "Buddhist culture", "Adventure sports"],
    best_time: "March to May, September to November"
  }
];

const cityDestinations = [
  {
    name: "Tokyo, Japan",
    country: "Japan",
    description: "Futuristic metropolis blending tradition with innovation",
    image: "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=400",
    rating: 9.0,
    cost_day_usd: 180,
    weather: "Temperate, 10-30°C",
    highlights: ["Technology", "Sushi", "Cherry blossoms", "Efficient transport"],
    best_time: "March to May, October to November"
  },
  {
    name: "Paris, France",
    country: "France",
    description: "City of love with iconic landmarks and world-class cuisine",
    image: "https://images.unsplash.com/photo-1502602898536-47ad22581b52?w=400",
    rating: 8.8,
    cost_day_usd: 220,
    weather: "Temperate, 5-25°C",
    highlights: ["Eiffel Tower", "Louvre", "French cuisine", "Fashion"],
    best_time: "April to June, September to October"
  },
  {
    name: "New York City",
    country: "USA",
    description: "The city that never sleeps with endless entertainment",
    image: "https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?w=400",
    rating: 8.5,
    cost_day_usd: 300,
    weather: "Temperate, -5 to 30°C",
    highlights: ["Broadway", "Central Park", "Museums", "Diverse food"],
    best_time: "April to June, September to November"
  }
];

const adventureDestinations = [
  {
    name: "New Zealand",
    country: "New Zealand",
    description: "Adventure capital with stunning landscapes and outdoor activities",
    image: "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400",
    rating: 9.2,
    cost_day_usd: 120,
    weather: "Temperate, 10-25°C",
    highlights: ["Bungee jumping", "Lord of the Rings", "Hiking", "Maori culture"],
    best_time: "December to February (summer)"
  },
  {
    name: "Costa Rica",
    country: "Costa Rica",
    description: "Eco-adventure paradise with rainforests and beaches",
    image: "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400",
    rating: 8.7,
    cost_day_usd: 80,
    weather: "Tropical, 20-30°C",
    highlights: ["Zip lining", "Wildlife", "Beaches", "Eco-tourism"],
    best_time: "December to April"
  }
];

const relaxingDestinations = [
  {
    name: "Santorini, Greece",
    country: "Greece",
    description: "Stunning sunsets and white-washed buildings overlooking the Aegean",
    image: "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400",
    rating: 9.1,
    cost_day_usd: 150,
    weather: "Mediterranean, 15-30°C",
    highlights: ["Sunset views", "Wine tasting", "Hot springs", "Greek cuisine"],
    best_time: "May to October"
  },
  {
    name: "Tuscany, Italy",
    country: "Italy",
    description: "Rolling hills, vineyards, and charming medieval towns",
    image: "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400",
    rating: 8.9,
    cost_day_usd: 120,
    weather: "Mediterranean, 10-30°C",
    highlights: ["Wine tours", "Art history", "Countryside", "Italian food"],
    best_time: "April to October"
  }
];

export const generateRecommendations = (travelData) => {
  // Use the new real-world data system
  return generateRealWorldRecommendations(travelData);
};

const parseBudget = (budget) => {
  if (!budget) return null;
  
  // Extract numbers from budget string
  const numbers = budget.match(/\d+/g);
  if (numbers) {
    return parseInt(numbers[0]) * 1000; // Assume first number is in thousands
  }
  return null;
};

const getBestTimeToVisit = (destination) => {
  if (destination.toLowerCase().includes('beach')) {
    return "April to October for best weather";
  } else if (destination.toLowerCase().includes('mountain')) {
    return "June to September for hiking, December to March for skiing";
  } else if (destination.toLowerCase().includes('city')) {
    return "Spring (March to May) or Fall (September to November)";
  }
  return "Year-round, but check specific destination for best times";
};

const generateTravelTips = (destination, budget, preferences) => {
  const tips = [];
  
  if (destination.toLowerCase().includes('beach')) {
    tips.push("Pack sunscreen and beach essentials");
    tips.push("Book accommodations early during peak season");
  }
  
  if (budget && budget.toLowerCase().includes('budget')) {
    tips.push("Consider staying in hostels or budget accommodations");
    tips.push("Eat at local restaurants for authentic and affordable meals");
  }
  
  if (preferences && preferences.toLowerCase().includes('family')) {
    tips.push("Look for family-friendly activities and accommodations");
    tips.push("Plan activities suitable for all ages");
  }
  
  return tips;
}; 