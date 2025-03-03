# Billionaire Impact Rankings - React UI

This is a React-based frontend for the Billionaire Impact Rankings application.

## Getting Started

### Prerequisites

- Node.js (v14 or later recommended)
- npm or yarn

### Installation

1. Navigate to the react-ui directory:
   ```
   cd react-ui
   ```

2. Install dependencies:
   ```
   npm install
   ```
   or if you use yarn:
   ```
   yarn install
   ```

3. Start the development server:
   ```
   npm start
   ```
   or:
   ```
   yarn start
   ```

The application will be available at http://localhost:3000.

## Project Structure

- `src/components/` - React components
  - `Layout.js` - Main layout component with navigation and footer
  - `Rankings.js` - Displays the billionaire rankings table
  - `Vote.js` - Voting interface for category weights
- `src/api/` - API interaction functions

## Backend Integration

This React UI is designed to work with the existing FastAPI backend. Make sure your backend API is running and accessible.

For development, you may need to set up a proxy in package.json to forward API requests to your backend server.
