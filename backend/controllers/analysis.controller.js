const axios = require("axios");
const FormData = require("form-data");
const fs = require("fs");
const path = require("path");
const Analysis = require("../models/Analysis");

/**
 * Analyze uploaded slide
 * Flow: React -> Node -> Python ML -> MongoDB
 */
exports.analyzeSlide = async (req, res) => {
    try {
        // Validate file
        if (!req.file) {
            return res.status(400).json({ msg: "No file uploaded" });
        }

        const filePath = req.file.path;

        //  Prepare file for Python ML service
        const formData = new FormData();
        formData.append("file", fs.createReadStream(filePath));

        //  Call Python ML service
        const response = await axios.post(
            "http://127.0.0.1:8000/upload-image/",
            formData,
            {
                headers: formData.getHeaders(),
                timeout: 20000 // 20s timeout (ML can be slow)
            }
        );

        //  Extract ML result
        const mlResult = response.data.analysis_result;

        if (!mlResult) {
            return res.status(500).json({ msg: "Invalid ML response" });
        }

        // Save analysis to MongoDB
        const analysis = await Analysis.create({
            user: req.user, // from auth middleware
            filename: req.file.filename,
            blur_score: mlResult.blur_score,
            tissue_coverage: mlResult.tissue_coverage,
            stain_quality: mlResult.stain_quality,
            overall_quality: mlResult.overall_quality,
            decision: mlResult.decision
        });

        // (Optional but recommended) delete temp file
        fs.unlink(filePath, (err) => {
            if (err) console.error("File cleanup error:", err);
        });

        // Send response to frontend
        res.status(200).json({
            success: true,
            analysis
        });

    } catch (error) {
        console.error("Analysis error:", error.message);

        res.status(500).json({
            success: false,
            msg: "Slide analysis failed"
        });
    }
};


//Reference frontend code to call this controller:

// const formData = new FormData();
// formData.append("slide", file); // MUST match upload.single("slide")

// await fetch("http://localhost:5000/api/analyze", {
//   method: "POST",
//   headers: {
//     Authorization: token
//   },
//   body: formData
// });
