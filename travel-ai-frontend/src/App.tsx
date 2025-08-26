import React, { useState } from 'react';

function App() {
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [messages, setMessages] = useState([
    { id: 1, text: "Hi! I'm your AI travel planner. Where would you like to go?", isAI: true }
  ]);
  const [inputMessage, setInputMessage] = useState('');

  const handleSendMessage = () => {
    if (inputMessage.trim()) {
      const newMessage = { id: Date.now(), text: inputMessage, isAI: false };
      setMessages([...messages, newMessage]);
      setInputMessage('');
      
      // Simulate AI response
      setTimeout(() => {
        const aiResponse = { id: Date.now() + 1, text: "I'm working on finding the perfect destinations for you! This feature will be connected to our AI backend soon.", isAI: true };
        setMessages(prev => [...prev, aiResponse]);
      }, 1000);
    }
  };

  const processSteps = [
    {
      step: 1,
      title: "Tell Me About Your Trip",
      description: "Share your preferences, budget, and travel style",
      icon: "💬"
    },
    {
      step: 2,
      title: "AI Analyzes & Recommends",
      description: "Our AI finds perfect destinations based on your needs",
      icon: "🤖"
    },
    {
      step: 3,
      title: "Explore Options",
      description: "Browse flights, hotels, and activities",
      icon: "✈️"
    },
    {
      step: 4,
      title: "Book & Enjoy",
      description: "Secure your trip and start your adventure",
      icon: "🎉"
    }
  ];

  return (
    <div className="min-h-screen relative overflow-hidden">
      {/* Background Image */}
      <div 
        className="absolute inset-0 bg-cover bg-center bg-no-repeat"
        style={{
          backgroundImage: "url('https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80')"
        }}
      >
        {/* Overlay */}
        <div className="absolute inset-0 bg-black/40"></div>
      </div>

      {/* Content */}
      <div className="relative z-10 min-h-screen flex flex-col">
        {/* Header */}
        <header className="p-6">
          <div className="max-w-7xl mx-auto flex justify-between items-center">
            <div className="text-white">
              <h1 className="text-3xl font-bold">TravelAI</h1>
              <p className="text-white/80">Your AI-Powered Travel Companion</p>
            </div>
            <button 
              onClick={() => setIsChatOpen(true)}
              className="bg-teal-500 hover:bg-teal-600 text-white px-6 py-3 rounded-lg font-semibold transition-colors"
            >
              Start Planning
            </button>
          </div>
        </header>

        {/* Hero Section */}
        <main className="flex-1 flex items-center justify-center px-6">
          <div className="text-center text-white max-w-4xl">
            <h2 className="text-5xl md:text-7xl font-bold mb-6">
              Plan Your Perfect Trip
            </h2>
            <p className="text-xl md:text-2xl mb-8 text-white/90">
              Let AI guide you to unforgettable destinations
            </p>
            <button 
              onClick={() => setIsChatOpen(true)}
              className="bg-teal-500 hover:bg-teal-600 text-white px-8 py-4 rounded-lg text-xl font-semibold transition-colors shadow-lg"
            >
              Chat with AI Travel Planner
            </button>
          </div>
        </main>

        {/* Process Chart */}
        <section className="py-20 px-6 bg-white/10 backdrop-blur-sm">
          <div className="max-w-6xl mx-auto">
            <h3 className="text-4xl font-bold text-white text-center mb-16">
              How It Works
            </h3>
            <div className="grid md:grid-cols-4 gap-8">
              {processSteps.map((step, index) => (
                <div key={step.step} className="text-center">
                  <div className="relative">
                    <div className="w-20 h-20 bg-teal-500 rounded-full flex items-center justify-center text-3xl mx-auto mb-4">
                      {step.icon}
                    </div>
                    {index < processSteps.length - 1 && (
                      <div className="hidden md:block absolute top-10 left-full w-full h-0.5 bg-teal-500/30 transform translate-x-4"></div>
                    )}
                  </div>
                  <h4 className="text-xl font-semibold text-white mb-2">
                    {step.title}
                  </h4>
                  <p className="text-white/80">
                    {step.description}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </section>
      </div>

      {/* Chat Interface */}
      {isChatOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          <div className="absolute inset-0 bg-black/50" onClick={() => setIsChatOpen(false)}></div>
          <div className="relative bg-white rounded-xl shadow-2xl w-full max-w-md h-[600px] flex flex-col">
            {/* Chat Header */}
            <div className="bg-teal-500 text-white p-4 rounded-t-xl">
              <div className="flex justify-between items-center">
                <h3 className="text-lg font-semibold">AI Travel Planner</h3>
                <button 
                  onClick={() => setIsChatOpen(false)}
                  className="text-white hover:text-gray-200"
                >
                  ✕
                </button>
              </div>
            </div>

            {/* Chat Messages */}
            <div className="flex-1 p-4 overflow-y-auto space-y-4">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${message.isAI ? 'justify-start' : 'justify-end'}`}
                >
                  <div
                    className={`max-w-xs px-4 py-2 rounded-lg ${
                      message.isAI
                        ? 'bg-gray-100 text-gray-800'
                        : 'bg-teal-500 text-white'
                    }`}
                  >
                    {message.text}
                  </div>
                </div>
              ))}
            </div>

            {/* Chat Input */}
            <div className="p-4 border-t">
              <div className="flex space-x-2">
                <input
                  type="text"
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                  placeholder="Type your message..."
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500"
                />
                <button
                  onClick={handleSendMessage}
                  className="bg-teal-500 text-white px-4 py-2 rounded-lg hover:bg-teal-600 transition-colors"
                >
                  Send
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
