# NeuroScent Frontend

Frontend application for NeuroScent perfume affinity platform.

## Tech Stack

- **React 18** with **TypeScript**
- **Vite** - Build tool
- **React Router** - Navigation
- **Framer Motion** - Animations
- **Axios** - API client

## Setup

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment

Create `.env` file:

```bash
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

### 3. Run Development Server

```bash
npm run dev
```

The app will be available at `http://localhost:5173`

## Build for Production

```bash
npm run build
```

Build output will be in `dist/` directory.

## Project Structure

```
frontend/
├── src/
│   ├── components/      # React components
│   ├── pages/          # Page components
│   ├── services/       # API services
│   ├── types/          # TypeScript types
│   ├── utils/          # Utilities
│   ├── App.tsx         # Main app
│   └── main.tsx        # Entry point
├── public/             # Static assets
└── package.json
```

## Available Routes

- `/` - Landing page
- `/test` - Sensory test flow
- `/results/:testId` - Test results

## License

Proprietary - NeuroScent Platform
