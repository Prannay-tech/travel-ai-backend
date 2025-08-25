import React from 'react';
import { MessageCircle, Sparkles } from 'lucide-react';

const FloatingChatButton = ({ onClick, isVisible = true }) => {
  if (!isVisible) return null;

  return (
    <div className="fixed bottom-6 right-6 z-40">
      <button
        onClick={onClick}
        className="group relative bg-gradient-to-r from-blue-600 to-purple-600 text-white p-4 rounded-full shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-110"
        aria-label="Chat with AI Assistant"
      >
        <MessageCircle className="h-6 w-6" />
        
        {/* Pulse animation */}
        <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full animate-ping opacity-20"></div>
        
        {/* Tooltip */}
        <div className="absolute bottom-full right-0 mb-2 px-3 py-2 bg-gray-900 text-white text-sm rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">
          <div className="flex items-center space-x-2">
            <Sparkles className="h-4 w-4" />
            <span>Chat with AI</span>
          </div>
          <div className="absolute top-full right-4 w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-gray-900"></div>
        </div>
      </button>
    </div>
  );
};

export default FloatingChatButton; 