const express = require("express");
const router = express.Router();
const upload = require("../config/multer");
const authMiddleware = require("../middleware/auth.middleware");
const { analyzeSlide, getMyAnalysis, getAnalysisById } = require("../controllers/analysis.controller");

router.post("/analyze", authMiddleware, upload.single("image"), analyzeSlide);
router.get("/myanalysis", authMiddleware, getMyAnalysis);
router.get("/:id", authMiddleware, getAnalysisById);

module.exports = router;