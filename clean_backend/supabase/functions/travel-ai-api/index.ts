import { serve } from "https://deno.land/std@0.168.0/http/server.ts"

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

serve(async (req) => {
  // Handle CORS
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    const url = new URL(req.url)
    const path = url.pathname
    const method = req.method

    // Route handling
    if (path === '/health' && method === 'GET') {
      return new Response(
        JSON.stringify({ 
          status: "healthy", 
          timestamp: new Date().toISOString() 
        }),
        { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      )
    }

    if (path === '/chat' && method === 'POST') {
      const { message, conversation_history } = await req.json()
      
      // Call Groq API
      const groqResponse = await fetch('https://api.groq.com/openai/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${Deno.env.get('GROQ_API_KEY')}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          model: 'llama3-70b-8192',
          messages: [
            {
              role: 'system',
              content: `You are an expert AI travel planner. Your job is to help users plan their perfect trip by extracting their travel preferences from natural language conversations.

Key responsibilities:
1. Extract travel preferences from user messages
2. Ask clarifying questions when needed
3. Provide helpful travel advice and suggestions
4. Guide users through the planning process

Travel preference categories to extract:
- Budget per person (e.g., "$1000-2000", "$500+")
- Number of people traveling (e.g., "2 people", "family of 4")
- Travel from location (Ask them to type in their city and country and extract location from that)
- Travel type: "domestic" or "international"
- Destination type: "beach", "mountain", "city", "historic", "religious", "adventure", "relaxing"
- Travel dates (e.g., "next summer", "December 2024")
- Currency preference (ALL valid currencies, convert them to USD in backend for uniformity but display prices in the user's preferred currency after converting from USD)
- Additional preferences (e.g., "romantic getaway", "family-friendly")

Always respond in a friendly, helpful manner. If you need more information, ask specific questions.`
            },
            ...conversation_history,
            { role: 'user', content: message }
          ],
          temperature: 0.3,
          max_tokens: 800,
          top_p: 0.8,
          frequency_penalty: 0.1,
          presence_penalty: 0.1
        })
      })

      const data = await groqResponse.json()
      
      return new Response(
        JSON.stringify({ response: data.choices[0].message.content }),
        { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      )
    }

    if (path === '/flights' && method === 'POST') {
      const { origin, destination, departure_date, passengers } = await req.json()
      
      // Try Amadeus API first
      let flights = []
      
      try {
        // Get Amadeus token
        const tokenResponse = await fetch('https://test.api.amadeus.com/v1/security/oauth2/token', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: new URLSearchParams({
            grant_type: 'client_credentials',
            client_id: Deno.env.get('AMADEUS_CLIENT_ID') || '',
            client_secret: Deno.env.get('AMADEUS_CLIENT_SECRET') || ''
          })
        })

        if (tokenResponse.ok) {
          const tokenData = await tokenResponse.json()
          const accessToken = tokenData.access_token

          // Search flights
          const flightResponse = await fetch(
            `https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode=${origin}&destinationLocationCode=${destination}&departureDate=${departure_date}&adults=${passengers}&max=10`,
            {
              headers: {
                'Authorization': `Bearer ${accessToken}`
              }
            }
          )

          if (flightResponse.ok) {
            const flightData = await flightResponse.json()
            flights = flightData.data?.map((flight: any) => ({
              id: `amadeus_${flight.id}`,
              airline: flight.itineraries[0]?.segments[0]?.carrierCode || 'Unknown',
              flight_number: `${flight.itineraries[0]?.segments[0]?.carrierCode || ''} ${flight.itineraries[0]?.segments[0]?.number || ''}`,
              departure_time: flight.itineraries[0]?.segments[0]?.departure?.at || '',
              arrival_time: flight.itineraries[0]?.segments[flight.itineraries[0]?.segments.length - 1]?.arrival?.at || '',
              duration: flight.itineraries[0]?.duration || '',
              price: { USD: parseFloat(flight.price.total) || 0 },
              stops: (flight.itineraries[0]?.segments?.length || 1) - 1,
              aircraft: 'Commercial Aircraft',
              booking_link: `https://www.amadeus.com/flights/${flight.id}`,
              source: 'Amadeus'
            })) || []
          }
        }
      } catch (error) {
        console.error('Amadeus API error:', error)
      }

      // Fallback to mock data if no flights found
      if (flights.length === 0) {
        flights = [
          {
            id: "mock_1",
            airline: "Delta Airlines",
            flight_number: "DL123",
            departure_time: `${departure_date}T09:00:00`,
            arrival_time: `${departure_date}T11:30:00`,
            duration: "2h 30m",
            price: { USD: 450, EUR: 380, GBP: 330 },
            stops: 0,
            aircraft: "Boeing 737",
            booking_link: "https://www.delta.com",
            source: "Mock Data"
          },
          {
            id: "mock_2",
            airline: "American Airlines",
            flight_number: "AA456",
            departure_time: `${departure_date}T14:15:00`,
            arrival_time: `${departure_date}T16:45:00`,
            duration: "2h 30m",
            price: { USD: 380, EUR: 320, GBP: 280 },
            stops: 1,
            aircraft: "Airbus A320",
            booking_link: "https://www.aa.com",
            source: "Mock Data"
          }
        ]
      }
      
      return new Response(
        JSON.stringify({ 
          success: true, 
          flights, 
          search: { origin, destination, departure_date, passengers } 
        }),
        { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      )
    }

    if (path.startsWith('/currency/convert') && method === 'GET') {
      const params = url.searchParams
      const amount = parseFloat(params.get('amount') || '1')
      const from_currency = params.get('from_currency') || 'USD'
      const to_currency = params.get('to_currency') || 'EUR'
      
      // Try real currency API
      let conversion = null
      
      try {
        const currencyResponse = await fetch(
          `https://api.exchangerate.host/convert?from=${from_currency}&to=${to_currency}&amount=${amount}`,
          {
            headers: {
              'apikey': Deno.env.get('CURRENCY_API_KEY') || ''
            }
          }
        )

        if (currencyResponse.ok) {
          const currencyData = await currencyResponse.json()
          conversion = {
            converted_amount: currencyData.result,
            rate: currencyData.info?.rate || 1,
            source: 'ExchangeRate-API'
          }
        }
      } catch (error) {
        console.error('Currency API error:', error)
      }

      // Fallback to mock conversion
      if (!conversion) {
        const rates = { USD: 1, EUR: 0.85, GBP: 0.73, CAD: 1.25, AUD: 1.35 }
        const converted_amount = amount * (rates[to_currency as keyof typeof rates] / rates[from_currency as keyof typeof rates])
        conversion = {
          converted_amount: Math.round(converted_amount * 100) / 100,
          rate: rates[to_currency as keyof typeof rates] / rates[from_currency as keyof typeof rates],
          source: 'Mock Data'
        }
      }
      
      return new Response(
        JSON.stringify(conversion),
        { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      )
    }

    if (path.startsWith('/weather/') && method === 'GET') {
      const location = path.split('/weather/')[1]
      
      // Try real weather API
      let weather = null
      
      try {
        const weatherResponse = await fetch(
          `http://api.weatherapi.com/v1/current.json?key=${Deno.env.get('WEATHER_API_KEY')}&q=${location}&aqi=no`
        )

        if (weatherResponse.ok) {
          const weatherData = await weatherResponse.json()
          weather = {
            location: weatherData.location?.name || location,
            country: weatherData.location?.country || 'Unknown',
            temperature_c: weatherData.current?.temp_c,
            temperature_f: weatherData.current?.temp_f,
            condition: weatherData.current?.condition?.text || 'Unknown',
            condition_icon: weatherData.current?.condition?.icon || '',
            humidity: weatherData.current?.humidity,
            wind_kph: weatherData.current?.wind_kph,
            feels_like_c: weatherData.current?.feelslike_c,
            feels_like_f: weatherData.current?.feelslike_f,
            source: 'WeatherAPI.com'
          }
        }
      } catch (error) {
        console.error('Weather API error:', error)
      }

      // Fallback to mock weather
      if (!weather) {
        weather = {
          location,
          country: 'Unknown',
          temperature_c: 22,
          temperature_f: 72,
          condition: 'Sunny',
          condition_icon: '//cdn.weatherapi.com/weather/64x64/day/113.png',
          humidity: 65,
          wind_kph: 15,
          feels_like_c: 24,
          feels_like_f: 75,
          source: 'Mock Data'
        }
      }
      
      return new Response(
        JSON.stringify({ success: true, weather }),
        { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      )
    }

    // Default response
    return new Response(
      JSON.stringify({ error: 'Endpoint not found' }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 404 }
    )

  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 500 }
    )
  }
})
