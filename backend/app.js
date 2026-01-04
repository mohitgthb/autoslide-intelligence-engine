const express = require('express');
const cors = require('cors');

const app = express();

const authMiddleware = require('./middleware/auth.middleware');
const authRoutes = require('./routes/auth.routes');
const analysisRoutes = require('./routes/analysis.routes');

// Middleware
app.use(cors());
app.use(express.json());

app.use("/api/auth", authRoutes);
app.use("/api/analyze", analysisRoutes);

module.exports = app;