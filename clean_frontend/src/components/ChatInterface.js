import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Send, Bot, Loader2, Plane } from 'lucide-react';
import axios from 'axios';

const ChatInterface = ({ setTravelData, setSelectedDestination }) => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);
  const [travelPreferences, setTravelPreferences] = useState({
    budget_per_person: '',
    people_count: '',
    travel_from: '',
    travel_type: '',
    destination_type: '',
    travel_dates: '',
    currency: 'USD',
    additional_preferences: ''
  });
  
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);
  const navigate = useNavigate();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Define the conversation flow
  const conversationFlow = [
    {
      step: 0,
      question: "👋 Hi there! I'm your AI travel companion. What's your budget per person for this trip?",
      suggestions: [
        "$500-1000",
        "$1000-2000", 
        "$2000-3000",
        "$3000+"
      ],
      field: 'budget_per_person'
    },
    {
      step: 1,
      question: "Great! How many people are traveling?",
      suggestions: [
        "1 person",
        "2 people",
        "3-4 people",
        "5+ people"
      ],
      field: 'people_count'
    },
    {
      step: 2,
      question: "Where are you traveling from?",
      suggestions: [
        "New York",
        "Los Angeles",
        "Chicago",
        "Miami",
        "Other"
      ],
      field: 'travel_from'
    },
    {
      step: 3,
      question: "Do you prefer domestic or international travel?",
      suggestions: [
        "🌍 International",
        "🇺🇸 Domestic"
      ],
      field: 'travel_type'
    },
    {
      step: 4,
      question: "What type of destination interests you?",
      suggestions: [
        "🏖️ Beach vacation",
        "⛰️ Mountain adventure",
        "🏙️ City break",
        "🏛️ Historic places",
        "🙏 Religious places",
        "🎯 Adventure trip",
        "🧘 Relaxing getaway"
      ],
      field: 'destination_type'
    },
    {
      step: 5,
      question: "When do you want to travel?",
      suggestions: [
        "Next month",
        "Next 3 months",
        "Next 6 months",
        "Next year"
      ],
      field: 'travel_dates'
    },
    {
      step: 6,
      question: "What currency would you prefer?",
      suggestions: [
        "USD (US Dollar)",
        "EUR (Euro)",
        "GBP (British Pound)",
        "CAD (Canadian Dollar)",
        "AUD (Australian Dollar)"
      ],
      field: 'currency'
    },
    {
      step: 7,
      question: "Any additional preferences? (romantic getaway, family-friendly, etc.)",
      suggestions: [
        "Romantic getaway",
        "Family-friendly",
        "Budget-conscious",
        "Luxury experience",
        "No specific preferences"
      ],
      field: 'additional_preferences'
    }
  ];

  const addMessage = (content, isUser = false) => {
    const newMessage = {
      id: Date.now(),
      content,
      isUser,
      timestamp: new Date().toLocaleTimeString()
    };
    setMessages(prev => [...prev, newMessage]);
  };

  const handleSuggestionClick = (suggestion) => {
    const currentFlow = conversationFlow[currentStep];
    const field = currentFlow.field;
    
    // Update travel preferences
    setTravelPreferences(prev => ({
      ...prev,
      [field]: suggestion
    }));

    // Add user message
    addMessage(suggestion, true);
    setInputValue('');

    // Move to next step or finish
    if (currentStep < conversationFlow.length - 1) {
      setCurrentStep(prev => prev + 1);
      const nextFlow = conversationFlow[currentStep + 1];
      addMessage(nextFlow.question);
    } else {
      // Finish conversation and get recommendations
      finishConversation();
    }
  };

  const finishConversation = async () => {
    setIsTyping(true);
    addMessage("Perfect! Let me find the best destinations for you... 🤔");

    try {
      // Call backend API to get recommendations
      const response = await axios.post('/recommendations', travelPreferences);
      
      if (response.data.success) {
        setTravelData(response.data);
        addMessage("🎉 I found some amazing destinations for you! Let me show you the options.");
        
        // Navigate to destinations page after a short delay
        setTimeout(() => {
          navigate('/destinations');
        }, 2000);
      } else {
        addMessage("Sorry, I couldn't find destinations matching your preferences. Let's try again!");
      }
    } catch (error) {
      console.error('Error getting recommendations:', error);
      addMessage("I'm having trouble connecting to my travel database. Please try again!");
    } finally {
      setIsTyping(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isTyping) return;

    const userMessage = inputValue.trim();
    addMessage(userMessage, true);
    setInputValue('');

    // If we're in the conversation flow, process the input
    if (currentStep < conversationFlow.length) {
      const currentFlow = conversationFlow[currentStep];
      const field = currentFlow.field;
      
      setTravelPreferences(prev => ({
        ...prev,
        [field]: userMessage
      }));

      if (currentStep < conversationFlow.length - 1) {
        setCurrentStep(prev => prev + 1);
        const nextFlow = conversationFlow[currentStep + 1];
        addMessage(nextFlow.question);
      } else {
        finishConversation();
      }
    } else {
      // Free-form chat with AI
      setIsTyping(true);
      try {
        const response = await axios.post('/chat', {
          message: userMessage,
          conversation_history: messages.map(msg => ({
            role: msg.isUser ? 'user' : 'assistant',
            content: msg.content
          }))
        });
        
        addMessage(response.data.response);
      } catch (error) {
        console.error('Chat error:', error);
        addMessage("I'm having trouble processing your message. Please try again!");
      } finally {
        setIsTyping(false);
      }
    }
  };

  const startConversation = () => {
    setMessages([]);
    setCurrentStep(0);
    setTravelPreferences({
      budget_per_person: '',
      people_count: '',
      travel_from: '',
      travel_type: '',
      destination_type: '',
      travel_dates: '',
      currency: 'USD',
      additional_preferences: ''
    });
    addMessage(conversationFlow[0].question);
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="glass-card overflow-hidden">
        {/* Header */}
        <div className="bg-gradient-to-r from-primary-600/20 to-accent-600/20 px-6 py-4 border-b border-gray-700/50">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-gradient-to-r from-primary-500 to-accent-500 rounded-lg">
              <Bot className="h-6 w-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-100">AI Travel Planner</h1>
              <p className="text-gray-400 text-sm">Let me help you plan your perfect trip!</p>
            </div>
          </div>
        </div>

        {/* Chat Messages */}
        <div className="h-96 overflow-y-auto p-6 space-y-4">
          {messages.length === 0 ? (
            <div className="text-center py-12">
              <div className="relative inline-block mb-4">
                <div className="p-4 bg-gradient-to-r from-primary-500/20 to-accent-500/20 rounded-full border border-primary-500/30 float-animation">
                  <Plane className="h-12 w-12 text-primary-400" />
                </div>
                <div className="absolute -top-1 -right-1 w-4 h-4 bg-accent-500 rounded-full pulse-glow"></div>
              </div>
              <h3 className="text-lg font-medium text-gray-100 mb-2">Ready to plan your trip?</h3>
              <p className="text-gray-400 mb-6">I'll help you find the perfect destination based on your preferences.</p>
              <button
                onClick={startConversation}
                className="modern-btn"
              >
                Start Planning
              </button>
            </div>
          ) : (
            messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.isUser ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                    message.isUser
                      ? 'bg-gradient-to-r from-primary-500 to-accent-500 text-white'
                      : 'glass-card text-gray-100'
                  }`}
                >
                  <p className="text-sm">{message.content}</p>
                  <p className={`text-xs mt-1 ${message.isUser ? 'text-primary-100' : 'text-gray-500'}`}>
                    {message.timestamp}
                  </p>
                </div>
              </div>
            ))
          )}

          {/* Suggestions */}
          {currentStep < conversationFlow.length && messages.length > 0 && !isTyping && (
            <div className="flex flex-wrap gap-2 mt-4">
              {conversationFlow[currentStep].suggestions.map((suggestion, index) => (
                <button
                  key={index}
                  onClick={() => handleSuggestionClick(suggestion)}
                  className="glass-card border border-gray-600/50 text-gray-300 px-3 py-2 rounded-lg text-sm hover:bg-primary-500/20 hover:border-primary-500/50 hover:text-white transition-all duration-300"
                >
                  {suggestion}
                </button>
              ))}
            </div>
          )}

          {/* Typing indicator */}
          {isTyping && (
            <div className="flex justify-start">
              <div className="glass-card text-gray-300 px-4 py-2 rounded-lg">
                <div className="flex items-center space-x-2">
                  <Loader2 className="h-4 w-4 animate-spin text-primary-400" />
                  <span className="text-sm">AI is thinking...</span>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input Form */}
        <div className="border-t border-gray-700/50 bg-gray-900/20 p-4">
          <form onSubmit={handleSubmit} className="flex space-x-4">
            <input
              ref={inputRef}
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Type your message..."
              className="input-modern flex-1"
              disabled={isTyping}
            />
            <button
              type="submit"
              disabled={!inputValue.trim() || isTyping}
              className="modern-btn disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Send className="h-4 w-4" />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
