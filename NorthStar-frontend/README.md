# NorthStar Retail Frontend

A modern React + Vite frontend application for NorthStar retail customer support. This application provides customers with quick access to order tracking, return management, and real-time stock checking.

## Features

- **Order Tracking**: Look up and track order status in real-time
- **Return Management**: Initiate and manage product returns with an intuitive wizard interface
- **Stock Checking**: Check product availability across inventory
- **Session Management**: Persistent user sessions for seamless experience
- **Responsive Design**: Works across desktop and mobile devices
- **Real-time Notifications**: Modal alerts for order updates and system messages

## Tech Stack

- **React 19.2.8** - UI framework
- **Vite 8.2.0** - Build tool and dev server with HMR
- **ESLint** - Code quality and linting
- **dotenv 17.4.2** - Environment variable management

## Prerequisites

- Node.js (v16 or higher)
- pnpm (v8 or higher) - recommended package manager

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd NorthStar-frontend
```

2. Install dependencies:
```bash
pnpm install
```

3. Create a `.env` file in the root directory with necessary environment variables:
```env
VITE_API_BASE=/api
```

## Development

Start the development server with hot module replacement:

```bash
pnpm dev
```

The application will be available at `http://localhost:5173`

## Building

Create an optimized production build:

```bash
pnpm build
```

Output files will be generated in the `dist/` directory.

## Preview

Preview the production build locally:

```bash
pnpm preview
```

## Linting

Run ESLint to check code quality:

```bash
pnpm lint
```

## Project Structure

```
src/
├── components/          # Reusable React components
│   ├── common/         # Shared UI components (modals, skeletons, notices)
│   ├── inventory/      # Inventory-related components (stock checker)
│   ├── layout/         # Layout components (header, navigation)
│   ├── orders/         # Order-related components (status lookup, progress)
│   └── returns/        # Return-related components (wizard, receipt)
├── pages/              # Page components (Home, Orders, Inventory, Returns)
├── services/           # API services and business logic
│   ├── api.js         # Core API client
│   ├── inventoryService.js
│   ├── orderService.js
│   ├── returnService.js
│   └── sessionService.js
├── context/            # React context for state management
│   └── SessionContext.jsx
├── utils/              # Utility functions
│   ├── constants.js
│   ├── formatters.js
│   └── validators.js
├── assets/             # Static assets (images, icons)
├── App.jsx             # Main App component
├── main.jsx            # Entry point
└── index.css           # Global styles
```

## Key Components

### Pages
- **Home**: Main landing page with navigation to order tracking, returns, and stock checking
- **Orders**: Order status lookup interface
- **Returns**: Return management wizard and processing
- **Inventory**: Real-time stock availability checker

### Services
- **api.js**: Base API client with request/response handling
- **orderService.js**: Order-related API calls
- **returnService.js**: Return processing and tracking
- **inventoryService.js**: Stock and inventory queries
- **sessionService.js**: User session management

### Utilities
- **formatters.js**: Data formatting functions (dates, currency, etc.)
- **validators.js**: Input validation and error checking
- **constants.js**: Application-wide constants

## Environment Variables

Configure the following in your `.env` file:

| Variable | Description | Example |
|----------|-------------|---------|
| `VITE_API_BASE` | Base URL for API requests | `/api` |

## Available Scripts

| Command | Description |
|---------|-------------|
| `pnpm dev` | Start development server with HMR |
| `pnpm build` | Create production build |
| `pnpm preview` | Preview production build |
| `pnpm lint` | Run ESLint checks |

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)

## Contributing

1. Create a feature branch (`git checkout -b feature/amazing-feature`)
2. Commit changes (`git commit -m 'Add amazing feature'`)
3. Push to branch (`git push origin feature/amazing-feature`)
4. Open a Pull Request

## Code Quality

This project uses ESLint to maintain code quality. Run `pnpm lint` before committing code to catch potential issues.

## Performance

- Vite's fast development server with HMR for quick iterations
- Production builds are optimized and minified
- React 19 with improved performance features

## Troubleshooting

### Port already in use
If port 5173 is already in use, Vite will automatically use the next available port.

### API connection issues
Ensure the `VITE_API_BASE_URL` environment variable is correctly set and the backend API is running.

### Module resolution errors
Clear the node_modules and reinstall:
```bash
rm -rf node_modules pnpm-lock.yaml
pnpm install
```

## License

[Add your license here]

## Support

For issues and support, please contact the development team or create an issue in the repository.
