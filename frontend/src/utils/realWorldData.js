// Enhanced AI Travel Recommendation System
// This system provides intelligent destination matching based on user preferences

// Comprehensive destination database
const destinationDatabase = {
  beach: [
    // Domestic Beach Destinations
    {
      name: "Miami Beach, Florida",
      country: "USA",
      state: "FL",
      type: "beach",
      description: "Famous for its Art Deco architecture, white sand beaches, and vibrant nightlife",
      image: "https://images.unsplash.com/photo-1514214246283-d427a95c5d2f?w=400",
      rating: 8.7,
      cost_day_usd: 180,
      weather: "Tropical, 20-32°C year-round",
      highlights: ["South Beach", "Art Deco District", "Cuban cuisine", "Water sports"],
      best_time: "March to May, October to December",
      airport: "MIA",
      avg_flight_cost: 250,
      activities: ["swimming", "nightlife", "cultural", "food"],
      family_friendly: true,
      romantic: true,
      budget_friendly: false
    },
    {
      name: "San Diego, California",
      country: "USA",
      state: "CA",
      type: "beach",
      description: "Perfect weather year-round with beautiful beaches and laid-back vibe",
      image: "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400",
      rating: 8.9,
      cost_day_usd: 200,
      weather: "Mediterranean, 15-25°C year-round",
      highlights: ["La Jolla", "Gaslamp Quarter", "Zoo", "Craft beer"],
      best_time: "March to November",
      airport: "SAN",
      avg_flight_cost: 300,
      activities: ["swimming", "surfing", "family", "food", "cultural"],
      family_friendly: true,
      romantic: true,
      budget_friendly: false
    },
    {
      name: "Myrtle Beach, South Carolina",
      country: "USA",
      state: "SC",
      type: "beach",
      description: "Family-friendly beach destination with golf courses and entertainment",
      image: "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400",
      rating: 7.8,
      cost_day_usd: 120,
      weather: "Subtropical, 10-30°C",
      highlights: ["Broadway at the Beach", "Golf courses", "Family attractions", "Seafood"],
      best_time: "April to October",
      airport: "MYR",
      avg_flight_cost: 200,
      activities: ["swimming", "golf", "family", "entertainment"],
      family_friendly: true,
      romantic: false,
      budget_friendly: true
    },
    // International Beach Destinations
    {
      name: "Bali, Indonesia",
      country: "Indonesia",
      type: "beach",
      description: "Tropical paradise with stunning beaches, rich culture, and affordable luxury",
      image: "https://images.unsplash.com/photo-1537953773345-d172ccf13cf1?w=400",
      rating: 9.2,
      cost_day_usd: 80,
      weather: "Tropical, 25-32°C year-round",
      highlights: ["Beach resorts", "Cultural temples", "Rice terraces", "Water sports"],
      best_time: "April to October",
      airport: "DPS",
      avg_flight_cost: 1200,
      activities: ["swimming", "cultural", "spa", "adventure", "food"],
      family_friendly: true,
      romantic: true,
      budget_friendly: true
    },
    {
      name: "Maldives",
      country: "Maldives",
      type: "beach",
      description: "Ultimate luxury beach destination with overwater bungalows",
      image: "https://images.unsplash.com/photo-1514282401047-d79a71a590e8?w=400",
      rating: 9.5,
      cost_day_usd: 300,
      weather: "Tropical, 25-30°C year-round",
      highlights: ["Overwater bungalows", "Crystal clear waters", "Snorkeling", "Luxury resorts"],
      best_time: "November to April",
      airport: "MLE",
      avg_flight_cost: 1500,
      activities: ["swimming", "snorkeling", "luxury", "romance"],
      family_friendly: false,
      romantic: true,
      budget_friendly: false
    },
    {
      name: "Phuket, Thailand",
      country: "Thailand",
      type: "beach",
      description: "Tropical island with beautiful beaches, vibrant culture, and great food",
      image: "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400",
      rating: 8.8,
      cost_day_usd: 90,
      weather: "Tropical, 25-32°C year-round",
      highlights: ["Patong Beach", "Phi Phi Islands", "Thai cuisine", "Night markets"],
      best_time: "November to April",
      airport: "HKT",
      avg_flight_cost: 1000,
      activities: ["swimming", "island_hopping", "food", "nightlife"],
      family_friendly: true,
      romantic: true,
      budget_friendly: true
    }
  ],
  mountain: [
    // Domestic Mountain Destinations
    {
      name: "Denver, Colorado",
      country: "USA",
      state: "CO",
      type: "mountain",
      description: "Gateway to the Rockies with outdoor adventures and craft beer scene",
      image: "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400",
      rating: 8.5,
      cost_day_usd: 150,
      weather: "Mountain, -5 to 30°C",
      highlights: ["Rocky Mountains", "Craft breweries", "Skiing", "Hiking"],
      best_time: "June to September, December to March",
      airport: "DEN",
      avg_flight_cost: 280,
      activities: ["hiking", "skiing", "breweries", "outdoor"],
      family_friendly: true,
      romantic: true,
      budget_friendly: true
    },
    {
      name: "Asheville, North Carolina",
      country: "USA",
      state: "NC",
      type: "mountain",
      description: "Artsy mountain town with craft beer and outdoor activities",
      image: "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400",
      rating: 8.3,
      cost_day_usd: 130,
      weather: "Mountain, 5-25°C",
      highlights: ["Blue Ridge Parkway", "Biltmore Estate", "Craft beer", "Art galleries"],
      best_time: "March to November",
      airport: "AVL",
      avg_flight_cost: 220,
      activities: ["hiking", "cultural", "food", "art"],
      family_friendly: true,
      romantic: true,
      budget_friendly: true
    },
    // International Mountain Destinations
    {
      name: "Swiss Alps",
      country: "Switzerland",
      type: "mountain",
      description: "Majestic mountains with world-class skiing and hiking",
      image: "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400",
      rating: 9.3,
      cost_day_usd: 250,
      weather: "Alpine, varies by season",
      highlights: ["Skiing", "Hiking", "Chocolate", "Scenic trains"],
      best_time: "December to March (skiing), June to September (hiking)",
      airport: "ZRH/GVA",
      avg_flight_cost: 1000,
      activities: ["skiing", "hiking", "cultural", "luxury"],
      family_friendly: true,
      romantic: true,
      budget_friendly: false
    },
    {
      name: "Banff National Park",
      country: "Canada",
      type: "mountain",
      description: "Stunning Canadian Rockies with pristine wilderness",
      image: "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400",
      rating: 9.1,
      cost_day_usd: 150,
      weather: "Mountain, varies by season",
      highlights: ["Lake Louise", "Wildlife", "Hiking", "Hot springs"],
      best_time: "June to September",
      airport: "YYC",
      avg_flight_cost: 400,
      activities: ["hiking", "wildlife", "nature", "photography"],
      family_friendly: true,
      romantic: true,
      budget_friendly: true
    }
  ],
  city: [
    // Domestic City Destinations
    {
      name: "New York City",
      country: "USA",
      state: "NY",
      type: "city",
      description: "The city that never sleeps with endless entertainment and culture",
      image: "https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?w=400",
      rating: 8.5,
      cost_day_usd: 300,
      weather: "Temperate, -5 to 30°C",
      highlights: ["Times Square", "Central Park", "Broadway", "Museums"],
      best_time: "April to June, September to November",
      airport: "JFK/LGA",
      avg_flight_cost: 350,
      activities: ["cultural", "shopping", "food", "entertainment"],
      family_friendly: true,
      romantic: true,
      budget_friendly: false
    },
    {
      name: "Chicago, Illinois",
      country: "USA",
      state: "IL",
      type: "city",
      description: "Windy City with amazing architecture, food, and lakefront",
      image: "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400",
      rating: 8.2,
      cost_day_usd: 220,
      weather: "Continental, -10 to 30°C",
      highlights: ["Millennium Park", "Deep dish pizza", "Architecture", "Lake Michigan"],
      best_time: "May to October",
      airport: "ORD/MDW",
      avg_flight_cost: 280,
      activities: ["cultural", "food", "architecture", "shopping"],
      family_friendly: true,
      romantic: true,
      budget_friendly: true
    },
    // International City Destinations
    {
      name: "Tokyo, Japan",
      country: "Japan",
      type: "city",
      description: "Futuristic metropolis blending tradition with innovation",
      image: "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=400",
      rating: 9.0,
      cost_day_usd: 180,
      weather: "Temperate, 10-30°C",
      highlights: ["Technology", "Sushi", "Cherry blossoms", "Efficient transport"],
      best_time: "March to May, October to November",
      airport: "NRT/HND",
      avg_flight_cost: 1200,
      activities: ["cultural", "food", "technology", "shopping"],
      family_friendly: true,
      romantic: true,
      budget_friendly: false
    },
    {
      name: "Paris, France",
      country: "France",
      type: "city",
      description: "City of love with iconic landmarks and world-class cuisine",
      image: "https://images.unsplash.com/photo-1502602898536-47ad22581b52?w=400",
      rating: 8.8,
      cost_day_usd: 220,
      weather: "Temperate, 5-25°C",
      highlights: ["Eiffel Tower", "Louvre", "French cuisine", "Fashion"],
      best_time: "April to June, September to October",
      airport: "CDG/ORY",
      avg_flight_cost: 900,
      activities: ["cultural", "food", "romance", "shopping"],
      family_friendly: true,
      romantic: true,
      budget_friendly: false
    }
  ]
};

