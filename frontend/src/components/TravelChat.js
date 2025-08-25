import React, { useState, useRef, useEffect } from 'react';
import { Send, MapPin, Calendar, DollarSign, Plane, Sparkles, X } from 'lucide-react';
// import axios from 'axios'; // Will be used when backend is connected

const TravelChat = ({ onClose, onRecommendationsReady }) => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);
  const [travelData, setTravelData] = useState({
    destination: '',
    budget: '',
    travelDates: '',
    currentLocation: '',
    preferences: '',
    currency: 'USD',
    travelType: 'international'
  });
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Initialize chat with welcome message
    setMessages([
      {
        id: 1,
        type: 'bot',
        content: "Hi! I'm your AI travel assistant. Let me help you find your perfect destination! 🌍",
        timestamp: new Date()
      },
      {
        id: 2,
        type: 'bot',
        content: "First, tell me about the type of place you want to visit. For example: 'beach', 'mountains', 'city', 'adventure', 'relaxing', etc.",
        timestamp: new Date()
      }
    ]);
  }, []);

  const steps = [
    {
      question: "What type of destination are you looking for?",
      placeholder: "e.g., beach, mountains, city, adventure, relaxing...",
      icon: <MapPin className="h-5 w-5" />,
      field: 'destination'
    },
    {
      question: "Do you prefer domestic or international travel?",
      placeholder: "Type 'domestic' or 'international'",
      icon: <Plane className="h-5 w-5" />,
      field: 'travelType',
      type: 'choice',
      options: ['domestic', 'international']
    },
    {
      question: "What's your budget for this trip?",
      placeholder: "e.g., $1000, $2000-3000, budget-friendly...",
      icon: <DollarSign className="h-5 w-5" />,
      field: 'budget'
    },
    {
      question: "What currency would you prefer?",
      placeholder: "e.g., USD, EUR, GBP, JPY...",
      icon: <DollarSign className="h-5 w-5" />,
      field: 'currency',
      type: 'choice',
      options: ['USD', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD', 'CHF', 'SGD']
    },
    {
      question: "When do you want to travel?",
      placeholder: "e.g., next month, summer 2024, flexible dates...",
      icon: <Calendar className="h-5 w-5" />,
      field: 'travelDates'
    },
    {
      question: "Where are you traveling from?",
      placeholder: "e.g., New York, London, Tokyo...",
      icon: <Plane className="h-5 w-5" />,
      field: 'currentLocation'
    },
    {
      question: "Any other preferences? (optional)",
      placeholder: "e.g., family-friendly, romantic, solo travel, foodie...",
      icon: <Sparkles className="h-5 w-5" />,
      field: 'preferences'
    }
  ];

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputValue,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsTyping(true);

    // Update travel data
    if (currentStep < steps.length) {
      const field = steps[currentStep].field;
      setTravelData(prev => ({
        ...prev,
        [field]: inputValue
      }));
    }

    // Simulate AI response
    setTimeout(() => {
      let botResponse;
      
      if (currentStep < steps.length - 1) {
        // Move to next step
        const nextStep = steps[currentStep + 1];
        botResponse = {
          id: Date.now() + 1,
          type: 'bot',
          content: nextStep.question,
          timestamp: new Date()
        };
        setCurrentStep(prev => prev + 1);
      } else {
        // Final step - generate recommendations
        botResponse = {
          id: Date.now() + 1,
          type: 'bot',
          content: "Perfect! I have all the information I need. Let me find the best destinations for you...",
          timestamp: new Date()
        };
        
        // Simulate processing and then show recommendations
        setTimeout(() => {
          const finalResponse = {
            id: Date.now() + 2,
            type: 'bot',
            content: "I've found some amazing destinations for you! Click below to see your personalized recommendations.",
            timestamp: new Date(),
            showRecommendations: true
          };
          setMessages(prev => [...prev, finalResponse]);
          setIsTyping(false);
        }, 2000);
      }

      setMessages(prev => [...prev, botResponse]);
      setIsTyping(false);
    }, 1000);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleGetRecommendations = () => {
    // Generate mock recommendations
    console.log('Travel Data:', travelData);
    if (onRecommendationsReady) {
      onRecommendationsReady(travelData);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md h-[600px] flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-gray-200">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
              <Sparkles className="h-6 w-6 text-white" />
            </div>
            <div>
              <h3 className="font-semibold text-gray-900">Travel AI Assistant</h3>
              <p className="text-sm text-gray-500">Ask me anything about travel!</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-full transition-colors"
          >
            <X className="h-5 w-5 text-gray-500" />
          </button>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] rounded-2xl px-4 py-3 ${
                  message.type === 'user'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-900'
                }`}
              >
                <p className="text-sm">{message.content}</p>
                {message.showRecommendations && (
                  <button
                    onClick={handleGetRecommendations}
                    className="mt-3 w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium"
                  >
                    View My Recommendations
                  </button>
                )}
              </div>
            </div>
          ))}
          
          {isTyping && (
            <div className="flex justify-start">
              <div className="bg-gray-100 rounded-2xl px-4 py-3">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <div className="p-4 border-t border-gray-200">
          {/* Choice buttons for specific steps */}
          {currentStep < steps.length && steps[currentStep].type === 'choice' && (
            <div className="mb-4">
              <p className="text-sm text-gray-600 mb-3">Choose an option:</p>
              <div className="grid grid-cols-2 gap-2">
                {steps[currentStep].options.map((option) => (
                  <button
                    key={option}
                    onClick={() => {
                      setInputValue(option);
                      handleSendMessage();
                    }}
                    className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors text-sm font-medium"
                  >
                    {option.toUpperCase()}
                  </button>
                ))}
              </div>
            </div>
          )}
          
          <div className="flex space-x-2">
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder={currentStep < steps.length ? steps[currentStep].placeholder : "Type your message..."}
              className="flex-1 px-4 py-3 border border-gray-300 rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              disabled={isTyping}
            />
            <button
              onClick={handleSendMessage}
              disabled={!inputValue.trim() || isTyping}
              className="px-4 py-3 bg-blue-600 text-white rounded-2xl hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
            >
              <Send className="h-5 w-5" />
            </button>
          </div>
          
          {/* Progress indicator */}
          {currentStep < steps.length && (
            <div className="mt-3">
              <div className="flex justify-between text-xs text-gray-500 mb-1">
                <span>Step {currentStep + 1} of {steps.length}</span>
                <span>{Math.round(((currentStep + 1) / steps.length) * 100)}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${((currentStep + 1) / steps.length) * 100}%` }}
                ></div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default TravelChat; 