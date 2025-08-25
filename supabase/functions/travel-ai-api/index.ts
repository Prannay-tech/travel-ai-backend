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
    const headers = Object.fromEntries(req.headers.entries())

    console.log('=== DEBUG INFO ===')
    console.log('Method:', method)
    console.log('Path:', path)
    console.log('Full URL:', req.url)
    console.log('Headers:', JSON.stringify(headers, null, 2))

    // Return debug info for all requests
    return new Response(
      JSON.stringify({ 
        message: "Debug response",
        method: method,
        path: path,
        fullUrl: req.url,
        headers: headers,
        timestamp: new Date().toISOString()
      }),
      { 
        headers: { 
          ...corsHeaders, 
          'Content-Type': 'application/json' 
        } 
      }
    )

  } catch (error) {
    return new Response(
      JSON.stringify({ 
        error: error.message,
        timestamp: new Date().toISOString()
      }),
      { 
        headers: { 
          ...corsHeaders, 
          'Content-Type': 'application/json' 
        }, 
        status: 500 
      }
    )
  }
})
