// Test file for recommendation system
import { generateRealWorldRecommendations } from './realWorldData';

// Test cases
const testCases = [
  {
    name: "Beach Lover",
    data: {
      destination: "beach",
      budget: "2000",
      travelDates: "summer 2024",
      currentLocation: "New York",
      preferences: "romantic",
      currency: "USD",
      travelType: "international"
    }
  },
  {
    name: "Mountain Adventurer",
    data: {
      destination: "mountain",
      budget: "1500",
      travelDates: "winter 2024",
      currentLocation: "Los Angeles",
      preferences: "family",
      currency: "USD",
      travelType: "domestic"
    }
  },
  {
    name: "City Explorer",
    data: {
      destination: "city",
      budget: "3000",
      travelDates: "spring 2024",
      currentLocation: "Chicago",
      preferences: "cultural",
      currency: "EUR",
      travelType: "international"
    }
  }
];

// Run tests
export const runRecommendationTests = () => {
  console.log("🧪 Testing Recommendation System...");
  
  testCases.forEach((testCase, index) => {
    console.log(`\n📋 Test ${index + 1}: ${testCase.name}`);
    console.log("Input:", testCase.data);
    
    try {
      const recommendations = generateRealWorldRecommendations(testCase.data);
      console.log("✅ Success!");
      console.log("Matched Type:", recommendations.summary.matchedType);
      console.log("Destinations Found:", recommendations.places.length);
      console.log("Top Destination:", recommendations.places[0]?.name);
      console.log("Average Cost:", recommendations.summary.averageCost);
    } catch (error) {
      console.log("❌ Error:", error.message);
    }
  });
  
  console.log("\n🎉 Recommendation System Test Complete!");
};

// Export for use in browser console
if (typeof window !== 'undefined') {
  window.testRecommendations = runRecommendationTests;
} 