// Currency conversion rates
const currencyRates = {
  USD: 1.0,
  EUR: 0.85,
  GBP: 0.73,
  JPY: 110.0,
  CAD: 1.25,
  AUD: 1.35,
  CHF: 0.88,
  SGD: 1.35
};

// Enhanced destination matching logic
const matchDestinationType = (userInput) => {
  const input = userInput.toLowerCase();
  
  // Beach destinations
  if (input.includes('beach') || input.includes('ocean') || input.includes('sea') || 
      input.includes('coast') || input.includes('island') || input.includes('tropical')) {
    return 'beach';
  }
  
  // Mountain destinations
  if (input.includes('mountain') || input.includes('ski') || input.includes('hike') || 
      input.includes('alpine') || input.includes('rocky') || input.includes('peaks')) {
    return 'mountain';
  }
  
  // City destinations
  if (input.includes('city') || input.includes('urban') || input.includes('metropolitan') || 
      input.includes('downtown') || input.includes('culture') || input.includes('museum')) {
    return 'city';
  }
  
  // Default to beach if no clear preference
  return 'beach';
};

// Enhanced budget parsing
const parseBudget = (budget, currency) => {
  if (!budget) return null;
  
  const input = budget.toLowerCase();
  
  // Extract numbers from budget string
  const numbers = budget.match(/\d+/g);
  if (!numbers) return null;
  
  let amount = parseInt(numbers[0]);
  
  // Handle different budget formats
  if (input.includes('k') || input.includes('thousand')) {
    amount *= 1000;
  } else if (input.includes('million') || input.includes('mil')) {
    amount *= 1000000;
  }
  
  // Handle ranges (e.g., $1000-2000)
  if (numbers.length > 1) {
    amount = (amount + parseInt(numbers[1])) / 2; // Use average
  }
  
  // Convert to USD for comparison
  return amount / currencyRates[currency];
};

