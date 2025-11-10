const express = require('express');
const fs = require('fs').promises;
const path = require('path');

const router = express.Router();
const DATA_DIR = path.join(__dirname, 'data');
const DEALERS_FILE = path.join(DATA_DIR, 'dealerships.json');

async function readDealersRaw() {
  const text = await fs.readFile(DEALERS_FILE, 'utf8');
  return JSON.parse(text);             // might be { dealerships: [...] } or an array
}

function dealersArrayFrom(raw) {
  // If file contains { dealerships: [...] } return that array
  if (Array.isArray(raw)) return raw;
  if (raw && Array.isArray(raw.dealerships)) return raw.dealerships;
  // fallback empty array
  return [];
}

// GET /fetchDealers  -> list all dealers (preserve original behavior)
router.get('/fetchDealers', async (req, res) => {
  try {
    const raw = await readDealersRaw();
    return res.json(raw);
  } catch (err) {
    console.error('Error reading dealers:', err);
    return res.status(500).json({ error: 'Could not read dealers' });
  }
});

// GET /fetchDealer/:id -> single dealer by id (robust)
router.get('/fetchDealer/:id', async (req, res) => {
  try {
    const id = Number(req.params.id);
    const raw = await readDealersRaw();
    const dealers = dealersArrayFrom(raw);

    const dealer = dealers.find(d => Number(d.id) === id);
    if (!dealer) return res.status(404).json({ error: 'Dealer not found' });
    return res.json(dealer);
  } catch (err) {
    console.error('Error in /fetchDealer/:id', err);
    return res.status(500).json({ error: 'Server error' });
  }
});

// GET /fetchDealers/state/:state -> dealers by state (case-insensitive)
router.get('/fetchDealers/state/:state', async (req, res) => {
  try {
    const state = req.params.state;
    const raw = await readDealersRaw();
    const dealers = dealersArrayFrom(raw);

    if (!state || state.toLowerCase() === 'all') return res.json(raw);
    const filtered = dealers.filter(d => (d.state || '').toLowerCase() === state.toLowerCase());
    return res.json(filtered);
  } catch (err) {
    console.error('Error in /fetchDealers/state/:state', err);
    return res.status(500).json({ error: 'Server error' });
  }
});

module.exports = router;
