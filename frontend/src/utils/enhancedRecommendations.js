// Enhanced AI Travel Recommendation System
// This system provides intelligent destination matching based on user preferences

// Comprehensive destination database
const destinationDatabase = {
  beach: // Domestic Beach Destinations
  [object Object]      name: "Miami Beach, Florida",
      country: USA",
      state:FL,      type: "beach",
      description: "Famous for its Art Deco architecture, white sand beaches, and vibrant nightlife",
      image: "https://images.unsplash.com/photo-1514214246283d4275400,
      rating: 80.7
      cost_day_usd: 180,
      weather: Tropical, 2032year-round",
      highlights: ["South Beach", Art Deco District", Cuban cuisine",Water sports"],
      best_time: "March to May, October to December",
      airport: "MIA",
      avg_flight_cost: 250,
      activities: ["swimming, unbathing", "nightlife",cultural", "food],   family_friendly: true,
      romantic: true,
      budget_friendly: false
    },
    [object Object]  name: "San Diego, California",
      country: USA",
      state:CA,      type: "beach",
      description: "Perfect weather year-round with beautiful beaches and laid-back vibe",
      image: "https://images.unsplash.com/photo-15069592534621da4d32400,
      rating: 80.9
      cost_day_usd: 20,
      weather: Mediterranean, 1525year-round",
      highlights: ["La Jolla", Gaslamp Quarter", Zoo, raft beer"],
      best_time: March to November",
      airport: "SAN",
      avg_flight_cost: 300,
      activities: ["swimming", surfing,family", "food",culture],   family_friendly: true,
      romantic: true,
      budget_friendly: false
    },
   [object Object]     name: "Myrtle Beach, South Carolina",
      country: USA",
      state:SC,      type: "beach",
      description: "Family-friendly beach destination with golf courses and entertainment",
      image: "https://images.unsplash.com/photo-15069592534621da4d32400,
      rating: 70.8
      cost_day_usd: 120,
      weather:Subtropical, 10-30°C",
      highlights: ["Broadway at the Beach,Golf courses", "Family attractions",Seafood"],
      best_time:April to October",
      airport: "MYR",
      avg_flight_cost: 200,
      activities: ["swimming,golf", "family", entertainment],   family_friendly: true,
      romantic: false,
      budget_friendly: true
    },
    [object Object]      name: "Outer Banks, North Carolina",
      country: USA",
      state:NC,      type: "beach",
      description:Peaceful barrier islands with pristine beaches and rich history",
      image: "https://images.unsplash.com/photo-15069592534621da4d32400,
      rating: 80.2
      cost_day_usd: 140,
      weather: Subtropical, 5-30°C",
      highlights: ["Wright Brothers Memorial",Wild horses",Lighthouses",Fishing"],
      best_time:May to September",
      airport: "ORF",
      avg_flight_cost: 220,
      activities: ["swimming", "fishing", history", "nature],   family_friendly: true,
      romantic: true,
      budget_friendly: true
    },
    // International Beach Destinations
  [object Object]
      name: "Bali, Indonesia",
      country: Indonesia,      type: "beach",
      description: Tropical paradise with stunning beaches, rich culture, and affordable luxury",
      image: "https://images.unsplash.com/photo-1537953773345d1723400,
      rating: 90.2
      cost_day_usd: 80,
      weather: Tropical, 2532year-round",
      highlights:Beach resorts",Cultural temples", Rice terraces",Water sports"],
      best_time:April to October",
      airport: "DPS",
      avg_flight_cost: 1200,
      activities: ["swimming,culture",spa", adventure", "food],   family_friendly: true,
      romantic: true,
      budget_friendly: true
    },
  [object Object]
      name:Maldives",
      country:Maldives,      type: "beach",
      description: "Ultimate luxury beach destination with overwater bungalows",
      image: "https://images.unsplash.com/photo-1514282401047d79a71a59000000000400,
      rating: 90.5
      cost_day_usd: 30,
      weather: Tropical, 2530year-round",
      highlights: ["Overwater bungalows", "Crystal clear waters, Snorkeling, Luxury resorts"],
      best_time: November to April",
      airport: "MLE",
      avg_flight_cost: 1500,
      activities: [swimming,snorkeling", luxury",romance],   family_friendly: false,
      romantic: true,
      budget_friendly: false
    },
   [object Object]
      name:Phuket, Thailand",
      country:Thailand,      type: "beach",
      description: "Tropical island with beautiful beaches, vibrant culture, and great food",
      image: "https://images.unsplash.com/photo-15069592534621da4d32400,
      rating: 80.8
      cost_day_usd: 90,
      weather: Tropical, 2532year-round",
      highlights: ["Patong Beach", Phi Phi Islands,Thai cuisine", Night markets"],
      best_time: November to April",
      airport: "HKT",
      avg_flight_cost: 1000,
      activities: ["swimming,island_hopping", food", "nightlife],   family_friendly: true,
      romantic: true,
      budget_friendly: true
    },
 [object Object]
      name: Cancun, Mexico",
      country: "Mexico,      type: "beach",
      description: "Famous beach destination with crystal clear waters and Mayan ruins",
      image: "https://images.unsplash.com/photo-1559827260dc66ef19?w=400,
      rating: 80.5
      cost_day_usd: 150,
      weather: Tropical, 20-35°C",
      highlights: ["Hotel Zone,Chichen Itza,Isla Mujeres", "Mexican cuisine"],
      best_time: December to April",
      airport: "CUN",
      avg_flight_cost: 400,
      activities: ["swimming", culture", food", "adventure],   family_friendly: true,
      romantic: true,
      budget_friendly: true
    }
  ],
  mountain: [
    // Domestic Mountain Destinations
    [object Object]     name:Denver, Colorado",
      country: USA",
      state:CO",
      type:mountain
      description: "Gateway to the Rockies with outdoor adventures and craft beer scene",
      image: "https://images.unsplash.com/photo-15069592534621da4d32400,
      rating: 80.5
      cost_day_usd: 150,
      weather:Mountain, -5,
      highlights:Rocky Mountains", Craft breweries",Skiing", "Hiking"],
      best_time: June to September, December to March",
      airport: "DEN",
      avg_flight_cost: 280,
      activities: ["hiking",skiing",breweries",outdoor],   family_friendly: true,
      romantic: true,
      budget_friendly: true
    },
   [object Object]
      name:Asheville, North Carolina",
      country: USA",
      state:NC",
      type:mountain
      description: "Artsy mountain town with craft beer and outdoor activities",
      image: "https://images.unsplash.com/photo-15069592534621da4d32400,
      rating: 80.3
      cost_day_usd: 130,
      weather:Mountain, 5-25°C",
      highlights: ["Blue Ridge Parkway", Biltmore Estate,Craft beer", Artgalleries"],
      best_time: March to November",
      airport: "AVL",
      avg_flight_cost: 220,
      activities: [hiking", culture", "food", "art],   family_friendly: true,
      romantic: true,
      budget_friendly: true
    },
 [object Object]
      name: "Park City, Utah",
      country: USA",
      state:UT",
      type:mountain
      description: "World-class skiing destination with charming historic downtown",
      image: "https://images.unsplash.com/photo-15069592534621da4d32400,
      rating: 80.7
      cost_day_usd: 20,
      weather: Mountain, -10,
      highlights: ["Sundance Film Festival", "Ski resorts", "Historic Main Street", "Outdoor activities"],
      best_time: December to March (skiing), June to September (summer)",
      airport: "SLC",
      avg_flight_cost: 300,
      activities: [skiing, culture,outdoor", "luxury],   family_friendly: true,
      romantic: true,
      budget_friendly: false
    },
    // International Mountain Destinations
   [object Object]      name: "Swiss Alps",
      country: "Switzerland",
      type:mountain
      description: "Majestic mountains with world-class skiing and hiking",
      image: "https://images.unsplash.com/photo-15069592534621da4d32400,
      rating: 90.3
      cost_day_usd: 250,
      weather: Alpine, varies by season",
      highlights: ["Skiing", "Hiking", "Chocolate", Scenic trains"],
      best_time: December to March (skiing), June to September (hiking)",
      airport: "ZRH/GVA",
      avg_flight_cost: 1000,
      activities: ["skiing", hiking,culture", "luxury],   family_friendly: true,
      romantic: true,
      budget_friendly: false
    },
    [object Object]      name: "Banff National Park",
      country: "Canada",
      type:mountain
      description: Stunning Canadian Rockies with pristine wilderness",
      image: "https://images.unsplash.com/photo-15069592534621da4d32400,
      rating: 90.1
      cost_day_usd: 150,
      weather:Mountain, varies by season",
      highlights: ["Lake Louise", "Wildlife", "Hiking", "Hot springs"],
      best_time: June to September",
      airport: "YYC",
      avg_flight_cost: 400,
      activities: ["hiking", "wildlife, ure", "photography],   family_friendly: true,
      romantic: true,
      budget_friendly: true
    },
 [object Object]      name: "Queenstown, New Zealand",
      country: "New Zealand",
      type:mountain
      description: Adventure capital with stunning mountain scenery",
      image: "https://images.unsplash.com/photo-15069592534621da4d32400,
      rating: 90
      cost_day_usd: 180,
      weather:Mountain, 5-25°C",
      highlights: ["Adventure sports,Fiordland", "Wine region", Lord of the Rings"],
      best_time: "December to February (summer), June to August (skiing)",
      airport: "ZQN",
      avg_flight_cost: 1200,
      activities: ["adventure,hiking", "wine",culture],   family_friendly: true,
      romantic: true,
      budget_friendly: false
    }
  ],
  city:  // Domestic City Destinations
    [object Object]   name:New York City",
      country: USA",
      state:NY",
      type: "city",
      description: "The city that never sleeps with endless entertainment and culture",
      image: "https://images.unsplash.com/photo-14964422266668d0e62e6e9?w=400,
      rating: 80.5
      cost_day_usd: 30,
      weather: Temperate, -5,
      highlights: ["Times Square,Central Park",Broadway",Museums"],
      best_time: "April to June, September to November",
      airport: "JFK/LGA",
      avg_flight_cost: 350,
      activities: ["culture",shopping", food", entertainment],   family_friendly: true,
      romantic: true,
      budget_friendly: false
    },
 [object Object]    name: Chicago, Illinois",
      country: USA",
      state:IL",
      type: "city",
      description: "Windy City with amazing architecture, food, and lakefront",
      image: "https://images.unsplash.com/photo-15069592534621da4d32400,
      rating: 80.2
      cost_day_usd: 220,
      weather:Continental, -10,
      highlights:Millennium Park", Deep dish pizza,Architecture", Lake Michigan"],
      best_time: Mayto October",
      airport: "ORD/MDW",
      avg_flight_cost: 280,
      activities:culture", "food,architecture", shopping],   family_friendly: true,
      romantic: true,
      budget_friendly: true
    },
  [object Object]
      name: "Nashville, Tennessee",
      country: USA",
      state:TN",
      type: "city",
      description: "Music City with vibrant nightlife and southern charm",
      image: "https://images.unsplash.com/photo-15069592534621da4d32400,
      rating: 80
      cost_day_usd: 180,
      weather: Subtropical, 0-35°C",
      highlights:Country music", "Broadway", "Hot chicken", "Music Row"],
      best_time: "March to May, September to November",
      airport: "BNA",
      avg_flight_cost: 250,
      activities: ["music", nightlife", "food",culture],   family_friendly: true,
      romantic: true,
      budget_friendly: true
    },
    // International City Destinations
 [object Object]      name: "Tokyo, Japan",
      country: "Japan",
      type: "city",
      description: "Futuristic metropolis blending tradition with innovation",
      image: "https://images.unsplash.com/photo-1540959733332eab4eeaf?w=400,
      rating: 90
      cost_day_usd: 180,
      weather: Temperate, 10-30°C",
      highlights: ["Technology", "Sushi", Cherry blossoms", "Efficient transport"],
      best_time: "March to May, October to November",
      airport: "NRT/HND",
      avg_flight_cost: 1200,
      activities:culture", "food,technology", shopping],   family_friendly: true,
      romantic: true,
      budget_friendly: false
    },
 [object Object]      name:Paris, France",
      country: "France",
      type: "city",
      description: City of love with iconic landmarks and world-class cuisine",
      image: "https://images.unsplash.com/photo-150260289853647d22581400,
      rating: 80.8
      cost_day_usd: 220,
      weather: Temperate, 5-25°C",
      highlights: Eiffel Tower",Louvre,French cuisine",Fashion"],
      best_time: "April to June, September to October",
      airport: "CDG/ORY",
      avg_flight_cost: 900,
      activities:culture", food", "romance", shopping],   family_friendly: true,
      romantic: true,
      budget_friendly: false
    },
  [object Object]  name:Barcelona, Spain",
      country: "Spain",
      type: "city",
      description: Vibrantcity with stunning architecture and Mediterranean charm",
      image: "https://images.unsplash.com/photo-15069592534621da4d32400,
      rating: 80.7
      cost_day_usd: 160,
      weather: Mediterranean, 10-30°C",
      highlights:Sagrada Familia",BeachesGaudi architecture"],
      best_time: "March to May, September to November",
      airport: "BCN",
      avg_flight_cost: 800,
      activities:culture", "food,architecture, ch],   family_friendly: true,
      romantic: true,
      budget_friendly: true
    }
  ],
  adventure: 
 [object Object]      name: "Queenstown, New Zealand",
      country: "New Zealand,  type: adventure
      description: Adventure capital with bungee jumping and extreme sports",
      image: "https://images.unsplash.com/photo-15069592534621da4d32400,
      rating: 90
      cost_day_usd: 180,
      weather:Mountain, 5-25°C",
      highlights: ["Bungee jumping, kydiving, Hiking", "Wine"],
      best_time: "December to February",
      airport: "ZQN",
      avg_flight_cost: 1200,
      activities: ["adventure,extreme_sports, hiking", "wine],   family_friendly: false,
      romantic: false,
      budget_friendly: false
    },
 [object Object]      name: "Interlaken, Switzerland",
      country: "Switzerland,  type: adventure
      description:Alpine adventure hub with paragliding and mountain sports",
      image: "https://images.unsplash.com/photo-15069592534621da4d32400,
      rating: 80.8
      cost_day_usd: 20,
      weather: Alpine, varies by season",
      highlights: ["Paragliding",Hiking", "Skiing, akes"],
      best_time: June to September",
      airport: "ZRH",
      avg_flight_cost: 1000,
      activities: ["adventure",paragliding",hiking", "skiing],   family_friendly: false,
      romantic: false,
      budget_friendly: false
    }
  ],
  relaxing: 
  [object Object]     name: Santorini, Greece",
      country: "Greece",
      type:relaxing
      description: "Stunning island with white buildings and breathtaking sunsets",
      image: "https://images.unsplash.com/photo-15069592534621da4d32400,
      rating: 90.2
      cost_day_usd: 20,
      weather: Mediterranean, 15-30°C",
      highlights:Sunsets", Wine",Beaches", Greek cuisine"],
      best_time: Mayto October",
      airport: "JTR",
      avg_flight_cost: 1000,
      activities: ["relaxation", wine",beach",romance],   family_friendly: false,
      romantic: true,
      budget_friendly: false
    },
    [object Object]
      name: "Maui, Hawaii",
      country: USA",
      state:HI",
      type:relaxing
      description: Peaceful Hawaiian island with beautiful beaches and waterfalls",
      image: "https://images.unsplash.com/photo-15069592534621da4d32400,
      rating: 90.1
      cost_day_usd: 250,
      weather: Tropical, 20-30°C",
      highlights: ["Road to Hana",Beaches, uaus, aterfalls"],
      best_time:April to October",
      airport: "OGG",
      avg_flight_cost: 500,
      activities: ["relaxation",beach", culture", "nature],   family_friendly: true,
      romantic: true,
      budget_friendly: false
    }
  ]
};