// Enhanced preference matching
const matchPreferences = (destination, preferences) => {
  if (!preferences) return 1.0;
  
  const pref = preferences.toLowerCase();
  let score = 1.0;
  
  // Family-friendly preference
  if (pref.includes('family') && destination.family_friendly) {
    score += 0.3;
  } else if (pref.includes('family') && !destination.family_friendly) {
    score -= 0.2;
  }
  
  // Romantic preference
  if (pref.includes('romantic') && destination.romantic) {
    score += 0.3;
  } else if (pref.includes('romantic') && !destination.romantic) {
    score -= 0.2;
  }
  
  // Budget preference
  if (pref.includes('budget') && destination.budget_friendly) {
    score += 0.3;
  } else if (pref.includes('budget') && !destination.budget_friendly) {
    score -= 0.2;
  }
  
  // Solo travel
  if (pref.includes('solo')) {
    score += 0.1; // Most destinations are good for solo travel
  }
  
  // Food preference
  if (pref.includes('food') && destination.activities.includes('food')) {
    score += 0.2;
  }
  
  // Culture preference
  if (pref.includes('culture') && destination.activities.includes('cultural')) {
    score += 0.2;
  }
  
  return Math.max(0.1, score); // Minimum score of 0.1
};

// Enhanced recommendation algorithm
export const generateRealWorldRecommendations = (travelData) => {
  const { destination, budget, travelDates, currentLocation, preferences, currency, travelType } = travelData;
  
  // Parse budget and convert to USD
  const budgetUSD = parseBudget(budget, currency);
  
  // Determine destination type
  const destinationType = matchDestinationType(destination);
  
  // Get all destinations of the matched type
  let allDestinations = destinationDatabase[destinationType] || [];
  
  // Filter by travel type (domestic vs international)
  if (travelType === 'domestic') {
    allDestinations = allDestinations.filter(dest => dest.country === 'USA');
  } else if (travelType === 'international') {
    allDestinations = allDestinations.filter(dest => dest.country !== 'USA');
  }
  
  // If no destinations found, get a mix
  if (allDestinations.length === 0) {
    allDestinations = Object.values(destinationDatabase).flat();
    if (travelType === 'domestic') {
      allDestinations = allDestinations.filter(dest => dest.country === 'USA');
    } else if (travelType === 'international') {
      allDestinations = allDestinations.filter(dest => dest.country !== 'USA');
    }
  }
  
  // Score and rank destinations
  const scoredDestinations = allDestinations.map(dest => {
    let score = dest.rating;
    
    // Budget scoring
    if (budgetUSD) {
      const totalCost = dest.cost_day_usd * 7 + dest.avg_flight_cost;
      if (totalCost <= budgetUSD) {
        score += 0.5; // Bonus for fitting budget
      } else if (totalCost <= budgetUSD * 1.5) {
        score += 0.2; // Small bonus for close to budget
      } else {
        score -= 0.3; // Penalty for over budget
      }
    }
    
    // Preference scoring
    score *= matchPreferences(dest, preferences);
    
    return { ...dest, score };
  });
  
  // Sort by score and take top 6
  const selectedDestinations = scoredDestinations
    .sort((a, b) => b.score - a.score)
    .slice(0, 6)
    .map(dest => ({
      ...dest,
      cost_day_converted: convertCurrency(dest.cost_day_usd, currency),
      flight_cost_converted: convertCurrency(dest.avg_flight_cost, currency),
      currency: currency
    }));
  
  // Get weather data for first destination
  const weatherInfo = selectedDestinations.length > 0 
    ? getWeatherData(selectedDestinations[0].name)
    : getDefaultWeather();
  
  // Get holiday data for first destination
  const holidays = selectedDestinations.length > 0 
    ? getHolidayData(selectedDestinations[0].country || selectedDestinations[0].state)
    : getDefaultHolidays();
  
  return {
    places: selectedDestinations,
    weather: weatherInfo,
    holidays: holidays,
    summary: {
      totalDestinations: selectedDestinations.length,
      averageCost: selectedDestinations.length > 0 
        ? selectedDestinations.reduce((sum, dest) => sum + dest.cost_day_converted, 0) / selectedDestinations.length 
        : 0,
      averageFlightCost: selectedDestinations.length > 0 
        ? selectedDestinations.reduce((sum, dest) => sum + dest.flight_cost_converted, 0) / selectedDestinations.length 
        : 0,
      bestTimeToVisit: getBestTimeToVisit(destinationType, travelType),
      travelTips: generateTravelTips(destination, budget, preferences, travelType),
      currency: currency,
      travelType: travelType,
      matchedType: destinationType
    }
  };
};

