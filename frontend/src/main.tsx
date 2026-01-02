import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import { loadConfig } from './config';
import './index.css';

/**
 * Bootstrap the React app:
 * 1. Load configuration from config.json
 * 2. Then render the React app
 * 
 * This ensures config is available before any component renders.
 */
async function startApp(): Promise<void> {
    try {
        await loadConfig();
        ReactDOM.createRoot(document.getElementById('root')!).render(<App />);
    } catch (error) {
        console.error('Failed to start app:', error);
        document.getElementById('root')!.innerHTML =
            '<div style="color: red; padding: 20px;">Failed to load configuration</div>';
    }
}

startApp();
