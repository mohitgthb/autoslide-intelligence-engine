const express = require("express");
const router = express.Router();
const upload = require("../config/multer");
const authMiddleware = require("../middleware/auth.middleware");
const { analyzeSlide } = require("../controllers/analysis.controller");

// Route: POST /api/analysis/upload
router.post("/analyze", authMiddleware, upload.single("image"), analyzeSlide);

module.exports = router;