// Helper functions
const getWeatherData = (destination) => {
  const weatherData = {
    "Miami Beach, Florida": {
      current: { temperature: "28°C", condition: "Sunny", humidity: "75%" },
      forecast: [
        { day: "Today", temp: "28°C", condition: "Sunny" },
        { day: "Tomorrow", temp: "29°C", condition: "Partly Cloudy" },
        { day: "Day 3", temp: "27°C", condition: "Light Rain" }
      ]
    },
    "Bali, Indonesia": {
      current: { temperature: "30°C", condition: "Sunny", humidity: "80%" },
      forecast: [
        { day: "Today", temp: "30°C", condition: "Sunny" },
        { day: "Tomorrow", temp: "31°C", condition: "Partly Cloudy" },
        { day: "Day 3", temp: "29°C", condition: "Light Rain" }
      ]
    },
    "Tokyo, Japan": {
      current: { temperature: "22°C", condition: "Clear", humidity: "65%" },
      forecast: [
        { day: "Today", temp: "22°C", condition: "Clear" },
        { day: "Tomorrow", temp: "24°C", condition: "Sunny" },
        { day: "Day 3", temp: "20°C", condition: "Cloudy" }
      ]
    }
  };
  
  return weatherData[destination] || getDefaultWeather();
};

const getDefaultWeather = () => ({
  current: { temperature: "22°C", condition: "Sunny", humidity: "65%" },
  forecast: [
    { day: "Today", temp: "22°C", condition: "Sunny" },
    { day: "Tomorrow", temp: "24°C", condition: "Partly Cloudy" },
    { day: "Day 3", temp: "21°C", condition: "Light Rain" }
  ]
});

