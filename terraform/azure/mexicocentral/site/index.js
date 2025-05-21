// index.js

const express = require('express');
const path = require('path');
const app = express();

// Set the port
const port = 3000;

// Serve static files (like HTML, CSS, JS, etc.)
app.use(express.static(path.join(__dirname, 'public')));

// Create a route for the home page
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});
