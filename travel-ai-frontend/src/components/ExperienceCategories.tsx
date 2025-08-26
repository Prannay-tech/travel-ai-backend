import React from 'react';

const ExperienceCategories: React.FC = () => {
  const experiences = [
    { title: "Mountain Treks", description: "Conquer peaks and explore alpine landscapes" },
    { title: "Guided Tours", description: "Discover hidden gems and local culture" },
    { title: "Photography Expeditions", description: "Capture stunning moments" },
    { title: "Cultural Immersion", description: "Experience authentic local traditions" },
    { title: "Adventure Sports", description: "Thrilling activities for adrenaline seekers" },
    { title: "Wellness Retreats", description: "Rejuvenate your mind and body" }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {experiences.map((experience, index) => (
        <div key={index} className="glass-card p-6 hover:scale-105 transition-transform duration-300">
          <h3 className="text-xl font-semibold text-white mb-2">{experience.title}</h3>
          <p className="text-white/70">{experience.description}</p>
        </div>
      ))}
    </div>
  );
};

export default ExperienceCategories;
