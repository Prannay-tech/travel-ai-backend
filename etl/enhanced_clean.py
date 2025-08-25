"""
Enhanced data cleaning and processing with spaCy for travel data.
"""

import pandas as pd
import numpy as np
import json
import re
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime
import spacy
from cleantext import clean
import unicodedata

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedTravelDataCleaner:
    def __init__(self, spacy_model: str = "en_core_web_sm"):
        """Initialize the enhanced cleaner with spaCy model."""
        try:
            self.nlp = spacy.load(spacy_model)
            logger.info(f"Loaded spaCy model: {spacy_model}")
        except OSError:
            logger.warning(f"spaCy model {spacy_model} not found. Installing...")
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", spacy_model])
            self.nlp = spacy.load(spacy_model)
        
        # Define travel-related entity patterns
        self.travel_entities = {
            'DESTINATION': ['city', 'country', 'place', 'destination'],
            'ACTIVITY': ['museum', 'beach', 'mountain', 'restaurant', 'hotel', 'park'],
            'CULTURE': ['historic', 'cultural', 'art', 'architecture', 'heritage'],
            'NATURE': ['nature', 'outdoor', 'hiking', 'scenic', 'landscape']
        }
    
    def clean_opentripmap_data(self, raw_data: List[Dict]) -> pd.DataFrame:
        """Enhanced cleaning for OpenTripMap data with spaCy processing."""
        cleaned_records = []
        
        for place in raw_data:
            try:
                # Extract basic information
                record = {
                    'place_id': place.get('xid', ''),
                    'name': self._clean_text(place.get('name', '')),
                    'type': place.get('kinds', '').split(',')[0] if place.get('kinds') else '',
                    'categories': place.get('kinds', ''),
                    'latitude': place.get('point', {}).get('lat', None),
                    'longitude': place.get('point', {}).get('lon', None),
                    'country': place.get('address', {}).get('country', ''),
                    'city': place.get('address', {}).get('city', ''),
                    'state': place.get('address', {}).get('state', ''),
                    'postcode': place.get('address', {}).get('postcode', ''),
                    'street': place.get('address', {}).get('road', ''),
                    'house_number': place.get('address', {}).get('house_number', ''),
                    'osm': place.get('osm', ''),
                    'wikidata': place.get('wikidata', ''),
                    'wikipedia': place.get('wikipedia', ''),
                    'rate': place.get('rate', 0),
                    'otm': place.get('otm', ''),
                    'sources': json.dumps(place.get('sources', {})),
                    'extent': json.dumps(place.get('extent', {})),
                    'url': place.get('url', ''),
                    'image': place.get('preview', {}).get('source', ''),
                    'description': self._clean_text(place.get('wikipedia_extracts', {}).get('text', '')),
                    'timestamp': datetime.now().isoformat()
                }
                
                # Enhanced text processing with spaCy
                if record['description']:
                    record.update(self._extract_entities(record['description']))
                    record['description_processed'] = self._process_description(record['description'])
                
                # Clean and validate coordinates
                if record['latitude'] and record['longitude']:
                    record['latitude'] = float(record['latitude'])
                    record['longitude'] = float(record['longitude'])
                else:
                    record['latitude'] = None
                    record['longitude'] = None
                
                # Add travel tags
                record['travel_tags'] = self._generate_travel_tags(record)
                
                # Add sentiment score
                record['sentiment_score'] = self._analyze_sentiment(record['description'])
                
                cleaned_records.append(record)
                
            except Exception as e:
                logger.warning(f"Error cleaning place {place.get('xid', 'unknown')}: {e}")
                continue
        
        df = pd.DataFrame(cleaned_records)
        logger.info(f"Enhanced cleaning completed for {len(df)} OpenTripMap records")
        return df
    
    def _clean_text(self, text: str) -> str:
        """Enhanced text cleaning using multiple libraries."""
        if not text:
            return ""
        
        # Use clean-text library for basic cleaning
        text = clean(text, 
                    fix_unicode=True,
                    to_ascii=True,
                    lower=False,
                    no_line_breaks=True,
                    no_urls=True,
                    no_emails=True,
                    no_phone_numbers=True,
                    no_numbers=False,
                    no_digits=False,
                    no_currency_symbols=False,
                    no_punct=False,
                    replace_with_punct="",
                    replace_with_url="",
                    replace_with_email="",
                    replace_with_phone_number="",
                    replace_with_number="",
                    replace_with_digit="",
                    replace_with_currency_symbol="",
                    lang="en")
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Normalize unicode characters
        text = unicodedata.normalize('NFKC', text)
        
        return text
    
    def _extract_entities(self, text: str) -> Dict:
        """Extract named entities and travel-related information using spaCy."""
        if not text:
            return {}
        
        doc = self.nlp(text)
        
        entities = {
            'locations': [],
            'organizations': [],
            'dates': [],
            'money': [],
            'activities': []
        }
        
        for ent in doc.ents:
            if ent.label_ == 'GPE':  # Countries, cities, states
                entities['locations'].append(ent.text)
            elif ent.label_ == 'ORG':  # Organizations
                entities['organizations'].append(ent.text)
            elif ent.label_ == 'DATE':  # Dates
                entities['dates'].append(ent.text)
            elif ent.label_ == 'MONEY':  # Money amounts
                entities['money'].append(ent.text)
        
        # Extract travel activities from text
        for token in doc:
            if token.pos_ == 'NOUN' and token.text.lower() in [
                'museum', 'beach', 'mountain', 'restaurant', 'hotel', 'park',
                'temple', 'castle', 'garden', 'market', 'theater', 'stadium'
            ]:
                entities['activities'].append(token.text)
        
        return {
            'extracted_locations': json.dumps(entities['locations']),
            'extracted_organizations': json.dumps(entities['organizations']),
            'extracted_dates': json.dumps(entities['dates']),
            'extracted_money': json.dumps(entities['money']),
            'extracted_activities': json.dumps(entities['activities'])
        }
    
    def _process_description(self, text: str) -> str:
        """Process description to extract key information."""
        if not text:
            return ""
        
        doc = self.nlp(text)
        
        # Extract key sentences (first and last)
        sentences = list(doc.sents)
        if len(sentences) >= 2:
            key_sentences = [sentences[0].text, sentences[-1].text]
        else:
            key_sentences = [sent.text for sent in sentences]
        
        return " ".join(key_sentences)
    
    def _generate_travel_tags(self, record: Dict) -> str:
        """Generate travel-specific tags based on content."""
        tags = set()
        
        # Add tags based on categories
        if record.get('categories'):
            categories = record['categories'].lower()
            if 'beach' in categories or 'coastal' in categories:
                tags.add('beach')
            if 'mountain' in categories or 'hiking' in categories:
                tags.add('mountain')
            if 'museum' in categories or 'cultural' in categories:
                tags.add('culture')
            if 'restaurant' in categories or 'food' in categories:
                tags.add('food')
            if 'historic' in categories:
                tags.add('history')
            if 'nature' in categories or 'park' in categories:
                tags.add('nature')
        
        # Add tags based on description
        if record.get('description'):
            desc = record['description'].lower()
            if any(word in desc for word in ['beach', 'coast', 'ocean']):
                tags.add('beach')
            if any(word in desc for word in ['mountain', 'hike', 'climb']):
                tags.add('mountain')
            if any(word in desc for word in ['museum', 'art', 'culture']):
                tags.add('culture')
            if any(word in desc for word in ['restaurant', 'food', 'cuisine']):
                tags.add('food')
            if any(word in desc for word in ['historic', 'ancient', 'heritage']):
                tags.add('history')
            if any(word in desc for word in ['nature', 'park', 'garden']):
                tags.add('nature')
        
        return ','.join(sorted(tags))
    
    def _analyze_sentiment(self, text: str) -> float:
        """Simple sentiment analysis based on positive/negative words."""
        if not text:
            return 0.0
        
        positive_words = {
            'beautiful', 'amazing', 'wonderful', 'fantastic', 'excellent',
            'great', 'good', 'nice', 'lovely', 'stunning', 'breathtaking',
            'magnificent', 'spectacular', 'impressive', 'famous', 'popular'
        }
        
        negative_words = {
            'bad', 'terrible', 'awful', 'disappointing', 'poor',
            'crowded', 'expensive', 'dirty', 'noisy', 'dangerous'
        }
        
        words = set(text.lower().split())
        positive_count = len(words.intersection(positive_words))
        negative_count = len(words.intersection(negative_words))
        
        total_words = len(words)
        if total_words == 0:
            return 0.0
        
        # Simple sentiment score between -1 and 1
        sentiment = (positive_count - negative_count) / total_words
        return max(-1.0, min(1.0, sentiment))
    
    def clean_skyscanner_data(self, raw_data: Dict) -> pd.DataFrame:
        """Enhanced cleaning for Skyscanner flight data."""
        cleaned_records = []
        
        try:
            quotes = raw_data.get('quotes', [])
            
            for quote in quotes:
                try:
                    record = {
                        'quote_id': quote.get('quoteId', ''),
                        'min_price': quote.get('minPrice', {}).get('amount', 0),
                        'currency': quote.get('minPrice', {}).get('currency', 'USD'),
                        'direct': quote.get('direct', False),
                        'outbound_leg': json.dumps(quote.get('outboundLeg', {})),
                        'inbound_leg': json.dumps(quote.get('inboundLeg', {})),
                        'timestamp': datetime.now().isoformat()
                    }
                    
                    # Extract leg information
                    outbound_leg = quote.get('outboundLeg', {})
                    record.update({
                        'origin_id': outbound_leg.get('originId', ''),
                        'destination_id': outbound_leg.get('destinationId', ''),
                        'departure_date': outbound_leg.get('departureDate', ''),
                        'carrier_ids': ','.join(str(cid) for cid in outbound_leg.get('carrierIds', [])),
                        'stops': len(outbound_leg.get('stopIds', [])),
                    })
                    
                    # Add price analysis
                    record['price_category'] = self._categorize_price(record['min_price'])
                    record['is_expensive'] = record['min_price'] > 500
                    
                    cleaned_records.append(record)
                    
                except Exception as e:
                    logger.warning(f"Error cleaning quote {quote.get('quoteId', 'unknown')}: {e}")
                    continue
            
        except Exception as e:
            logger.error(f"Error processing Skyscanner data: {e}")
        
        df = pd.DataFrame(cleaned_records)
        logger.info(f"Enhanced cleaning completed for {len(df)} Skyscanner records")
        return df
    
    def clean_amadeus_data(self, raw_data: List[Dict]) -> pd.DataFrame:
        """Enhanced cleaning for Amadeus flight data."""
        cleaned_records = []
        
        try:
            for flight in raw_data:
                try:
                    # Extract basic flight information
                    itineraries = flight.get('itineraries', [])
                    outbound_itinerary = itineraries[0] if itineraries else {}
                    segments = outbound_itinerary.get('segments', [])
                    
                    # Calculate stops
                    stops = max(0, len(segments) - 1)
                    
                    # Extract price information
                    price_info = flight.get('price', {})
                    total_price = price_info.get('total', 0)
                    currency = price_info.get('currency', 'USD')
                    
                    # Extract route information
                    route_name = flight.get('route_name', '')
                    origin = flight.get('origin', '')
                    destination = flight.get('destination', '')
                    
                    record = {
                        'quote_id': flight.get('id', ''),
                        'min_price': float(total_price) if total_price else 0,
                        'currency': currency,
                        'direct': stops == 0,
                        'outbound_leg': json.dumps(outbound_itinerary),
                        'inbound_leg': json.dumps(itineraries[1] if len(itineraries) > 1 else {}),
                        'origin_id': origin,
                        'destination_id': destination,
                        'departure_date': segments[0].get('departure', {}).get('at', '').split('T')[0] if segments else '',
                        'carrier_ids': ','.join(set(seg.get('carrierCode', '') for seg in segments)),
                        'stops': stops,
                        'price_category': self._categorize_price(float(total_price) if total_price else 0),
                        'is_expensive': float(total_price) > 500 if total_price else False,
                        'route_name': route_name,
                        'duration': outbound_itinerary.get('duration', ''),
                        'created_at': datetime.now().isoformat(),
                        'updated_at': datetime.now().isoformat()
                    }
                    
                    cleaned_records.append(record)
                    
                except Exception as e:
                    logger.warning(f"Error cleaning flight {flight.get('id', 'unknown')}: {e}")
                    continue
            
        except Exception as e:
            logger.error(f"Error processing Amadeus data: {e}")
        
        df = pd.DataFrame(cleaned_records)
        logger.info(f"Enhanced cleaning completed for {len(df)} Amadeus records")
        return df
    
    def _categorize_price(self, price: float) -> str:
        """Categorize flight prices."""
        if price < 200:
            return 'budget'
        elif price < 500:
            return 'moderate'
        elif price < 1000:
            return 'expensive'
        else:
            return 'luxury'
    
    def remove_duplicates(self, df: pd.DataFrame, subset: List[str] = None) -> pd.DataFrame:
        """Remove duplicate records with enhanced logic."""
        if subset is None:
            subset = ['place_id'] if 'place_id' in df.columns else ['name', 'latitude', 'longitude']
        
        initial_count = len(df)
        df_cleaned = df.drop_duplicates(subset=subset, keep='first')
        removed_count = initial_count - len(df_cleaned)
        
        logger.info(f"Removed {removed_count} duplicate records")
        return df_cleaned
    
    def filter_by_quality(self, df: pd.DataFrame, min_rate: float = 0) -> pd.DataFrame:
        """Filter records by quality score with enhanced criteria."""
        if 'rate' in df.columns:
            df_filtered = df[df['rate'] >= min_rate]
            logger.info(f"Filtered to {len(df_filtered)} records with rate >= {min_rate}")
            return df_filtered
        return df
    
    def add_geographic_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add geographic features and clustering."""
        if 'latitude' in df.columns and 'longitude' in df.columns:
            # Add hemisphere information
            df['hemisphere'] = df['latitude'].apply(lambda x: 'north' if x > 0 else 'south')
            df['timezone_approx'] = df['longitude'].apply(lambda x: int(x / 15))
            
            # Add continent approximation (simplified)
            df['continent_approx'] = df['latitude'].apply(self._approximate_continent)
        
        return df
    
    def _approximate_continent(self, lat: float) -> str:
        """Approximate continent based on latitude/longitude."""
        if pd.isna(lat):
            return 'unknown'
        
        if lat > 60:
            return 'europe'
        elif lat > 30:
            return 'asia'
        elif lat > 0:
            return 'africa'
        elif lat > -30:
            return 'south_america'
        else:
            return 'antarctica'

def main():
    """Example usage of EnhancedTravelDataCleaner."""
    cleaner = EnhancedTravelDataCleaner()
    
    # Example: Clean sample data
    sample_place = {
        'xid': 'test123',
        'name': '  Eiffel Tower  ',
        'kinds': 'cultural,historic,architecture',
        'point': {'lat': 48.8584, 'lon': 2.2945},
        'address': {'country': 'France', 'city': 'Paris'},
        'rate': 7.5,
        'wikipedia_extracts': {
            'text': 'The Eiffel Tower is a beautiful wrought-iron lattice tower located on the Champ de Mars in Paris, France. It was constructed from 1887 to 1889 as the centerpiece of the 1889 World\'s Fair and is one of the most famous landmarks in the world.'
        }
    }
    
    cleaned = cleaner.clean_opentripmap_data([sample_place])
    print(f"Enhanced cleaned place: {cleaned.iloc[0].to_dict()}")

if __name__ == "__main__":
    main() 