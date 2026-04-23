"""
Cost of Living Dataset Integration
Uses the Kaggle cost of living dataset for accurate destination cost calculations.
"""

import pandas as pd
import numpy as np
import os
import logging
from typing import Dict, Optional, List, Tuple
from datetime import datetime
import asyncio
import json

logger = logging.getLogger(__name__)

class CostOfLivingDataset:
    """Cost of living data provider using the Kaggle dataset"""
    
    def __init__(self):
        self.dataset_path = "cost_of_living_dataset.csv"
        self.data = None
        self.cities_data = {}
        self.load_dataset()
        
    def load_dataset(self):
        """Load the cost of living dataset"""
        try:
            # Try to load the dataset file
            if os.path.exists(self.dataset_path):
                self.data = pd.read_csv(self.dataset_path)
                logger.info(f"Loaded cost of living dataset with {len(self.data)} cities")
                self._process_dataset()
            else:
                logger.warning(f"Dataset file {self.dataset_path} not found. Using fallback data.")
                self._create_fallback_data()
                
        except Exception as e:
            logger.error(f"Error loading dataset: {e}")
            self._create_fallback_data()
    
    def _process_dataset(self):
        """Process and clean the dataset"""
        try:
            # Clean the data
            self.data = self.data.dropna(subset=['city', 'country'])
            
            # Create a lookup dictionary for faster access
            for _, row in self.data.iterrows():
                city = row['city'].strip()
                country = row['country'].strip()
                key = f"{city}, {country}"
                
                self.cities_data[key] = {
                    'city': city,
                    'country': country,
                    'data_quality': row.get('data_quality', 0),
                    'costs': self._extract_costs_from_row(row)
                }
                
            logger.info(f"Processed {len(self.cities_data)} cities from dataset")
            
        except Exception as e:
            logger.error(f"Error processing dataset: {e}")
            self._create_fallback_data()
    
    def _extract_costs_from_row(self, row) -> Dict:
        """Extract cost categories from a dataset row"""
        try:
            return {
                # Food & Dining
                'food': {
                    'inexpensive_meal': row.get('x1', 0),
                    'mid_range_meal_2people': row.get('x2', 0),
                    'mcdonalds_meal': row.get('x3', 0),
                    'domestic_beer_restaurant': row.get('x4', 0),
                    'imported_beer_restaurant': row.get('x5', 0),
                    'cappuccino': row.get('x6', 0),
                    'coke_pepsi': row.get('x7', 0),
                    'water_restaurant': row.get('x8', 0)
                },
                
                # Groceries
                'groceries': {
                    'milk_1l': row.get('x9', 0),
                    'bread_500g': row.get('x10', 0),
                    'rice_1kg': row.get('x11', 0),
                    'eggs_12': row.get('x12', 0),
                    'cheese_1kg': row.get('x13', 0),
                    'chicken_1kg': row.get('x14', 0),
                    'beef_1kg': row.get('x15', 0),
                    'apples_1kg': row.get('x16', 0),
                    'banana_1kg': row.get('x17', 0),
                    'oranges_1kg': row.get('x18', 0),
                    'tomato_1kg': row.get('x19', 0),
                    'potato_1kg': row.get('x20', 0),
                    'onion_1kg': row.get('x21', 0),
                    'lettuce_head': row.get('x22', 0),
                    'water_1_5l': row.get('x23', 0),
                    'wine_mid_range': row.get('x24', 0),
                    'domestic_beer_market': row.get('x25', 0),
                    'imported_beer_market': row.get('x26', 0),
                    'cigarettes_20pack': row.get('x27', 0)
                },
                
                # Transportation
                'transport': {
                    'one_way_ticket': row.get('x28', 0),
                    'monthly_pass': row.get('x29', 0),
                    'taxi_start': row.get('x30', 0),
                    'taxi_1km': row.get('x31', 0),
                    'taxi_1hour_waiting': row.get('x32', 0),
                    'gasoline_1l': row.get('x33', 0),
                    'volkswagen_golf': row.get('x34', 0),
                    'toyota_corolla': row.get('x35', 0)
                },
                
                # Utilities & Services
                'utilities': {
                    'basic_utilities_85m2': row.get('x36', 0),
                    'mobile_1min': row.get('x37', 0),
                    'internet_60mbps': row.get('x38', 0)
                },
                
                # Entertainment & Activities
                'entertainment': {
                    'fitness_club_monthly': row.get('x39', 0),
                    'tennis_court_1hour': row.get('x40', 0),
                    'cinema_international': row.get('x41', 0)
                },
                
                # Education
                'education': {
                    'preschool_monthly': row.get('x42', 0),
                    'primary_school_yearly': row.get('x43', 0)
                },
                
                # Clothing
                'clothing': {
                    'jeans_levis': row.get('x44', 0),
                    'summer_dress': row.get('x45', 0),
                    'nike_running_shoes': row.get('x46', 0),
                    'business_shoes': row.get('x47', 0)
                },
                
                # Housing
                'housing': {
                    'apartment_1bed_center': row.get('x48', 0),
                    'apartment_1bed_outside': row.get('x49', 0),
                    'apartment_3bed_center': row.get('x50', 0),
                    'apartment_3bed_outside': row.get('x51', 0),
                    'price_sqm_center': row.get('x52', 0),
                    'price_sqm_outside': row.get('x53', 0)
                },
                
                # Income
                'income': {
                    'avg_monthly_salary': row.get('x54', 0),
                    'mortgage_rate': row.get('x55', 0)
                }
            }
            
        except Exception as e:
            logger.error(f"Error extracting costs from row: {e}")
            return {}
    
    def _create_fallback_data(self):
        """Create fallback data when dataset is not available"""
        fallback_cities = {
            "Bali, Indonesia": {
                "city": "Bali",
                "country": "Indonesia",
                "data_quality": 1,
                "costs": self._get_fallback_costs("Bali")
            },
            "Maldives": {
                "city": "Maldives",
                "country": "Maldives",
                "data_quality": 1,
                "costs": self._get_fallback_costs("Maldives")
            },
            "Tokyo, Japan": {
                "city": "Tokyo",
                "country": "Japan",
                "data_quality": 1,
                "costs": self._get_fallback_costs("Tokyo")
            },
            "New York, USA": {
                "city": "New York",
                "country": "USA",
                "data_quality": 1,
                "costs": self._get_fallback_costs("New York")
            },
            "London, UK": {
                "city": "London",
                "country": "UK",
                "data_quality": 1,
                "costs": self._get_fallback_costs("London")
            }
        }
        
        self.cities_data = fallback_cities
        logger.info("Using fallback cost of living data")
    
    def _get_fallback_costs(self, city: str) -> Dict:
        """Get fallback costs for a specific city"""
        fallback_costs = {
            "Bali": {
                "food": {"inexpensive_meal": 3, "mid_range_meal_2people": 25, "cappuccino": 2.5},
                "groceries": {"milk_1l": 1.5, "bread_500g": 1, "rice_1kg": 1.2, "eggs_12": 2.5},
                "transport": {"one_way_ticket": 0.5, "taxi_1km": 0.8, "gasoline_1l": 0.9},
                "utilities": {"basic_utilities_85m2": 80, "internet_60mbps": 30},
                "entertainment": {"fitness_club_monthly": 40, "cinema_international": 5},
                "housing": {"apartment_1bed_center": 600, "apartment_1bed_outside": 400},
                "income": {"avg_monthly_salary": 800}
            },
            "Maldives": {
                "food": {"inexpensive_meal": 8, "mid_range_meal_2people": 60, "cappuccino": 4},
                "groceries": {"milk_1l": 2.5, "bread_500g": 2, "rice_1kg": 2.5, "eggs_12": 4},
                "transport": {"one_way_ticket": 1, "taxi_1km": 2, "gasoline_1l": 1.2},
                "utilities": {"basic_utilities_85m2": 150, "internet_60mbps": 80},
                "entertainment": {"fitness_club_monthly": 100, "cinema_international": 12},
                "housing": {"apartment_1bed_center": 2000, "apartment_1bed_outside": 1500},
                "income": {"avg_monthly_salary": 1500}
            },
            "Tokyo": {
                "food": {"inexpensive_meal": 8, "mid_range_meal_2people": 50, "cappuccino": 4},
                "groceries": {"milk_1l": 2, "bread_500g": 2.5, "rice_1kg": 3, "eggs_12": 3},
                "transport": {"one_way_ticket": 2.5, "taxi_1km": 3, "gasoline_1l": 1.5},
                "utilities": {"basic_utilities_85m2": 150, "internet_60mbps": 50},
                "entertainment": {"fitness_club_monthly": 80, "cinema_international": 15},
                "housing": {"apartment_1bed_center": 1200, "apartment_1bed_outside": 800},
                "income": {"avg_monthly_salary": 3000}
            },
            "New York": {
                "food": {"inexpensive_meal": 15, "mid_range_meal_2people": 80, "cappuccino": 5},
                "groceries": {"milk_1l": 1.2, "bread_500g": 3, "rice_1kg": 2, "eggs_12": 4},
                "transport": {"one_way_ticket": 2.75, "taxi_1km": 2.5, "gasoline_1l": 1.2},
                "utilities": {"basic_utilities_85m2": 200, "internet_60mbps": 70},
                "entertainment": {"fitness_club_monthly": 100, "cinema_international": 15},
                "housing": {"apartment_1bed_center": 2500, "apartment_1bed_outside": 1800},
                "income": {"avg_monthly_salary": 5000}
            },
            "London": {
                "food": {"inexpensive_meal": 12, "mid_range_meal_2people": 70, "cappuccino": 4},
                "groceries": {"milk_1l": 1.5, "bread_500g": 1.8, "rice_1kg": 2.5, "eggs_12": 3.5},
                "transport": {"one_way_ticket": 3, "taxi_1km": 2.5, "gasoline_1l": 1.8},
                "utilities": {"basic_utilities_85m2": 180, "internet_60mbps": 60},
                "entertainment": {"fitness_club_monthly": 90, "cinema_international": 12},
                "housing": {"apartment_1bed_center": 1800, "apartment_1bed_outside": 1200},
                "income": {"avg_monthly_salary": 3500}
            }
        }
        
        return fallback_costs.get(city, fallback_costs["New York"])
    
    async def get_cost_of_living(self, city: str, country: str = None) -> Dict:
        """Get comprehensive cost of living data for a city"""
        try:
            # Try to find the city in our dataset
            city_data = self._find_city_data(city, country)
            
            if city_data:
                return self._calculate_daily_costs(city_data)
            else:
                # Return fallback data for unknown cities
                return self._get_fallback_daily_costs(city, country)
                
        except Exception as e:
            logger.error(f"Error getting cost of living for {city}: {e}")
            return self._get_fallback_daily_costs(city, country)
    
    def _find_city_data(self, city: str, country: str = None) -> Optional[Dict]:
        """Find city data in the dataset"""
        try:
            # Try exact match first
            if country:
                key = f"{city}, {country}"
                if key in self.cities_data:
                    return self.cities_data[key]
            
            # Try city-only match
            for key, data in self.cities_data.items():
                if city.lower() in key.lower():
                    return data
            
            # Try partial match
            for key, data in self.cities_data.items():
                if city.lower() in data['city'].lower():
                    return data
            
            return None
            
        except Exception as e:
            logger.error(f"Error finding city data: {e}")
            return None
    
    def _calculate_daily_costs(self, city_data: Dict) -> Dict:
        """Calculate daily costs from city data"""
        try:
            costs = city_data['costs']
            
            # Calculate daily food costs
            daily_food = self._calculate_daily_food_cost(costs)
            
            # Calculate daily transport costs
            daily_transport = self._calculate_daily_transport_cost(costs)
            
            # Calculate daily activities costs
            daily_activities = self._calculate_daily_activities_cost(costs)
            
            # Calculate daily misc costs
            daily_misc = self._calculate_daily_misc_cost(costs)
            
            # Calculate accommodation costs
            accommodation_monthly = self._calculate_accommodation_cost(costs)
            
            # Calculate utilities costs
            utilities_monthly = self._calculate_utilities_cost(costs)
            
            daily_total = daily_food + daily_transport + daily_activities + daily_misc
            
            return {
                "daily_food": round(daily_food, 2),
                "daily_transport": round(daily_transport, 2),
                "daily_activities": round(daily_activities, 2),
                "daily_misc": round(daily_misc, 2),
                "daily_total": round(daily_total, 2),
                "weekly_total": round(daily_total * 7, 2),
                "monthly_total": round(daily_total * 30, 2),
                "accommodation_monthly": round(accommodation_monthly, 2),
                "utilities_monthly": round(utilities_monthly, 2),
                "currency": "USD",
                "source": "Kaggle Cost of Living Dataset",
                "data_quality": city_data.get('data_quality', 0),
                "last_updated": datetime.now().isoformat(),
                "city": city_data['city'],
                "country": city_data['country']
            }
            
        except Exception as e:
            logger.error(f"Error calculating daily costs: {e}")
            return self._get_fallback_daily_costs(city_data.get('city', 'Unknown'))
    
    def _calculate_daily_food_cost(self, costs: Dict) -> float:
        """Calculate daily food cost"""
        try:
            food = costs.get('food', {})
            groceries = costs.get('groceries', {})
            
            # Restaurant meals (assume 1 meal per day)
            restaurant_cost = food.get('inexpensive_meal', 0)
            
            # Groceries for other meals (breakfast, lunch, snacks)
            grocery_items = [
                groceries.get('milk_1l', 0) * 0.1,  # 100ml per day
                groceries.get('bread_500g', 0) * 0.2,  # 100g per day
                groceries.get('eggs_12', 0) * 0.17,  # 2 eggs per day
                groceries.get('rice_1kg', 0) * 0.1,  # 100g per day
                groceries.get('chicken_1kg', 0) * 0.15,  # 150g per day
                groceries.get('apples_1kg', 0) * 0.2,  # 200g per day
                groceries.get('banana_1kg', 0) * 0.2,  # 200g per day
                groceries.get('tomato_1kg', 0) * 0.1,  # 100g per day
                groceries.get('potato_1kg', 0) * 0.1,  # 100g per day
                groceries.get('water_1_5l', 0) * 0.67  # 1 liter per day
            ]
            
            daily_groceries = sum(grocery_items)
            
            return restaurant_cost + daily_groceries
            
        except Exception as e:
            logger.error(f"Error calculating daily food cost: {e}")
            return 30.0
    
    def _calculate_daily_transport_cost(self, costs: Dict) -> float:
        """Calculate daily transport cost"""
        try:
            transport = costs.get('transport', {})
            
            # Assume 2 one-way tickets per day
            public_transport = transport.get('one_way_ticket', 0) * 2
            
            # Assume occasional taxi use (1 short trip per day)
            taxi_cost = transport.get('taxi_1km', 0) * 3  # 3km trip
            
            return public_transport + taxi_cost
            
        except Exception as e:
            logger.error(f"Error calculating daily transport cost: {e}")
            return 20.0
    
    def _calculate_daily_activities_cost(self, costs: Dict) -> float:
        """Calculate daily activities cost"""
        try:
            entertainment = costs.get('entertainment', {})
            
            # Assume occasional entertainment activities
            cinema_cost = entertainment.get('cinema_international', 0) / 7  # Once per week
            fitness_cost = entertainment.get('fitness_club_monthly', 0) / 30  # Monthly fee
            tennis_cost = entertainment.get('tennis_court_1hour', 0) / 14  # Once per 2 weeks
            
            return cinema_cost + fitness_cost + tennis_cost
            
        except Exception as e:
            logger.error(f"Error calculating daily activities cost: {e}")
            return 40.0
    
    def _calculate_daily_misc_cost(self, costs: Dict) -> float:
        """Calculate daily miscellaneous cost"""
        try:
            utilities = costs.get('utilities', {})
            clothing = costs.get('clothing', {})
            
            # Utilities (monthly divided by 30)
            internet_cost = utilities.get('internet_60mbps', 0) / 30
            mobile_cost = utilities.get('mobile_1min', 0) * 10  # 10 minutes per day
            
            # Clothing (monthly budget divided by 30)
            clothing_budget = (
                clothing.get('jeans_levis', 0) + 
                clothing.get('summer_dress', 0) + 
                clothing.get('nike_running_shoes', 0)
            ) / 90  # Assume clothing lasts 3 months
            
            return internet_cost + mobile_cost + clothing_budget
            
        except Exception as e:
            logger.error(f"Error calculating daily misc cost: {e}")
            return 25.0
    
    def _calculate_accommodation_cost(self, costs: Dict) -> float:
        """Calculate monthly accommodation cost"""
        try:
            housing = costs.get('housing', {})
            
            # Use 1-bedroom apartment outside center as default
            return housing.get('apartment_1bed_outside', housing.get('apartment_1bed_center', 1000))
            
        except Exception as e:
            logger.error(f"Error calculating accommodation cost: {e}")
            return 1000.0
    
    def _calculate_utilities_cost(self, costs: Dict) -> float:
        """Calculate monthly utilities cost"""
        try:
            utilities = costs.get('utilities', {})
            
            return utilities.get('basic_utilities_85m2', 120)
            
        except Exception as e:
            logger.error(f"Error calculating utilities cost: {e}")
            return 120.0
    
    def _get_fallback_daily_costs(self, city: str, country: str = None) -> Dict:
        """Get fallback daily costs"""
        return {
            "daily_food": 30.0,
            "daily_transport": 20.0,
            "daily_activities": 40.0,
            "daily_misc": 25.0,
            "daily_total": 115.0,
            "weekly_total": 805.0,
            "monthly_total": 3450.0,
            "accommodation_monthly": 1000.0,
            "utilities_monthly": 120.0,
            "currency": "USD",
            "source": "Fallback Data",
            "data_quality": 0,
            "last_updated": datetime.now().isoformat(),
            "city": city,
            "country": country
        }
    
    def get_city_list(self) -> List[Dict]:
        """Get list of all available cities"""
        try:
            cities = []
            for key, data in self.cities_data.items():
                cities.append({
                    "city": data['city'],
                    "country": data['country'],
                    "data_quality": data.get('data_quality', 0)
                })
            
            return sorted(cities, key=lambda x: x['city'])
            
        except Exception as e:
            logger.error(f"Error getting city list: {e}")
            return []
    
    def search_cities(self, query: str) -> List[Dict]:
        """Search cities by name or country"""
        try:
            results = []
            query_lower = query.lower()
            
            for key, data in self.cities_data.items():
                if (query_lower in data['city'].lower() or 
                    query_lower in data['country'].lower()):
                    results.append({
                        "city": data['city'],
                        "country": data['country'],
                        "data_quality": data.get('data_quality', 0)
                    })
            
            return results[:10]  # Limit to 10 results
            
        except Exception as e:
            logger.error(f"Error searching cities: {e}")
            return []

# Global instance
cost_of_living_dataset = CostOfLivingDataset()
