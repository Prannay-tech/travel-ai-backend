import React from 'react';

const DestinationGrid: React.FC = () => {
  const destinations = [
    { name: "Bali, Indonesia", country: "Indonesia", price: "$1,200", type: "Beach" },
    { name: "Swiss Alps", country: "Switzerland", price: "$2,500", type: "Mountain" },
    { name: "Tokyo, Japan", country: "Japan", price: "$2,000", type: "City" },
    { name: "Santorini, Greece", country: "Greece", price: "$2,800", type: "Beach" },
    { name: "Machu Picchu", country: "Peru", price: "$1,800", type: "Historic" },
    { name: "New Zealand", country: "New Zealand", price: "$3,200", type: "Adventure" }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      {destinations.map((destination, index) => (
        <div key={index} className="glass-card p-6 hover:scale-105 transition-transform duration-300 cursor-pointer">
          <h3 className="text-xl font-bold text-white mb-2">{destination.name}</h3>
          <p className="text-white/80 mb-2">{destination.country}</p>
          <div className="flex justify-between items-center">
            <span className="text-teal-primary font-semibold">From {destination.price}</span>
            <span className="text-xs bg-white/20 text-white px-2 py-1 rounded-full">
              {destination.type}
            </span>
          </div>
        </div>
      ))}
    </div>
  );
};

export default DestinationGrid;
