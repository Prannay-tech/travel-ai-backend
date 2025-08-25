import React from 'react';
import { Link } from 'react-router-dom';
import { Plane, Bot, MapPin, Calendar, Star, Zap } from 'lucide-react';

const Home = () => {
  const features = [
    {
      icon: Bot,
      title: "AI-Powered Planning",
      description: "Intelligent travel recommendations based on your preferences and budget"
    },
    {
      icon: MapPin,
      title: "Smart Destinations",
      description: "Discover perfect destinations from beaches to mountains to historic cities"
    },
    {
      icon: Calendar,
      title: "Complete Booking",
      description: "Book flights, hotels, and activities all in one place"
    },
    {
      icon: Star,
      title: "Personalized Experience",
      description: "Get recommendations tailored to your travel style and interests"
    }
  ];

  return (
    <div className="max-w-6xl mx-auto">
      {/* Hero Section */}
      <div className="text-center py-16 animate-fade-in-up">
        <div className="mb-8">
          <div className="relative inline-block mb-6">
            <div className="p-6 bg-gradient-to-r from-primary-500/20 to-accent-500/20 rounded-full border border-primary-500/30 float-animation">
              <Plane className="h-20 w-20 text-primary-400" />
            </div>
            <div className="absolute -top-2 -right-2 w-6 h-6 bg-accent-500 rounded-full pulse-glow"></div>
          </div>
          <h1 className="text-5xl md:text-6xl font-bold text-gray-100 mb-4">
            Plan Your Perfect Trip with
            <span className="gradient-text"> AI</span>
          </h1>
          <p className="text-xl text-gray-300 mb-8 max-w-3xl mx-auto leading-relaxed">
            Let our intelligent travel assistant help you discover amazing destinations, 
            find the best deals, and plan every detail of your journey.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/chat"
              className="modern-btn flex items-center justify-center space-x-2 text-lg"
            >
              <Bot className="h-5 w-5" />
              <span>Start Planning</span>
            </Link>
            <Link
              to="/destinations"
              className="glass-card border border-primary-500/30 text-primary-300 px-8 py-4 rounded-lg text-lg font-semibold hover:bg-primary-500/10 hover:border-primary-400/50 transition-all duration-300 flex items-center justify-center space-x-2"
            >
              <MapPin className="h-5 w-5" />
              <span>Browse Destinations</span>
            </Link>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-16">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-100 mb-4">
            Why Choose <span className="gradient-text">Travel AI</span>?
          </h2>
          <p className="text-gray-300 max-w-2xl mx-auto text-lg">
            Our AI-powered platform makes travel planning effortless and personalized
          </p>
        </div>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8 px-8">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <div key={index} className="text-center group">
                <div className="glass-card p-6 mb-4 group-hover:scale-105 transition-transform duration-300">
                  <div className="bg-gradient-to-r from-primary-500/20 to-accent-500/20 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:glow-on-hover">
                    <Icon className="h-8 w-8 text-primary-400" />
                  </div>
                  <h3 className="text-xl font-semibold text-gray-100 mb-2">
                    {feature.title}
                  </h3>
                  <p className="text-gray-400 leading-relaxed">
                    {feature.description}
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* How It Works */}
      <div className="py-16">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-100 mb-4">
            How It Works
          </h2>
          <p className="text-gray-300 text-lg">
            Get from idea to booking in just a few simple steps
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          <div className="text-center group">
            <div className="glass-card p-6 mb-4 group-hover:scale-105 transition-transform duration-300">
              <div className="bg-gradient-to-r from-primary-500 to-accent-500 text-white w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold">
                1
              </div>
              <h3 className="text-xl font-semibold text-gray-100 mb-2">
                Chat with AI
              </h3>
              <p className="text-gray-400">
                Tell our AI assistant about your preferences, budget, and travel style
              </p>
            </div>
          </div>
          
          <div className="text-center group">
            <div className="glass-card p-6 mb-4 group-hover:scale-105 transition-transform duration-300">
              <div className="bg-gradient-to-r from-primary-500 to-accent-500 text-white w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold">
                2
              </div>
              <h3 className="text-xl font-semibold text-gray-100 mb-2">
                Get Recommendations
              </h3>
              <p className="text-gray-400">
                Receive personalized destination suggestions that match your criteria
              </p>
            </div>
          </div>
          
          <div className="text-center group">
            <div className="glass-card p-6 mb-4 group-hover:scale-105 transition-transform duration-300">
              <div className="bg-gradient-to-r from-primary-500 to-accent-500 text-white w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold">
                3
              </div>
              <h3 className="text-xl font-semibold text-gray-100 mb-2">
                Book Everything
              </h3>
              <p className="text-gray-400">
                Book flights, hotels, and activities with our integrated booking system
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="glass-card p-8 text-center text-white border border-primary-500/30">
        <h2 className="text-3xl md:text-4xl font-bold mb-4">
          Ready to Start Your Journey?
        </h2>
        <p className="text-gray-300 mb-6 max-w-2xl mx-auto text-lg">
          Join thousands of travelers who have discovered amazing destinations with our AI-powered platform
        </p>
        <Link
          to="/chat"
          className="modern-btn inline-flex items-center space-x-2 text-lg"
        >
          <Zap className="h-5 w-5" />
          <span>Start Planning Now</span>
        </Link>
      </div>
    </div>
  );
};

export default Home;
