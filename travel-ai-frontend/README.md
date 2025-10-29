Travel AI Frontend (Next.js 14)

Overview

Next.js 14 app using TypeScript, Tailwind CSS, Framer Motion, Zustand, and React Query. It provides dark-mode UI, a rich search flow, and a comprehensive destination detail experience with image gallery and tabbed content.

Key Pages

- src/app/page.tsx: Landing page with hero, search bar, and background carousel.
- src/app/search/page.tsx: Results grid with filters, sorting, and improved loading/empty states.
- src/app/destination/[id]/page.tsx: Detail page with image modal and tabs: Overview, Activities, Hotels, Restaurants, Flights, Travel Info.

Core Components

- src/components/SearchBar.tsx: Query, origin, budget, date range, travelers, type; quick actions.
- src/components/ImageCarousel.tsx: High-quality rotating hero images with overlays and controls.
- src/components/DestinationCard.tsx: Summary cards for destinations.
- src/components/HowItWorks.tsx: Onboarding steps.
- src/components/TravelChat.tsx: Floating chatbot UI.

Data Layer

- src/lib/api.ts: API client to call FastAPI backend.
- src/hooks/useApi.ts: React Query hooks for destinations, weather, cost-of-living, etc.

Local Development

1. npm install
2. npm run dev

Styling

- Tailwind CSS + custom global utilities in src/styles/globals.css
- Dark mode gradients, glassmorphism, and motion animations

Future Enhancements

- Authentication gating for saved/custom itineraries
- Deep links to booking vendors
- Real live data wiring on detail page (flights/hotels/activities)


