// inventory.js
const express = require('express');
const fs = require('fs').promises;
const path = require('path');

const router = express.Router();
const DATA_DIR = path.join(__dirname, 'data');            // matches your repo layout
const CARS_FILE = path.join(DATA_DIR, 'car_records.json');

// helper to read cars file
async function readCars() {
  const text = await fs.readFile(CARS_FILE, 'utf8');
  // some sample files wrap array under "cars" like { "cars": [ ... ] }
  const obj = JSON.parse(text);
  if (Array.isArray(obj)) return obj;
  if (Array.isArray(obj.cars)) return obj.cars;
  // fallback: return parsed object
  return obj;
}

// GET /fetchCars -> list all car records
router.get('/fetchCars', async (req, res) => {
  try {
    const cars = await readCars();
    return res.json({ cars });
  } catch (err) {
    console.error('Error reading cars:', err);
    return res.status(500).json({ error: 'Could not read cars' });
  }
});

// GET /fetchCar/:id -> single car by index or id (try both)
router.get('/fetchCar/:id', async (req, res) => {
  try {
    const id = Number(req.params.id);
    const cars = await readCars();
    // try if each car has "id" field
    const byId = cars.find(c => Number(c.id) === id);
    if (byId) return res.json(byId);

    // else if id is index (1-based)
    if (!isNaN(id) && id > 0 && id <= cars.length) {
      return res.json(cars[id - 1]);
    }

    return res.status(404).json({ error: 'Car not found' });
  } catch (err) {
    console.error(err);
    return res.status(500).json({ error: 'Server error' });
  }
});

// GET /fetchCars/dealer/:dealer_id -> cars for a dealer
router.get('/fetchCars/dealer/:dealer_id', async (req, res) => {
  try {
    const dealerId = Number(req.params.dealer_id);
    const cars = await readCars();
    const filtered = cars.filter(c => Number(c.dealer_id) === dealerId);
    return res.json({ cars: filtered });
  } catch (err) {
    console.error(err);
    return res.status(500).json({ error: 'Server error' });
  }
});

module.exports = router;
