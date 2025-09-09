const config = {
    apiBaseUrl: process.env.NODE_ENV === 'production'
        ? 'YOUR_RENDER_API_URL'  // You'll replace this with your Render.com URL
        : 'http://localhost:8000'
};

export default config;
