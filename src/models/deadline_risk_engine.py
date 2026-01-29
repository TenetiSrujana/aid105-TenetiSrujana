def analyze_deadline_risk(scheme_data):
    """
    Analyze deadline urgency and risk in a safe, consistent format.
    """

    deadline = scheme_data.get("deadline")
    benefit = int(scheme_data.get("estimated_benefit", 0))

    # Default response
    result = {
        "status": "ACTIVE",
        "urgency": "LOW",
        "risk_level": "LOW",
        "warning": "✅ Sufficient time available",
        "estimated_loss": f"₹{benefit} potential benefit at risk"
    }

    # Missing deadline
    if not deadline:
        return result

    # Expired deadline
    if isinstance(deadline, str) and deadline.lower() == "expired":
        return {
            "status": "EXPIRED",
            "urgency": "EXPIRED",
            "risk_level": "CRITICAL",
            "warning": "❌ Deadline missed. Scheme no longer available.",
            "estimated_loss": "No action possible (scheme closed)"
        }

    return result
