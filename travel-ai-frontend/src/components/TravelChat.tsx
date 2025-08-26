import React from 'react';

interface TravelChatProps {
  isOpen: boolean;
  onClose: () => void;
}

const TravelChat: React.FC<TravelChatProps> = ({ isOpen, onClose }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div className="absolute inset-0 bg-black/50" onClick={onClose} />
      <div className="relative bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-6 max-w-md w-full">
        <h3 className="text-white text-lg font-semibold mb-4">AI Travel Planner</h3>
        <p className="text-white/80 mb-4">Chat interface coming soon!</p>
        <button 
          onClick={onClose}
          className="bg-teal-primary text-white px-4 py-2 rounded-lg"
        >
          Close
        </button>
      </div>
    </div>
  );
};

export default TravelChat;
