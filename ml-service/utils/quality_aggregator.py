def aggregate_quality(
    blur_score: float,
    tissue_coverage: float,
    stain_quality: float
):
    """
    Returns overall quality score and decision
    """

    # Weights (can be tuned later)
    W_BLUR = 0.4
    W_TISSUE = 0.4
    W_STAIN = 0.2

    # Convert blur to quality (lower blur = better)
    blur_quality = 1.0 - blur_score

    overall_quality = (
        W_BLUR * blur_quality +
        W_TISSUE * tissue_coverage +
        W_STAIN * stain_quality
    )

    # Decision thresholds
    if overall_quality >= 0.7:
        decision = "ACCEPT"
    elif overall_quality >= 0.5:
        decision = "REVIEW"
    else:
        decision = "REJECT"

    return overall_quality, decision
