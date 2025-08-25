# Prompt Engineering Guide for Travel AI

This guide shows you exactly where to customize the AI prompts and model parameters for optimal travel planning conversations.

## 🔑 **Step 1: Add Your Groq API Key**

### **Where to add the API key:**
File: `clean_backend/.env`

```bash
# Replace "your-groq-api-key-here" with your actual Groq API key
GROQ_API_KEY=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
```

### **How to get a Groq API key:**
1. Visit https://console.groq.com/
2. Sign up for a free account
3. Generate your API key
4. Copy the key and paste it in the `.env` file

## 🎯 **Step 2: Customize the AI System Prompt**

### **Location:** `clean_backend/main.py` (lines 75-90)

The main system prompt is defined in the `AI_SYSTEM_PROMPT` variable. Here's the current prompt:

```python
AI_SYSTEM_PROMPT = """
You are an expert AI travel planner. Your job is to help users plan their perfect trip by extracting their travel preferences from natural language conversations.

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

Always respond in a friendly, helpful manner. If you need more information, ask specific questions.
"""
```

### **Customization Examples:**

#### **Enhanced Travel Expert Prompt:**
```python
AI_SYSTEM_PROMPT = """
You are TravelGPT, an expert AI travel consultant with 20+ years of experience in luxury and budget travel planning. You specialize in creating personalized travel experiences that match each client's unique preferences and budget. Your job is to make travel planning and booking as easy as possible, suggesting them places to travel, activities to do there and special seasons and festivals that are a must see in all the places ( eg. St. Patricks day in chicago, Tomatino Festival in Spain , and other events that only happen on specific dates at the locations)

Your expertise includes:
- Luxury travel and exclusive experiences
- Budget-friendly travel planning
- Family vacation coordination
- Solo travel and adventure planning
- Cultural immersion experiences
- Food and culinary tourism
- Wellness and spa retreats

Key responsibilities:
1. Extract detailed travel preferences through natural conversation
2. Provide expert travel advice and insider tips
3. Suggest unique experiences and hidden gems
4. Consider seasonal factors and local events
5. Offer practical travel tips and safety advice

Travel preference categories to extract:
- Budget per person (with currency preference)
- Number and type of travelers (solo, couple, family, group)
- Departure location and travel type (domestic/international)
- Destination preferences (beach, mountain, city, historic, religious, adventure, relaxing)
- Travel dates and duration
- Special interests (food, culture, adventure, relaxation, shopping)
- Accessibility requirements
- Dietary restrictions
- Accommodation preferences (luxury, boutique, budget, unique)

Communication style:
- Warm, enthusiastic, and professional
- Use travel-specific terminology naturally
- Share personal insights and recommendations
- Ask follow-up questions to understand preferences better
- Provide context about destinations and experiences
"""
```

#### **Budget-Focused Prompt:**
```python
AI_SYSTEM_PROMPT = """
You are BudgetTravelBot, an AI travel planner specializing in affordable travel experiences. You help travelers find amazing destinations and experiences within their budget constraints.

Your specialties:
- Budget-friendly destination recommendations
- Money-saving travel tips and hacks
- Off-season travel planning
- Alternative accommodation options
- Local transportation advice
- Free and low-cost activities
- Meal planning on a budget

Key responsibilities:
1. Help users maximize their travel budget
2. Suggest affordable alternatives to expensive destinations
3. Provide money-saving tips and strategies
4. Recommend budget-friendly activities and experiences
5. Guide users through cost-effective travel planning

Always consider:
- Total trip cost (flights, accommodation, food, activities, transportation)
- Seasonal price variations
- Alternative airports and routes
- Local currency and exchange rates
- Budget-friendly accommodation options
- Free activities and attractions
- Local transportation passes and deals
"""
```

## ⚙️ **Step 3: Customize Model Parameters**

### **Location:** `clean_backend/main.py` (lines 230-240)

The model parameters are in the `call_groq_ai` function:

```python
json={
    "model": "llama3-70b-8192",        # Model selection
    "messages": messages,              # Conversation history
    "temperature": 0.3,                # Creativity level (0.0-1.0)
    "max_tokens": 800,                 # Response length limit
    "top_p": 0.8,                     # Response diversity (0.0-1.0)
    "frequency_penalty": 0.1,         # Reduce repetition
    "presence_penalty": 0.1           # Encourage new topics
}
```

### **Parameter Explanations:**

#### **Model Selection:**
- `"llama3-70b-8192"` - Most capable model (recommended)
- `"llama3-8b-8192"` - Faster, lighter model
- `"mixtral-8x7b-32768"` - Good balance of speed and capability

#### **Temperature (0.0-1.0):**
- `0.0` - Very focused, consistent responses
- `0.3` - Balanced creativity and consistency (current)
- `0.7` - More creative, varied responses
- `1.0` - Maximum creativity

