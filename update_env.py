#!/usr/bin/env python3
"""
Script to update .env file with all API keys for the Travel AI project.
"""

import os
from pathlib import Path

def update_env_file():
    """Update .env file with all API keys."""
    
    # Define the API keys
    api_keys = {
        'CALENDARIFIC_API_KEY': 'bOuJMpGlgN6b8CNH1SdzwZXnkAi4qUQM',
        'EXCHANGERATE_API_KEY': '3404037a1e3df912b7f03b3caba8d58a',
        'WEATHERAPI_KEY': '0199245a95814f5a968202129251607',  # WeatherAPI.com key
        'FRANKFURTER_API_KEY': 'free_no_key_needed',
        'NUMBEO_API_KEY': 'your_numbeo_key_here',  # Placeholder for future
        'RESTCOUNTRIES_API_KEY': 'free_no_key_needed',
    }
    
    # Path to .env file
    env_path = Path('.env')
    
    # Read existing .env file if it exists
    existing_vars = {}
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    existing_vars[key] = value
    
    # Update with new API keys (don't overwrite existing ones unless they're placeholders)
    for key, value in api_keys.items():
        if key not in existing_vars or existing_vars[key] in ['your_key_here', 'your_api_key_here', 'free_no_key_needed']:
            existing_vars[key] = value
    
    # Write back to .env file
    with open(env_path, 'w') as f:
        f.write("# Travel AI Project Environment Variables\n")
        f.write("# API Keys for various services\n\n")
        
        # Write Supabase credentials first (if they exist)
        if 'SUPABASE_URL' in existing_vars:
            f.write(f"SUPABASE_URL={existing_vars['SUPABASE_URL']}\n")
        if 'SUPABASE_KEY' in existing_vars:
            f.write(f"SUPABASE_KEY={existing_vars['SUPABASE_KEY']}\n")
        
        f.write("\n# API Keys\n")
        
        # Write API keys
        for key, value in api_keys.items():
            f.write(f"{key}={value}\n")
        
        # Write any other existing variables
        other_vars = {k: v for k, v in existing_vars.items() 
                     if k not in ['SUPABASE_URL', 'SUPABASE_KEY'] + list(api_keys.keys())}
        
        if other_vars:
            f.write("\n# Other Variables\n")
            for key, value in other_vars.items():
                f.write(f"{key}={value}\n")
    
    print("✅ .env file updated successfully!")
    print("\n📋 Added/Updated API Keys:")
    for key, value in api_keys.items():
        print(f"   {key}: {value}")
    
    print("\n⚠️  Important Notes:")
    print("   - Some APIs are free and don't require keys")
    print("   - Numbeo API key needs to be obtained separately")
    print("   - Make sure to keep your .env file secure and never commit it to version control")

if __name__ == "__main__":
    update_env_file() 