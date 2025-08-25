# Flight Search API Setup Guide

This guide will help you set up the flight search APIs for your Travel AI application.

## 🚀 **Available Flight APIs**

### **1. Skyscanner API (Recommended)**
- **URL**: https://www.partners.skyscanner.net/
- **Features**: Real-time flight prices, comprehensive route coverage
- **Free Tier**: Available with limits
- **Setup Time**: 5-10 minutes

### **2. Amadeus API (Alternative)**
- **URL**: https://developers.amadeus.com/
- **Features**: Flight search, hotel search, destination insights
- **Free Tier**: 1000 API calls/month
- **Setup Time**: 10-15 minutes

## 📋 **Step 1: Get Skyscanner API Key**

### **1.1 Create Skyscanner Partner Account**
1. Go to https://www.partners.skyscanner.net/
2. Click "Get Started" or "Sign Up"
3. Fill in your details:
   - Company name: "Travel AI" (or your project name)
   - Website: Your project URL
   - Use case: "Travel planning application"
4. Submit the form

### **1.2 Get Your API Key**
1. After approval (usually within 24 hours), log into your dashboard
2. Navigate to "API Keys" section
3. Copy your API key (starts with `skyscanner_`)

### **1.3 Add to Environment Variables**
Add this line to your `clean_backend/.env` file:
```
SKYSCANNER_API_KEY=your_skyscanner_api_key_here
```

## 🔑 **Step 2: Get Amadeus API Keys (Optional)**

### **2.1 Create Amadeus Developer Account**
1. Go to https://developers.amadeus.com/
2. Click "Get Started"
3. Create a new account
4. Verify your email

### **2.2 Create Application**
1. Log into your Amadeus dashboard
2. Click "Create App"
3. Fill in the details:
   - App name: "Travel AI Flight Search"
   - Description: "AI-powered travel planning with flight search"
   - Category: "Travel"
4. Submit

### **2.3 Get API Credentials**
1. In your app dashboard, you'll see:
   - **API Key** (Client ID)
   - **API Secret** (Client Secret)
2. Copy both values

### **2.4 Add to Environment Variables**
Add these lines to your `clean_backend/.env` file:
```
AMADEUS_CLIENT_ID=your_amadeus_client_id_here
AMADEUS_CLIENT_SECRET=your_amadeus_client_secret_here
```

## 🧪 **Step 3: Test the Integration**

### **3.1 Test with Mock Data (No API Keys)**
The system will work with mock data even without API keys:

```bash
# Start the backend
cd clean_backend
python main.py
```

### **3.2 Test Flight Search Endpoint**
```bash
curl -X POST "http://localhost:8000/flights/search" \
  -H "Content-Type: application/json" \
  -d '{
    "origin": "NYC",
    "destination": "LAX",
    "departure_date": "2024-12-15",
    "passengers": 2
  }'
```

### **3.3 Test with Real APIs (After Adding Keys)**
Once you add the API keys, restart the backend and test again:

```bash
# Restart backend to load new environment variables
pkill -f "python main.py"
python main.py
```

## 📊 **API Response Format**

The flight search will return results in this format:

```json
[
  {
    "id": "skyscanner_123_agent1",
    "airline": "Delta Airlines",
    "flight_number": "DL123",
    "departure_time": "2024-12-15T09:00:00",
    "arrival_time": "2024-12-15T11:30:00",
    "duration": "2h 30m",
    "price": {
      "USD": 450,
      "EUR": 382.5,
      "GBP": 328.5
    },
    "stops": 0,
    "aircraft": "Boeing 737",
    "booking_link": "https://www.delta.com/booking/...",
    "source": "Skyscanner"
  }
]
```

## 🔧 **Configuration Options**

### **Environment Variables**
```bash
# Required for Skyscanner
SKYSCANNER_API_KEY=your_key_here

# Required for Amadeus
AMADEUS_CLIENT_ID=your_client_id_here
AMADEUS_CLIENT_SECRET=your_client_secret_here

# Optional: Currency conversion
CURRENCY_API_KEY=your_currency_key_here
```

### **API Priority**
The system will use APIs in this order:
1. **Skyscanner** (if API key available)
2. **Amadeus** (if API keys available)
3. **Mock Data** (fallback)

## 🚨 **Troubleshooting**

### **Common Issues**

#### **1. "No API key provided"**
- Check that your API key is correctly added to `.env`
- Restart the backend after adding the key
- Verify the key format (Skyscanner keys start with `skyscanner_`)

#### **2. "API rate limit exceeded"**
- Skyscanner: Check your usage limits in dashboard
- Amadeus: Free tier is 1000 calls/month
- Consider implementing caching for repeated searches

#### **3. "No flights found"**
- Check airport codes (use IATA codes like "NYC", "LAX")
- Verify date format (YYYY-MM-DD)
- Try different dates or routes

#### **4. "API timeout"**
- Skyscanner can take 10-30 seconds to return results
- Amadeus is usually faster (2-5 seconds)
- Consider implementing loading states in frontend

### **Debug Mode**
Enable debug logging by setting:
```python
logging.basicConfig(level=logging.DEBUG)
```

## 📈 **Performance Optimization**

### **Caching Strategy**
```python
# Cache flight results for 1 hour
CACHE_DURATION = 3600  # seconds

# Cache key format: f"flights:{origin}:{destination}:{date}:{passengers}"
```

### **Rate Limiting**
```python
# Implement rate limiting for API calls
MAX_REQUESTS_PER_MINUTE = 60
```

## 🎯 **Next Steps**

1. **Get Skyscanner API key** (recommended)
2. **Test with mock data** first
3. **Add real API keys** to `.env`
4. **Test real API integration**
5. **Implement caching** for better performance
6. **Add error handling** in frontend

## 💰 **Cost Analysis**

### **Free Tier Limits**
- **Skyscanner**: Varies by plan, check dashboard
- **Amadeus**: 1000 API calls/month free
- **Mock Data**: Unlimited (no cost)

### **Production Scaling**
- **Skyscanner**: Pay-per-use or monthly plans
- **Amadeus**: $0.10 per API call after free tier
- **Estimated cost**: $10-50/month for 10,000 searches

---

**Your flight search is now ready! The system will automatically use real APIs when keys are available, or fall back to mock data for testing.** 🚀