#### **Max Tokens:**
- `400` - Short, concise responses
- `800` - Medium-length responses (current)
- `1200` - Longer, detailed responses
- `2000` - Very detailed responses

#### **Top P (0.0-1.0):**
- `0.5` - More focused responses
- `0.8` - Balanced diversity (current)
- `1.0` - Maximum diversity

### **Recommended Configurations:**

#### **For Professional Travel Planning:**
```python
json={
    "model": "llama3-70b-8192",
    "messages": messages,
    "temperature": 0.2,        # More focused
    "max_tokens": 1000,        # Detailed responses
    "top_p": 0.7,             # Balanced diversity
    "frequency_penalty": 0.2,  # Reduce repetition
    "presence_penalty": 0.1
}
```

#### **For Creative Travel Inspiration:**
```python
json={
    "model": "llama3-70b-8192",
    "messages": messages,
    "temperature": 0.6,        # More creative
    "max_tokens": 1200,        # Longer responses
    "top_p": 0.9,             # More diverse
    "frequency_penalty": 0.1,
    "presence_penalty": 0.2    # Encourage new topics
}
```

#### **For Fast, Concise Responses:**
```python
json={
    "model": "llama3-8b-8192",  # Faster model
    "messages": messages,
    "temperature": 0.3,
    "max_tokens": 500,          # Shorter responses
    "top_p": 0.8,
    "frequency_penalty": 0.1,
    "presence_penalty": 0.1
}
```

## 🎨 **Step 4: Customize Conversation Flow**

### **Location:** `clean_frontend/src/components/ChatInterface.js`

You can customize the conversation flow by modifying the `conversationFlow` array:

```javascript
const conversationFlow = [
    {
        step: 0,
        question: "👋 Hi there! I'm your AI travel companion. What's your budget per person for this trip?",
        suggestions: ["$500-1000", "$1000-2000", "$2000-3000", "$3000+"],
        field: 'budget_per_person'
    },
    // ... more steps
];
```

### **Customization Examples:**

#### **Luxury Travel Flow:**
```javascript
const conversationFlow = [
    {
        step: 0,
        question: "🌟 Welcome to Luxury Travel Planning! What's your preferred budget range for this exclusive experience?",
        suggestions: ["$5000-10000", "$10000-20000", "$20000-50000", "$50000+"],
        field: 'budget_per_person'
    },
    {
        step: 1,
        question: "How many guests will be traveling?",
        suggestions: ["1 (Solo Luxury)", "2 (Romantic Getaway)", "3-4 (Family Luxury)", "5+ (Group Experience)"],
        field: 'people_count'
    }
];
```

#### **Adventure Travel Flow:**
```javascript
const conversationFlow = [
    {
        step: 0,
        question: "🏔️ Ready for an adventure? What's your adventure budget per person?",
        suggestions: ["$1000-2000", "$2000-4000", "$4000-8000", "$8000+"],
        field: 'budget_per_person'
    },
    {
        step: 1,
        question: "How many adventure seekers in your group?",
        suggestions: ["1 (Solo Adventure)", "2 (Adventure Duo)", "3-4 (Adventure Squad)", "5+ (Expedition Team)"],
        field: 'people_count'
    }
];
```

## 🧪 **Step 5: Testing Your Prompts**

### **Test the AI Chat:**
1. Add your Groq API key to `.env`
2. Restart the backend: `python main.py`
3. Visit http://localhost:3000/chat
4. Test different conversation scenarios

### **Test API Directly:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I want to plan a romantic getaway for 2 people with a budget of $3000-5000",
    "conversation_history": []
  }'
```

## 📊 **Step 6: Monitor and Optimize**

### **Track Performance:**
- Monitor response quality and relevance
- Check for consistent preference extraction
- Evaluate user satisfaction
- Monitor API usage and costs

### **Iterative Improvement:**
1. Test different prompts
2. Adjust model parameters
3. Refine conversation flow
4. Gather user feedback
5. Optimize based on results

## 🎯 **Quick Start Checklist**

- [ ] Get Groq API key from https://console.groq.com/
- [ ] Add API key to `clean_backend/.env`
- [ ] Customize `AI_SYSTEM_PROMPT` in `main.py`
- [ ] Adjust model parameters if needed
- [ ] Test the chat interface
- [ ] Iterate and improve based on results

## 💡 **Pro Tips**

1. **Start Simple**: Begin with the basic prompt and gradually enhance
2. **Test Extensively**: Try various user scenarios and edge cases
3. **Monitor Costs**: Keep track of API usage to stay within limits
4. **User Feedback**: Gather feedback to improve the experience
5. **A/B Testing**: Test different prompts with real users

---

**Remember**: The key to great prompt engineering is iteration and testing. Start with the basic setup and gradually refine based on how the AI performs with real users!
