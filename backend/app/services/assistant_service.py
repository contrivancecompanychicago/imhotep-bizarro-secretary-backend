from app.config import settings


def build_onboarding_response(
    message: str,
    user_name: str | None = None,
    user_email: str | None = None,
    user_type: str = "new",
    site_url: str | None = None,
) -> str:
    site_url = site_url or settings.deep_human_families_site_url
    normalized = (message or "").strip().lower()

    if user_type == "new":
        if "hello" in normalized or "hi" in normalized:
            return (
                "Hello and welcome to the DEEP Human Families onboarding experience. "
                "I can help you understand the site, complete your onboarding steps, "
                "and answer questions about what happens next. "
                f"You can continue here: {site_url}"
            )

        if "next step" in normalized or "what do i do" in normalized or "start" in normalized:
            return (
                "The next step is to complete your onboarding details and review your information "
                "before continuing. If you are unsure where to begin, I can walk you through it step by step."
            )

        if "help" in normalized or "question" in normalized:
            return (
                "I can help with onboarding, account questions, returning-user support, and next-step guidance. "
                "If your question involves an urgent medical concern, please contact a clinician or emergency services immediately."
            )

        return (
            "I’m here to help with your DEEP Human Families onboarding experience. "
            "You can ask about next steps, account setup, onboarding questions, or returning-user support. "
            "For urgent medical issues, please contact a healthcare professional immediately."
        )

    if user_type == "existing":
        if "status" in normalized or "where am i" in normalized or "progress" in normalized:
            return (
                "Welcome back. You can continue your onboarding or review your saved information on the site. "
                "If you need help finding the next step, I can guide you through the process."
            )

        if "appointment" in normalized or "schedule" in normalized:
            return (
                "I can help you review your appointment or schedule information. "
                "Please share the date, name, or concern you need help with and I’ll guide you to the next step."
            )

        if "help" in normalized or "question" in normalized:
            return (
                "I can help with your current onboarding progress, schedule questions, and return-to-site support. "
                "If you need a medical review or urgent care response, please contact a provider or emergency service."
            )

        return (
            "Welcome back. I can help you continue your onboarding, review your progress, "
            "or answer questions about your current experience. "
            "For urgent medical concerns, contact a clinician right away."
        )

    return (
        "I’m here to support your DEEP Human Families onboarding experience. "
        "I can help with registration questions, next steps, and returning-user assistance. "
        "If this is a medical emergency, contact a clinician or emergency care immediately."
    )
