# TravelAI Frontend

A modern, AI-powered travel planning website with a sophisticated dark theme and glass morphism design.

## 🎨 Design Features

- **Dark Theme**: Sophisticated dark color scheme with teal accents
- **Glass Morphism**: Modern glass card effects with backdrop blur
- **Responsive Design**: Works perfectly on all devices
- **Smooth Animations**: Framer Motion animations for enhanced UX
- **Modern Typography**: Inter font family for clean readability

## 🚀 Features

### Core Components
- **Hero Section**: "TO THE UNKNOWN" with call-to-action buttons
- **Experience Categories**: 6 different travel experience types
- **Destination Grid**: Beautiful destination cards with hover effects
- **AI Chat Interface**: Conversational travel planning with Groq LLM
- **Floating Chat Button**: Always accessible chat interface

### AI Integration
- **Conversational Flow**: Structured conversation to collect travel preferences
- **Real-time Chat**: Live communication with the AI travel planner
- **Session Management**: Persistent conversation state
- **Backend Integration**: Connected to Railway-deployed backend

## 🛠 Tech Stack

- **React 18** with TypeScript
- **Tailwind CSS** for styling
- **Framer Motion** for animations
- **Heroicons** for icons
- **Axios** for API calls

## 🎯 Color Palette

- **Primary Dark**: `#1a1a2e`
- **Secondary Dark**: `#16213e`
- **Tertiary Dark**: `#0f3460`
- **Teal Primary**: `#00d4ff`
- **Teal Secondary**: `#08d9d6`
- **Glass Effect**: `rgba(255, 255, 255, 0.1)`

## 📱 Responsive Design

- **Mobile First**: Optimized for mobile devices
- **Tablet**: Responsive grid layouts
- **Desktop**: Full-width layouts with enhanced spacing
- **Large Screens**: Maximum content width for readability

## 🎭 Animations

- **Page Load**: Fade-in animations for sections
- **Scroll Animations**: Elements animate as they come into view
- **Hover Effects**: Scale and color transitions
- **Chat Interface**: Smooth modal transitions
- **Floating Button**: Continuous floating animation

## 🔧 Getting Started

1. **Install Dependencies**:
   ```bash
   npm install
   ```

2. **Start Development Server**:
   ```bash
   npm start
   ```

3. **Build for Production**:
   ```bash
   npm run build
   ```

## 🌐 Backend Integration

The frontend connects to the Railway-deployed backend at:
`https://web-production-b058.up.railway.app`

### API Endpoints Used:
- `POST /chat` - AI conversation endpoint
- `POST /recommendations` - Destination recommendations
- `POST /flights` - Flight search
- `POST /hotels` - Hotel search

## 🎨 Design Inspiration

Based on modern travel agency designs with:
- **Barcelle Travel Agency** aesthetic
- **Morii Adventure** color scheme
- **Glass morphism** effects
- **Dark mode** sophistication

## 📁 Project Structure

```
src/
├── components/
│   ├── TravelChat.tsx      # AI chat interface
│   ├── ExperienceCategories.tsx  # Experience cards
│   └── DestinationGrid.tsx # Destination gallery
├── App.tsx                 # Main application
├── index.css              # Global styles
└── index.tsx              # Entry point
```

## 🚀 Deployment

Ready for deployment on:
- **Vercel** (recommended)
- **Netlify**
- **GitHub Pages**

## 🔮 Future Enhancements

- [ ] Booking interface integration
- [ ] User authentication
- [ ] Saved trips feature
- [ ] Real-time flight/hotel data
- [ ] Weather integration
- [ ] Multi-language support
