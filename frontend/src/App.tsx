import React, { useEffect, useState } from 'react';
import { getConfig } from './config';

/**
 * App component that fetches and displays the backend response
 */
function App(): React.ReactElement {
    const [message, setMessage] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState<boolean>(true);
    const [backendUrl, setBackendUrl] = useState<string>('');

    useEffect(() => {
        // Fetch message from backend using the configured URL
        async function fetchMessage(): Promise<void> {
            try {
                const config = getConfig();
                setBackendUrl(config.BACKEND_URL);

                const response = await fetch(`${config.BACKEND_URL}/api/hello`);
                if (!response.ok) {
                    throw new Error(`Backend error: ${response.statusText}`);
                }
                const data = await response.json();
                setMessage(data.message);
            } catch (err) {
                setError(err instanceof Error ? err.message : 'Unknown error');
            } finally {
                setLoading(false);
            }
        }

        fetchMessage();
    }, []);

    if (loading) {
        return <div className="container">Loading...</div>;
    }

    return (
        <div className="container">
            <h1>Build Once, Deploy Many 🚀</h1>

            <div className="config-info">
                <h2>Runtime Configuration</h2>
                <p>
                    <strong>Backend URL:</strong> <code>{backendUrl}</code>
                </p>
                <p className="explanation">
                    This URL comes from <code>config.json</code>, loaded at runtime.
                    <br />
                    The React build itself contains NO hardcoded backend URL.
                </p>
            </div>

            <div className="response-section">
                <h2>Backend Response</h2>
                {error ? (
                    <div className="error">❌ Error: {error}</div>
                ) : (
                    <div className="success">
                        ✅ Message from backend: <strong>{message}</strong>
                    </div>
                )}
            </div>

            <div className="explanation-box">
                <h3>Why This Works</h3>
                <ul>
                    <li>
                        <strong>Build:</strong> React is built once with `npm run build`
                    </li>
                    <li>
                        <strong>Runtime:</strong> On app start, JavaScript fetches
                        <code>config.json</code> (a static file, NOT bundled)
                    </li>
                    <li>
                        <strong>Dynamic:</strong> Change <code>config.json</code> to point
                        to different backends without rebuilding React
                    </li>
                    <li>
                        <strong>Same Build:</strong> One React build works with any backend
                        URL
                    </li>
                </ul>
            </div>
        </div>
    );
}

export default App;
