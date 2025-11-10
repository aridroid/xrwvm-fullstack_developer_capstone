// app.js
const express = require('express');
const cors = require('cors');
const morgan = require('morgan');
const path = require('path');

const dealershipRoutes = require('./dealership');
const reviewRoutes = require('./review');
// optional route - require only if the file exists
let inventoryRoutes = null;
try {
  inventoryRoutes = require('./inventory');
} catch (err) {
  // inventory is optional — log and continue
  console.warn('Optional route "inventory.js" not found. Skipping inventory routes.');
}

const app = express();
const PORT = process.env.PORT || 3000;

// middleware
app.use(cors());                 // allow cross-origin (Django / React calls)
app.use(morgan('dev'));          // request logging in dev
app.use(express.json());         // parse JSON bodies

// routes
app.use('/', dealershipRoutes);  // /fetchDealers, /fetchDealer/:id, /fetchDealers/state/:state
app.use('/', reviewRoutes);      // /fetchReviews, /fetchReviews/dealer/:id, etc.
if (inventoryRoutes) {
  app.use('/', inventoryRoutes); // optional, only if file exists
}

// simple health
app.get('/ping', (req, res) => res.json({ status: 'ok' }));

// 404 for unknown routes (JSON)
app.use((req, res, next) => {
  res.status(404).json({ error: 'Not found' });
});

// basic error handler (returns JSON)
app.use((err, req, res, next) => {
  console.error('Server error:', err && err.stack ? err.stack : err);
  res.status(err.status || 500).json({ error: 'Server error' });
});

app.listen(PORT, () => {
  console.log(`Dealers API listening on http://localhost:${PORT}`);
});
