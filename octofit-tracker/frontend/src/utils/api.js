/**
 * Builds the API base URL based on the environment
 * @returns {string} The base API URL
 */
export const getApiBaseUrl = () => {
  const codespaceName = process.env.REACT_APP_CODESPACE_NAME;
  
  if (codespaceName) {
    return `https://${codespaceName}-8000.app.github.dev/api`;
  }
  
  // Fallback to localhost for local development
  return 'http://localhost:8000/api';
};

/**
 * Builds a full API URL for a given endpoint
 * @param {string} endpoint - The API endpoint (e.g., 'users/', 'teams/')
 * @returns {string} The full API URL
 */
export const getApiUrl = (endpoint) => {
  const baseUrl = getApiBaseUrl();
  // Remove any leading slashes from endpoint to avoid double slashes
  const cleanEndpoint = endpoint.replace(/^\/+/, '');
  return `${baseUrl}/${cleanEndpoint}`;
};