// Currency conversion rates
const currencyRates = {
  USD: 10  EUR:0.85  GBP: 073 JPY: 1100  CAD:1.25  AUD:1.35  CHF: 0.88,
  SGD: 1.35hanced destination matching logic
const matchDestinationType = (userInput) =>[object Object]const input = userInput.toLowerCase();
  
  // Beach destinations
  if (input.includes('beach') || input.includes('ocean') || input.includes('sea) ||    input.includes('coast') || input.includes(island || input.includes(tropical)) {
    returnbeach';
  }
  
  // Mountain destinations
  if (input.includes('mountain') || input.includes('ski') || input.includes('hike) ||    input.includes(alpine || input.includes('rocky') || input.includes('peaks)) {
    return 'mountain';
  }
  
  // City destinations
  if (input.includes('city') || input.includes('urban') || input.includes(metropolitan) ||    input.includes('downtown') || input.includes('culture') || input.includes('museum))[object Object]   return 'city';
  }
  
  // Adventure destinations
  if (input.includes('adventure') || input.includes('extreme') || input.includes('thrill) ||    input.includes(bungee || input.includes('skydive') || input.includes('climb)) {
    returnadventure';
  }
  
  // Relaxing destinations
  if (input.includes('relax') || input.includes('peaceful') || input.includes(quiet) ||    input.includes('spa') || input.includes('wellness') || input.includes(tranquil))[object Object]
    return 'relaxing';
  }
  
  // Default to beach if no clear preference
  return 'beach;
};// Enhanced budget parsing
const parseBudget = (budget, currency) => {
  if (!budget) return null;
  
  const input = budget.toLowerCase();
  
  // Extract numbers from budget string
  const numbers = budget.match(/\d+/g);
  if (!numbers) return null;
  
  let amount = parseInt(numbers[0]);
  
  // Handle different budget formats
  if (input.includes('k') || input.includes(thousand')) {
    amount *=10  } else if (input.includes('million') || input.includes('mil')) {
    amount *=100  }
  
  // Handle ranges (e.g.,10000if (numbers.length >1) {
    amount = (amount + parseInt(numbers[1])) / 2; // Use average
  }
  
  // Convert to USD for comparison
  return amount / currencyRates[currency];
};

// Enhanced preference matching
const matchPreferences = (destination, preferences) => {
  if (!preferences) return 1.0
  
  const pref = preferences.toLowerCase();
  let score = 10// Family-friendly preference
  if (pref.includes('family') && destination.family_friendly) [object Object]    score += 0.3;
  } else if (pref.includes('family) && !destination.family_friendly) [object Object]    score -= 0.2;
  }
  
  // Romantic preference
  if (pref.includes('romantic)&& destination.romantic) [object Object]    score += 0.3;
  } else if (pref.includes('romantic) && !destination.romantic) [object Object]    score -= 0.2;
  }
  
  // Budget preference
  if (pref.includes('budget') && destination.budget_friendly) [object Object]    score += 0.3;
  } else if (pref.includes('budget) && !destination.budget_friendly) [object Object]    score -= 0.2;
  }
  
  // Solo travel
  if (pref.includes('solo)) [object Object]
    score += 0.1; // Most destinations are good for solo travel
  }
  
  // Food preference
  if (pref.includes('food) && destination.activities.includes('food)) [object Object]    score += 0.2;
  }
  
  // Culture preference
  if (pref.includes('culture) && destination.activities.includes('culture)) [object Object]    score += 0.2}
  
  return Math.max(0.1, score); // Minimum score of 00.1ced recommendation algorithm
export const generateEnhancedRecommendations = (travelData) => {
  const { destination, budget, travelDates, currentLocation, preferences, currency, travelType } = travelData;
  
  // Parse budget and convert to USD
  const budgetUSD = parseBudget(budget, currency);
  
  // Determine destination type
  const destinationType = matchDestinationType(destination);
  
  // Get all destinations of the matched type
  let allDestinations = destinationDatabase[destinationType] || 
  
  // Filter by travel type (domestic vs international)
  if (travelType ===domestic') {
    allDestinations = allDestinations.filter(dest => dest.country === 'USA');
  } else if (travelType === 'international') {
    allDestinations = allDestinations.filter(dest => dest.country !== 'USA);
  }
  
  // If no destinations found, get a mix
  if (allDestinations.length === 0) {
    allDestinations = Object.values(destinationDatabase).flat();
    if (travelType === 'domestic) {   allDestinations = allDestinations.filter(dest => dest.country === USA');
    } else if (travelType === 'international) {   allDestinations = allDestinations.filter(dest => dest.country !== USA);
    }
  }
  
  // Score and rank destinations
  const scoredDestinations = allDestinations.map(dest =>[object Object]  let score = dest.rating;
    
    // Budget scoring
    if (budgetUSD) {
      const totalCost = dest.cost_day_usd * 7 + dest.avg_flight_cost;
      if (totalCost <= budgetUSD) [object Object]
        score +=0.5 Bonus for fitting budget
      } else if (totalCost <= budgetUSD * 1.5[object Object]
        score += 00.2// Small bonus for close to budget
      } else [object Object]
        score -= 00.3/ Penalty for over budget
      }
    }
    
    // Preference scoring
    score *= matchPreferences(dest, preferences);
    
    return { ...dest, score };
  });
  
  // Sort by score and take top 6const selectedDestinations = scoredDestinations
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
    ? getWeatherData(selectedDestinations[0)
    : getDefaultWeather();
  
  // Get holiday data for first destination
  const holidays = selectedDestinations.length >0 
    ? getHolidayData(selectedDestinations[0].country || selectedDestinations[0].state)
    : getDefaultHolidays();
  
  return {
    places: selectedDestinations,
    weather: weatherInfo,
    holidays: holidays,
    summary:[object Object] totalDestinations: selectedDestinations.length,
      averageCost: selectedDestinations.length > 0 
        ? selectedDestinations.reduce((sum, dest) => sum + dest.cost_day_converted,0lectedDestinations.length 
        : 0,
      averageFlightCost: selectedDestinations.length > 0 
        ? selectedDestinations.reduce((sum, dest) => sum + dest.flight_cost_converted,0lectedDestinations.length 
        :0,
      bestTimeToVisit: getBestTimeToVisit(destinationType, travelType),
      travelTips: generateTravelTips(destination, budget, preferences, travelType),
      currency: currency,
      travelType: travelType,
      matchedType: destinationType
    }
  };
};

// Helper functions
const getWeatherData = (destination) =>[object Object] const weatherData = [object Object]Miami Beach, Florida: {
      current: [object Object] temperature: 28, condition: Sunny, humidity: "75%" },
      forecast:   [object Object]day: Today", temp: 28, condition: Sunny },
        { day:Tomorrow", temp: 29condition: "Partly Cloudy },
     [object Object]day: Day3 27 condition: "Light Rain" }
      ]
    },
    Bali, Indonesia: {
      current: [object Object] temperature: 30, condition: Sunny, humidity: "80%" },
      forecast:   [object Object]day: Today", temp: 30, condition: Sunny },
        { day:Tomorrow", temp: 31condition: "Partly Cloudy },
     [object Object]day: Day3 29 condition: "Light Rain" }
      ]
    },
    Tokyo, Japan: {
      current: [object Object] temperature: 22 condition: Clear, humidity: "65%" },
      forecast:   [object Object]day: Today", temp: 22 condition: Clear },
        { day:Tomorrow", temp: 24, condition: Sunny },
     [object Object]day: Day3 20 condition: "Cloudy }
      ]
    }
  };
  
  return weatherData[destination] || getDefaultWeather();
};

