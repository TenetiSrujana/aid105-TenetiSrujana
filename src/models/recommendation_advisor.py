def generate_recommendation_report(scheme_result):
    score = scheme_result["score"]
    confidence = scheme_result["confidence"]
    scheme = scheme_result["scheme"]        
    reasons = scheme_result["reasons"]

    # Priority logic
    if score >= 80:
        priority = "APPLY IMMEDIATELY"
    elif score >= 50:
        priority = "PREPARE DOCUMENTS"
    else:
        priority = "NOT RECOMMENDED CURRENTLY"

    # Base required documents
    documents = [
        "Aadhaar Card",
        "Income Certificate",
        "Residence Proof"
    ]

    # Scheme-specific documents
    if "Scholarship" in scheme:
        documents.append("Bonafide / Study Certificate")

    if "Housing" in scheme:
        documents.append("Land Ownership / Ration Card")

    if "Pension" in scheme:
        documents.append("Age Proof / Disability Certificate")

    steps = [
        f"Review eligibility criteria for {scheme}",
        "Collect required documents",
        "Apply via official government portal",
        "Track application status regularly"
    ]

    return {
        "scheme": scheme,
        "priority": priority,
        "confidence": confidence,
        "score": score,
        "reasons": reasons,
        "required_documents": documents,
        "next_steps": steps
    }
