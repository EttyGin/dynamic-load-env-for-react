/**
 * Runtime configuration module
 * 
 * This module loads configuration from a public config.json file at RUNTIME,
 * not at build time. This allows the same React build to be deployed to
 * multiple environments by simply changing the config.json file.
 * 
 * Key principle: config.json is NOT bundled into the React build.
 * It's served as a static file, loaded after the app starts.
 */

let config = null;

/**
 * Fetches config.json from the public folder.
 * This happens BEFORE React renders the app.
 */
export async function loadConfig() {
    if (config) {
        return config;
    }

    try {
        const response = await fetch('/config.json');
        if (!response.ok) {
            throw new Error(`Failed to load config.json: ${response.statusText}`);
        }
        config = await response.json();
        return config;
    } catch (error) {
        console.error('Error loading config:', error);
        // Fallback to default if config.json is missing
        config = {
            BACKEND_URL: NaN,
        };
        return config;
    }
}

/**
 * Gets the currently loaded configuration
 */
export function getConfig() {
    if (!config) {
        throw new Error(
            'Config not loaded yet. Make sure loadConfig() was called first.'
        );
    }
    return config;
}
