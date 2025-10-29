# 🎨 FRONTEND REQUIREMENTS - TRAVEL AI PLATFORM

## 📋 COMPLETE VISION DOCUMENTATION

### **Phase 1: Landing Page / Home**

**Layout:**
- **Centered Search Bar** (Google-style)
  - Above: "Where do you want to go?" text
  - Background: Rotating images of fun vacation activities (via Google)
  - Below: Step-by-step flowchart explaining what the tool does
  
**Search Bar Functionality:**
- Minimal input required
- Can work with just: Location OR Time range
- Optional: Budget, Destination type, Activity preferences
- Auto-complete suggestions as user types

---

### **Phase 2: User Input Processing**

**Information Collection (via AI Chatbot):**
- **Mandatory**: Location OR Time range
- **Preferred**: Budget
- **Optional**:
  - Destination type (beaches, mountains, cities, historical places, national/state parks)
  - Activity preferences (romantic getaway, adventure sports, clubbing, fine dining)
  - Domestic vs International travel
  - Number of days

**AI Chatbot Behavior:**
- Acts like a travel agent
- Listens to user preferences
- Uses LLM to process all data
- Generates personalized recommendations

---

### **Phase 3: Top 10 Destinations Display**

**Page Structure:**
- Shows **10 destinations** ranked by budget/preferences
- Each destination card displays:
  - **Photo** of the destination
  - **Estimated Flight Price** (in light font)
  - **Estimated Hotel Price** (in light font)
  - **Total Estimated Trip Cost** (prominent)
  - Number of days based on user input

**Ranking Logic:**
- Budget-based prioritization
- Preference matching
- Days-based cost calculations
- Real-time pricing integration

---

### **Phase 4: Destination Detail Page**

**When User Clicks on a Destination:**
- Opens new page with detailed information

**Page Content:**
1. **Photos** of the destination
2. **Cost Estimates**:
   - Flight prices
   - Hotel prices
   - Activity costs
3. **Booking Links**:
   - Flight booking
   - Hotel booking
   - Activity booking

**Detailed Sections:**
- **Top 10 Activities** with:
  - Activity name
  - Cost to book
  - Links to multiple vendors
- **Hotels in Budget** with:
  - Hotel options
  - Prices
  - Booking links
- **Restaurants** with:
  - Restaurant recommendations
  - Cuisine types
  - Booking links
- **Flights** with:
  - Available flights
  - Prices
  - Booking links

**Overall Goal**: Provide **planned and curated itinerary** + **booking assistance**

---

### **Phase 5: AI Chatbot Integration**

**Chatbot UI:**
- **Always Active**: Floating popup on the side
- **Accessible**: Can be opened/used at any time
- **Interactive**: User can make requests anytime

**Dynamic Itinerary Modification:**
- Example: User says "I want restaurants with Indian food"
- **AI listens** and **modifies itinerary in real-time**
- Updates the displayed itinerary based on user preferences
- Continues to refine based on additional input

**Chatbot Features:**
- Acts like a personal travel agent
- Understands natural language
- Modifies recommendations dynamically
- Provides personalized suggestions

---

### **Phase 6: User Authentication**

**Login/Sign Up System:**
- **Guest Users**:
  - Can view default itinerary
  - Cannot customize
  - Limited functionality

- **Logged In Users**:
  - Can customize itinerary
  - Can save preferences
  - Can modify recommendations
  - Full functionality access

**Authentication Flow:**
- Sign up / Login required for customization
- Guest mode for browsing
- Seamless transition between modes

---

## 🔄 COMPLETE USER JOURNEY FLOW

### **Step 1: Landing**
1. User opens website
2. Sees search bar with "Where do you want to go?"
3. Views explanation flowchart
4. Chatbot popup visible on side

### **Step 2: Initial Search**
1. User types minimal info (location OR time)
2. AI chatbot asks clarifying questions
3. User provides preferences (budget, destination type, activities)
4. AI processes with LLM
5. System generates top 10 destinations

### **Step 3: Browse Destinations**
1. User sees 10 destination cards
2. Each shows photo, flight price, hotel price, total cost
3. User clicks on preferred destination

### **Step 4: View Details**
1. New page opens with destination details
2. Shows photos, costs, activities
3. Provides booking links for everything
4. Planned itinerary is visible

### **Step 5: Customize (If Logged In)**
1. User uses chatbot to make requests
2. Example: "I want Indian restaurants"
3. AI modifies itinerary in real-time
4. Updated itinerary reflects changes

### **Step 6: Book**
1. User clicks booking links
2. Flights, hotels, activities can be booked
3. Direct links to vendors
4. Complete booking assistance

---

## 🎯 KEY FEATURES SUMMARY

### **✅ AI-Powered**
- LLM processes user input
- Acts like a travel agent
- Generates personalized recommendations
- Modifies itinerary dynamically

### **✅ Real-Time Data**
- Live flight prices
- Live hotel prices
- Real-time activity costs
- Current booking availability

### **✅ Interactive Chatbot**
- Always accessible
- Natural language understanding
- Real-time modifications
- Personalized assistance

### **✅ Complete Booking Flow**
- Curated itineraries
- Multiple booking links
- Direct vendor integration
- End-to-end travel planning

### **✅ User Authentication**
- Guest browsing
- Logged-in customization
- Saved preferences
- Personalized experience

---

## 📱 FRONTEND COMPONENTS NEEDED

### **Landing Page**
- Search bar component
- Image carousel
- Flowchart/explanation section
- Chatbot popup

### **Search Results**
- Destination cards grid
- Price display components
- Filter/sort options
- Pagination

### **Destination Detail Page**
- Image gallery
- Cost breakdown display
- Activity listing
- Booking link buttons
- Itinerary view

### **Chatbot UI**
- Floating popup
- Chat window
- Message input
- AI response display
- Typing indicators

### **Authentication**
- Login form
- Sign up form
- User profile
- Guest mode indicator

---

## 🔧 BACKEND INTEGRATION POINTS

### **Current Backend Already Supports:**
✅ AI chat endpoint (`/chat`)
✅ Destination discovery (`/discover-destinations`)
✅ Itinerary generation (`/generate-itineraries`)
✅ Cost calculations (flight, hotel, activities)
✅ Real-time pricing
✅ Booking links
✅ Activity recommendations

### **Ready for Frontend:**
✅ All APIs implemented
✅ Real-time data available
✅ AI processing ready
✅ Booking links provided

---

## 🚀 IMPLEMENTATION PRIORITY

### **Phase 1: Core Experience**
1. Landing page with search
2. Top 10 destinations display
3. Basic chatbot integration

### **Phase 2: Details & Customization**
1. Destination detail pages
2. Dynamic itinerary modification
3. Enhanced chatbot features

### **Phase 3: Authentication & Booking**
1. User login/signup
2. Guest vs logged-in modes
3. Booking integration

---

## 📝 ADDITIONAL NOTES

- Images should come from Google Places API
- Pricing should be real-time from backend
- Chatbot should feel natural and conversational
- Itinerary modifications should be instant
- Booking links should be from multiple vendors
- Guest mode should have clear limitations
- Logged-in mode should enable full customization