const getHolidayData = (country) => {
  const holidayData = {
    "USA": [
      { name: "Independence Day", date: "2024-07-04", description: "National holiday with fireworks" },
      { name: "Labor Day", date: "2024-09-02", description: "End of summer celebration" }
    ],
    "Indonesia": [
      { name: "Independence Day", date: "2024-08-17", description: "National independence celebration" },
      { name: "Nyepi", date: "2024-03-11", description: "Balinese day of silence" }
    ],
    "Japan": [
      { name: "Golden Week", date: "2024-04-29", description: "Series of national holidays" },
      { name: "Obon", date: "2024-08-13", description: "Buddhist festival honoring ancestors" }
    ]
  };
  
  return holidayData[country] || getDefaultHolidays();
};

const getDefaultHolidays = () => [
  { name: "Local Festival", date: "2024-08-15", description: "Annual cultural celebration" }
];

const convertCurrency = (usdAmount, targetCurrency) => {
  return Math.round(usdAmount * currencyRates[targetCurrency]);
};

const getBestTimeToVisit = (destinationType, travelType) => {
  const timeRecommendations = {
    beach: "March to October for best beach weather",
    mountain: "June to September for hiking, December to March for skiing",
    city: "Spring (March to May) or Fall (September to November)",
    adventure: "June to September for outdoor activities",
    relaxing: "April to October for pleasant weather"
  };
  
  return timeRecommendations[destinationType] || "Year-round, but check specific destination for best times";
};

const generateTravelTips = (destination, budget, preferences, travelType) => {
  const tips = [];
  
  if (travelType === 'domestic') {
    tips.push("Consider booking flights 2-3 months in advance for best prices");
    tips.push("Check for local events and festivals during your visit");
  } else {
    tips.push("Book international flights 3-6 months in advance");
    tips.push("Check visa requirements and passport validity");
    tips.push("Consider travel insurance for international trips");
  }
  
  if (destination.toLowerCase().includes('beach')) {
    tips.push("Pack sunscreen and beach essentials");
    tips.push("Book accommodations early during peak season");
  }
  
  if (destination.toLowerCase().includes('mountain')) {
    tips.push("Check weather conditions before hiking");
    tips.push("Pack appropriate gear for altitude changes");
  }
  
  if (budget && budget.toLowerCase().includes('budget')) {
    tips.push("Consider staying in hostels or budget accommodations");
    tips.push("Eat at local restaurants for authentic and affordable meals");
  }
  
  if (preferences && preferences.toLowerCase().includes('family')) {
    tips.push("Look for family-friendly activities and accommodations");
    tips.push("Plan activities suitable for all ages");
  }
  
  if (preferences && preferences.toLowerCase().includes('romantic')) {
    tips.push("Book romantic accommodations and experiences");
    tips.push("Plan special dinners and sunset activities");
  }
  
  return tips;
}; 