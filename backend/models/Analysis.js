const mongoose = require("mongoose");

const AnalysisSchema = new mongoose.Schema(
    {
        user: {
            type: mongoose.Schema.Types.ObjectId,
            ref: "User",
            required: true
        },
        filename: String,
        blur_score: Number,
        tissue_coverage: Number,
        stain_quality: Number,
        overall_quality: Number,
        decision: String,
    },
    {timestamps: true}
);

module.exports = mongoose.model("Analysis", AnalysisSchema);