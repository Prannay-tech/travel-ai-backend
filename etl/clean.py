"""
Data cleaning and preprocessing for travel data.
"""

import pandas as pd
import numpy as np
import json
import re
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TravelDataCleaner:
    def __init__(self):
        self.cleaned_data = {}
    
    def clean_opentripmap_data(self, raw_data: List[Dict]) -> pd.DataFrame:
        """Clean and structure OpenTripMap data."""
        cleaned_records = []
        
        for place in raw_data:
            try:
                # Extract basic information
                record = {
                    'place_id': place.get('xid', ''),
                    'name': place.get('name', ''),
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
                
                # Clean and validate coordinates
                if record['latitude'] and record['longitude']:
                    record['latitude'] = float(record['latitude'])
                    record['longitude'] = float(record['longitude'])
                else:
                    record['latitude'] = None
                    record['longitude'] = None
                
                # Clean text fields
                record['name'] = self._clean_text(record['name'])
                record['description'] = self._clean_text(record['description'])
                
                cleaned_records.append(record)
                
            except Exception as e:
                logger.warning(f"Error cleaning place {place.get('xid', 'unknown')}: {e}")
                continue
        
        df = pd.DataFrame(cleaned_records)
        logger.info(f"Cleaned {len(df)} OpenTripMap records")
        return df
    
    def clean_skyscanner_data(self, raw_data: Dict) -> pd.DataFrame:
        """Clean and structure Skyscanner flight data."""
        cleaned_records = []
        
        try:
            # Extract quotes from the response
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
                    
                    cleaned_records.append(record)
                    
                except Exception as e:
                    logger.warning(f"Error cleaning quote {quote.get('quoteId', 'unknown')}: {e}")
                    continue
            
        except Exception as e:
            logger.error(f"Error processing Skyscanner data: {e}")
        
        df = pd.DataFrame(cleaned_records)
        logger.info(f"Cleaned {len(df)} Skyscanner records")
        return df
    
    def clean_place_details(self, raw_data: Dict) -> Dict:
        """Clean detailed place information."""
        try:
            cleaned = {
                'place_id': raw_data.get('xid', ''),
                'name': self._clean_text(raw_data.get('name', '')),
                'type': raw_data.get('kinds', '').split(',')[0] if raw_data.get('kinds') else '',
                'categories': raw_data.get('kinds', ''),
                'latitude': float(raw_data.get('point', {}).get('lat', 0)),
                'longitude': float(raw_data.get('point', {}).get('lon', 0)),
                'country': raw_data.get('address', {}).get('country', ''),
                'city': raw_data.get('address', {}).get('city', ''),
                'state': raw_data.get('address', {}).get('state', ''),
                'postcode': raw_data.get('address', {}).get('postcode', ''),
                'street': raw_data.get('address', {}).get('road', ''),
                'house_number': raw_data.get('address', {}).get('house_number', ''),
                'osm': raw_data.get('osm', ''),
                'wikidata': raw_data.get('wikidata', ''),
                'wikipedia': raw_data.get('wikipedia', ''),
                'rate': raw_data.get('rate', 0),
                'otm': raw_data.get('otm', ''),
                'sources': json.dumps(raw_data.get('sources', {})),
                'extent': json.dumps(raw_data.get('extent', {})),
                'url': raw_data.get('url', ''),
                'image': raw_data.get('preview', {}).get('source', ''),
                'description': self._clean_text(raw_data.get('wikipedia_extracts', {}).get('text', '')),
                'timestamp': datetime.now().isoformat()
            }
            
            return cleaned
            
        except Exception as e:
            logger.error(f"Error cleaning place details: {e}")
            return {}
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text fields."""
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\-\'\"\(\)]', '', text)
        
        return text
    
    def validate_coordinates(self, lat: float, lon: float) -> bool:
        """Validate latitude and longitude values."""
        return (-90 <= lat <= 90) and (-180 <= lon <= 180)
    
    def remove_duplicates(self, df: pd.DataFrame, subset: List[str] = None) -> pd.DataFrame:
        """Remove duplicate records."""
        if subset is None:
            subset = ['place_id'] if 'place_id' in df.columns else ['name', 'latitude', 'longitude']
        
        initial_count = len(df)
        df_cleaned = df.drop_duplicates(subset=subset, keep='first')
        removed_count = initial_count - len(df_cleaned)
        
        logger.info(f"Removed {removed_count} duplicate records")
        return df_cleaned
    
    def filter_by_quality(self, df: pd.DataFrame, min_rate: float = 0) -> pd.DataFrame:
        """Filter records by quality score."""
        if 'rate' in df.columns:
            df_filtered = df[df['rate'] >= min_rate]
            logger.info(f"Filtered to {len(df_filtered)} records with rate >= {min_rate}")
            return df_filtered
        return df

def main():
    """Example usage of TravelDataCleaner."""
    cleaner = TravelDataCleaner()
    
    # Example: Clean sample data
    sample_place = {
        'xid': 'test123',
        'name': '  Eiffel Tower  ',
        'kinds': 'cultural,historic,architecture',
        'point': {'lat': 48.8584, 'lon': 2.2945},
        'address': {'country': 'France', 'city': 'Paris'},
        'rate': 7.5,
        'wikipedia_extracts': {'text': 'The Eiffel Tower is a wrought-iron lattice tower...'}
    }
    
    cleaned = cleaner.clean_place_details(sample_place)
    print(f"Cleaned place: {cleaned}")

if __name__ == "__main__":
    main() 