const getDefaultWeather = () => ({
  current: [object Object] temperature: 22, condition: Sunny, humidity: "65 },
  forecast: [
 [object Object]day: Today", temp: 22, condition: "Sunny" },
    { day:Tomorrow", temp: 24condition: "Partly Cloudy" },
 [object Object]day: Day3 21 condition: "Light Rain }  ]
});

const getHolidayData = (country) =>[object Object] const holidayData = {
  USA:      { name:Independence Day, date: "2024-0704ription:National holiday with fireworks},
      [object Object]name: Labor Day, date: "2024-0902 description: "End of summer celebration" }
    ],
 Indonesia:      { name:Independence Day, date: "2024-08-17ription: "National independence celebration},
      { name: "Nyepi, date: "2024-03-11 description: "Balinese day of silence" }
    ],
    Japan:[object Object]name: "Golden Week, date: "2024-04-29scription: "Series of national holidays},
   [object Object]name: Obon, date: "2024-08-13,description: Buddhist festival honoring ancestors }
    ]
  };
  
  return holidayData[country] || getDefaultHolidays();
};

const getDefaultHolidays = () => [
  { name:Local Festival, date: "2024-08-15scription: "Annual cultural celebration" }
];

const convertCurrency = (usdAmount, targetCurrency) => {
  return Math.round(usdAmount * currencyRates[targetCurrency]);
};

const getBestTimeToVisit = (destinationType, travelType) => {
  const timeRecommendations = {
    beach:March to October for best beach weather,   mountain: June to September for hiking, December to March for skiing",
    city:Spring (March to May) or Fall (September to November)",
    adventure: June to September for outdoor activities,  relaxing:April to October for pleasant weather
  };
  
  return timeRecommendations[destinationType] || "Year-round, but check specific destination for best times";
};

const generateTravelTips = (destination, budget, preferences, travelType) => {
  const tips = [];
  
  if (travelType ===domestic) {
    tips.push("Consider booking flights 2-3 months in advance for best prices");
    tips.push("Check for local events and festivals during your visit); } else[object Object]   tips.push("Book international flights 3-6 months in advance");
    tips.push("Check visa requirements and passport validity");
    tips.push("Consider travel insurance for international trips");
  }
  
  if (destination.toLowerCase().includes('beach'))[object Object]   tips.push("Pack sunscreen and beach essentials");
    tips.push("Book accommodations early during peak season");
  }
  
  if (destination.toLowerCase().includes(mountain'))[object Object]  tips.push("Check weather conditions before hiking");
    tips.push("Pack appropriate gear for altitude changes");
  }
  
  if (budget && budget.toLowerCase().includes('budget')) {
    tips.push("Consider staying in hostels or budget accommodations");
    tips.push("Eat at local restaurants for authentic and affordable meals");
  }
  
  if (preferences && preferences.toLowerCase().includes('family'))[object Object]   tips.push("Look for family-friendly activities and accommodations");
    tips.push("Plan activities suitable for all ages");
  }
  
  if (preferences && preferences.toLowerCase().includes(romantic'))[object Object]   tips.push("Book romantic accommodations and experiences");
    tips.push("Plan special dinners and sunset activities");
  }
  
  return tips;
}; 