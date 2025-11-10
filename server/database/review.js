// review.js (append or update)
const express = require('express');
const fs = require('fs').promises;
const path = require('path');

const router = express.Router();
const DATA_DIR = path.join(__dirname, 'data');
const REVIEWS_FILE = path.join(DATA_DIR, 'reviews.json');

async function readReviews() {
  const text = await fs.readFile(REVIEWS_FILE, 'utf8');
  return JSON.parse(text);
}

async function writeReviews(obj) {
  await fs.writeFile(REVIEWS_FILE, JSON.stringify(obj, null, 2), 'utf8');
}

// GET all reviews
router.get('/fetchReviews', async (req, res) => {
  try {
    const data = await readReviews();
    return res.json(data);
  } catch (err) {
    console.error('Error reading reviews:', err);
    return res.status(500).json({ error: 'Server error' });
  }
});

// GET reviews for a dealer id
router.get('/fetchReviews/dealer/:id', async (req, res) => {
  try {
    const id = Number(req.params.id);
    const data = await readReviews();
    const filtered = (data.reviews || []).filter(r => Number(r.dealership) === id);
    return res.json({ reviews: filtered });
  } catch (err) {
    console.error('Error reading reviews:', err);
    return res.status(500).json({ error: 'Server error' });
  }
});

// POST insert review
router.post('/insertReview', async (req, res) => {
  try {
    const body = req.body;

    // minimal validation — adjust fields to match your frontend
    const required = ['name', 'dealership', 'review'];
    const missing = required.filter(f => body[f] === undefined || body[f] === null || body[f] === '');
    if (missing.length) {
      return res.status(400).json({ error: 'Missing fields', missing });
    }

    const data = await readReviews();
    data.reviews = data.reviews || [];

    // create new id
    const maxId = data.reviews.reduce((m, r) => Math.max(m, Number(r.id || 0)), 0);
    const newId = maxId + 1;

    const newReview = {
      id: newId,
      name: body.name,
      dealership: Number(body.dealership),
      review: body.review,
      purchase: !!body.purchase,               // boolean
      purchase_date: body.purchase_date || null,
      car_make: body.car_make || null,
      car_model: body.car_model || null,
      car_year: body.car_year ? Number(body.car_year) : null,
      // add any other fields you want to store
    };

    data.reviews.push(newReview);
    await writeReviews(data);

    return res.status(201).json({ success: true, review: newReview });
  } catch (err) {
    console.error('Error inserting review:', err);
    return res.status(500).json({ error: 'Server error' });
  }
});

// SIMPLE SENTIMENT ANALYZER (add this to review.js)
const positiveWords = ["good", "great", "excellent", "amazing", "awesome", "love", "liked", "best", "happy"];
const negativeWords = ["bad", "terrible", "poor", "worst", "awful", "hate", "disappoint", "angry", "slow"];

// helper
function analyzeSentiment(text) {
  if (!text || typeof text !== 'string') return { sentiment: 'neutral', score: 0 };

  const lower = text.toLowerCase();
  let score = 0;
  for (const w of positiveWords) if (lower.includes(w)) score += 1;
  for (const w of negativeWords) if (lower.includes(w)) score -= 1;

  let sentiment = 'neutral';
  if (score > 0) sentiment = 'positive';
  if (score < 0) sentiment = 'negative';

  return { sentiment, score };
}


router.get('/analyze', (req, res) => {
  const text = req.query.text || req.query.review || '';
  if (!text) return res.status(400).json({ error: 'Provide ?text=your+review' });

  const result = analyzeSentiment(text);
  return res.json({ text, ...result });
});

router.post('/analyze', (req, res) => {
  const bodyText = req.body.text || req.body.review || '';
  if (!bodyText) return res.status(400).json({ error: 'Send JSON with { "text": "..." }' });

  const result = analyzeSentiment(bodyText);
  return res.json({ text: bodyText, ...result });
});


module.exports = router;
