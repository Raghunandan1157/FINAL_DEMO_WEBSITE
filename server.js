// server.js  (CommonJS; no "type":"module" needed)
const express = require("express");
const cors = require("cors");
const jwt = require("jsonwebtoken");
require("dotenv").config();

const app = express();
const PORT = process.env.PORT || 3000;
const SECRET = process.env.CHATBOT_IDENTITY_SECRET;

// Configure CORS: set ALLOWED_ORIGINS in .env as a comma-separated list
const allowed = (process.env.ALLOWED_ORIGINS || "")
  .split(",")
  .map((s) => s.trim())
  .filter(Boolean);

app.use(
  cors({
    origin: (origin, cb) => {
      if (!origin) return cb(null, true); // allow same-origin / curl
      if (!allowed.length || allowed.includes(origin)) return cb(null, true);
      return cb(new Error("CORS: origin not allowed"));
    },
  })
);
app.use(express.json());

if (!SECRET) {
  console.error("❌ Missing CHATBOT_IDENTITY_SECRET in .env");
  process.exit(1);
}

app.get("/health", (req, res) => res.json({ ok: true }));

// POST is better than GET to avoid leaking details in URLs
app.post("/get-user-token", (req, res) => {
  try {
    const { user_id, email, name, org, role, stripe_accounts } = req.body || {};
    if (!user_id && !email) {
      return res.status(400).json({ error: "user_id or email is required" });
    }

    const payload = {
      user_id,
      email,
      name,
      org,
      role,
      // include only if provided
      ...(Array.isArray(stripe_accounts) ? { stripe_accounts } : {}),
    };

    const token = jwt.sign(payload, SECRET, { expiresIn: "1h" });
    res.json({ token });
  } catch (e) {
    console.error(e);
    res.status(500).json({ error: "Token generation failed" });
  }
});

app.listen(PORT, () =>
  console.log(`✅ Chatbase identity server on http://localhost:${PORT}`)
);
